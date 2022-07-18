from unicodedata import name
import gym
import seals
import gym_game
import time
import pickle
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from Trace_generator import *
from stable_baselines3 import PPO
from imitation.algorithms.adversarial.gail import GAIL
from imitation.rewards.reward_nets import BasicRewardNet
from imitation.util.networks import RunningNorm
from stable_baselines3.common.evaluation import evaluate_policy


from imitation.algorithms.mce_irl import (
    MCEIRL,
    mce_occupancy_measures,
    mce_partition_fh,
    TabularPolicy,
)


def GAIL_IRL(venv, cluster ,learner, rollouts, reward_net):
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
    learner_rewards_before_training, _ = evaluate_policy(
        learner, venv, 100, return_episode_rewards=True
    )
    print("done before train")
    
    gail_trainer.train(120000)  # Note: set to 300000 for better results
    learner_rewards_after_training, _ = evaluate_policy(
        learner, venv, 100, return_episode_rewards=True
    )
    irl_cluster_file = "IRL/GAIL_" + cluster + ".pl"
    file = open(irl_cluster_file, 'wb')
    pickle.dump(gail_trainer.policy, file)

    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == "__main__":
    level = "Level1"
    cluster_threshold = 6

    print('setup env')
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    venv = DummyVecEnv([lambda: gym.make("FlowerHunter-v0", map_name = "Level1")] * 8)
    #generate trajectories

    level_cluster =  "Clusters/" + level + "_clusters"
    level_clusters = os.listdir(level_cluster)
    print(level_clusters)
    for cluster in tqdm(level_clusters):
        if int(cluster.split('_____')[1]) >= cluster_threshold:
            rollouts = generate_trajectories(cluster, "Level1_clusters", env)

            print('setup learner')
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
            
            print("start IRL")
            GAIL_IRL(venv, cluster, learner, rollouts, reward_net)
            #gail -> policy._predict(obs)