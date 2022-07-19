import sys
import numpy as np
import math
import random

import gym
import gym_game
from stable_baselines3.common import base_class

class IRL_agent():
    #base_class.BasePolicy
    def __init__(self, irl_alg, cluster):
        self.policy = self.load_policy(irl_alg, cluster)
        pass

    def load_policy(self, irl_alg, cluster):
        pass

    def select_action(self, obs):
        return self.policy.predict(obs)

if __name__ == "__main__":
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    env.reset()
    done = False
    while not done:
        _, _, done,_ = env.step(5)
        env.render()