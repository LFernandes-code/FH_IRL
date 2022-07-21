from shutil import register_unpack_format
import sys
import pickle

import gym
import gym_game
from stable_baselines3.common import base_class
import imitation

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
    agent = IRL_Agent("GAIL", "15_____8")
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    obs = env.reset()
    done = False
    f_reward = -2
    #"""
    act = agent.select_action(obs)[0]
    max_steps = 3000
    current_step = 0
    while not done:
        print("step: ", current_step)
        obs, r, done,_ = env.step(act)
        act = agent.select_action(obs)[0]
        f_reward = r
        #env.render()
        current_step += 1
        if current_step >= max_steps:
            print("Max step reached")
            done = True
    #"""
    print("final rward: ", f_reward)