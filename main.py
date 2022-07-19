from shutil import register_unpack_format
import sys
import pickle

import gym
import gym_game
from stable_baselines3.common import base_class

class IRL_Agent():
    #base_class.BasePolicy
    def __init__(self, irl_alg, cluster):
        self.policy = self.load_policy(irl_alg, cluster)

    def load_policy(self, irl_alg, cluster):
        irl_cluster_file = "IRL/" + irl_alg + "_" + cluster + ".pl"

        with open(irl_cluster_file, 'rb') as f:
            policy =  pickle.load(f)
            return policy

    def select_action(self, obs):
        return self.policy.predict(obs)

if __name__ == "__main__":
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    agent = IRL_Agent("GAIL", "0")
    obs = env.reset()
    done = False
    act = agent.select_action(obs)
    while not done:
        obs, _, done,_ = env.step(act)
        act = agent.select_action(obs)
        env.render()