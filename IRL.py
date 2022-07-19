import gym
import seals
import gym_game
import time
import pickle
import pprint
from Trace_generator import *
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from imitation.data import rollout
from imitation.data import types
from imitation.util import util

from imitation.envs import resettable_env
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from imitation.rewards import reward_nets
from imitation.rewards.reward_nets import BasicRewardNet
from imitation.util.networks import RunningNorm
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.policies import ActorCriticPolicy

from imitation.algorithms.adversarial.gail import GAIL
from imitation.algorithms.mce_irl import (
    MCEIRL,
    mce_occupancy_measures,
    mce_partition_fh,
    TabularPolicy,
)

from imitation.algorithms import bc
from imitation.algorithms import density as db

def density_irl(cluster, rollouts, FAST = True):
    # Set FAST = False for longer training. Use True for testing and CI.
    if FAST:
        N_VEC = 1
        N_TRAJECTORIES = 1
        N_ITERATIONS = 1
        N_RL_TRAIN_STEPS = 100

    else:
        N_VEC = 8
        N_TRAJECTORIES = 10
        N_ITERATIONS = 100
        N_RL_TRAIN_STEPS = int(1e5)

    env_level = {"map_name": "Level1"}

    env = util.make_vec_env("FlowerHunter-v0", N_VEC, env_make_kwargs= env_level)

    imitation_trainer = PPO(ActorCriticPolicy, env, learning_rate=3e-4, n_steps=2048)
    density_trainer = db.DensityAlgorithm(
        venv=env,
        demonstrations=rollouts,
        rl_algo=imitation_trainer,
        density_type=db.DensityType.STATE_ACTION_DENSITY,
        is_stationary=True,
        kernel="gaussian",
        kernel_bandwidth=0.2,  # found using divination & some palm reading
        standardise_inputs=True,
        allow_variable_horizon=True,
    )
    start_time = time.time()
    
    density_trainer.train()

    novice_stats = density_trainer.test_policy()
    print("Novice stats (true reward function):")
    pprint.pprint(novice_stats)
    novice_stats_im = density_trainer.test_policy(
        true_reward=False, n_trajectories=N_TRAJECTORIES
    )
    print("Novice stats (imitation reward function):")
    pprint.pprint(novice_stats_im)

    for i in range(N_ITERATIONS):
        density_trainer.train_policy(N_RL_TRAIN_STEPS)

        good_stats = density_trainer.test_policy(n_trajectories=N_TRAJECTORIES)
        print(f"Trained stats (epoch {i}):")
        pprint.pprint(good_stats)
        novice_stats_im = density_trainer.test_policy(true_reward=False)
        print(f"Trained stats (imitation reward function, epoch {i}):")
        pprint.pprint(novice_stats_im)

    
    irl_cluster_file = "IRL/DB_" + cluster + ".pl"
    file = open(irl_cluster_file, 'wb')
    pickle.dump(density_trainer.policy, file)

    print("--- %s seconds ---" % (time.time() - start_time))


def train_mce_irl(env, cluster, demos, **kwargs):
    reward_net = reward_nets.BasicRewardNet(
        env.observation_space,
        env.action_space,
        use_action=False,
        use_next_state=False,
        use_done=False,
        hid_sizes=[],
    )

    mce_irl = MCEIRL(demos, env, reward_net, linf_eps=1e-3)
    mce_irl.train(**kwargs)

    irl_cluster_file = "IRL/MCE_" + cluster + ".pl"
    file = open(irl_cluster_file, 'wb')
    pickle.dump(mce_irl.policy, file)

def bc_IRL(env, cluster, rollouts):
    transitions = rollout.flatten_trajectories(rollouts)

    bc_trainer = bc.BC(
    observation_space=env.observation_space,
    action_space=env.action_space,
    demonstrations=transitions,
    )
    
    start_time = time.time()
    
    bc_trainer.train(n_epochs=200)
    
    irl_cluster_file = "IRL/BC_" + cluster + ".pl"
    file = open(irl_cluster_file, 'wb')
    pickle.dump(bc_trainer.policy, file)

    print("--- %s seconds ---" % (time.time() - start_time))

def GAIL_IRL(cluster, rollouts):
    venv = DummyVecEnv([lambda: gym.make("FlowerHunter-v0", map_name = "Level1")] * 8)

    learner = PPO(
                env=venv,
                policy=MlpPolicy,
                batch_size=64,
                ent_coef=0.0,
                learning_rate=0.0003,
                n_epochs=10,
            )

    reward_net = BasicRewardNet(
        venv.observation_space, venv.action_space, normalize_input_layer=RunningNorm
    )

    gail_trainer = GAIL(
        demonstrations=rollouts,
        demo_batch_size=1024,
        gen_replay_buffer_capacity=2048,
        n_disc_updates_per_round=4,
        venv=venv,
        gen_algo=learner,
        reward_net=reward_net,
        allow_variable_horizon=True
    )

    start_time = time.time()
    
    gail_trainer.train(120000)  # Note: set to 300000 for better results
    
    irl_cluster_file = "IRL/GAIL_" + cluster + ".pl"
    file = open(irl_cluster_file, 'wb')
    pickle.dump(gail_trainer.policy, file)

    print("--- %s seconds ---" % (time.time() - start_time))
    

if __name__ == "__main__":
    alg = "DB" #"BC" #"GAIL"
    level = "Level1"
    cluster_threshold = 6

    print('setup env')
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    
    #generate trajectories
    #"""
    level_cluster =  "Clusters/" + level + "_clusters"
    level_clusters = os.listdir(level_cluster)
    print(level_clusters)
    for cluster in level_clusters:
        if int(cluster.split('_____')[1]) >= cluster_threshold:
            rollouts = generate_trajectories(cluster, "Level1_clusters", env)
            if alg == "GAIL":
                GAIL_IRL(cluster, rollouts)
            elif alg == "BC":
                bc_IRL(env, cluster, rollouts)
            elif alg == "DB":
                density_irl(cluster, rollouts)
            #gail -> policy._predict(obs)
    #"""
    
    """
    cluster = "15_____8"
    rollouts = generate_trajectories(cluster, "Level1_clusters", env)
    density_irl(cluster, rollouts)
    #"""