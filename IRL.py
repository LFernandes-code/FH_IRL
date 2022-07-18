from unicodedata import name
import gym
import seals
import gym_game
import time
import pickle
from Trace_generator import *
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from imitation.data import rollout
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, resettable_env
from imitation.rewards import reward_nets
from imitation.rewards.reward_nets import BasicRewardNet
from imitation.util.networks import RunningNorm
from stable_baselines3.common.evaluation import evaluate_policy

from imitation.algorithms.adversarial.gail import GAIL
from imitation.algorithms.mce_irl import (
    MCEIRL,
    mce_occupancy_measures,
    mce_partition_fh,
    TabularPolicy,
)

def train_mce_irl(cluster, demos, **kwargs):
    state_venv = resettable_env.DictExtractWrapper(
        DummyVecEnv([lambda: gym.make("FlowerHunter-v0", map_name = "Level1")] * 4), "state"
    )
    obs_venv = resettable_env.DictExtractWrapper(
        DummyVecEnv([lambda: gym.make("FlowerHunter-v0", map_name = "Level1")] * 4), "obs"
    )

    reward_net = reward_nets.BasicRewardNet(
        env.pomdp_observation_space,
        env.action_space,
        use_action=False,
        use_next_state=False,
        use_done=False,
        hid_sizes=[],
    )

    mce_irl = MCEIRL(demos, env, reward_net, linf_eps=1e-3)
    mce_irl.train(**kwargs)

    """
    imitation_trajs = rollout.generate_trajectories(
        policy=mce_irl.policy,
        venv=state_venv,
        sample_until=rollout.make_min_timesteps(5000),
    )
    print("Imitation stats: ", rollout.rollout_stats(imitation_trajs))
    """

    irl_cluster_file = "IRL/MCE_" + cluster + ".pl"
    file = open(irl_cluster_file, 'wb')
    pickle.dump(mce_irl.policy, file)



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
    alg = "GAIL"
    level = "Level1"
    cluster_threshold = 6

    print('setup env')
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    
    #generate trajectories

    level_cluster =  "Clusters/" + level + "_clusters"
    level_clusters = os.listdir(level_cluster)
    print(level_clusters)
    for cluster in tqdm(level_clusters):
        if int(cluster.split('_____')[1]) >= cluster_threshold:
            rollouts = generate_trajectories(cluster, "Level1_clusters", env)
            if alg == "GAIL":
                GAIL_IRL(cluster, rollouts)
            elif alg == "MCE":
                train_mce_irl(cluster, rollouts)
            #gail -> policy._predict(obs)