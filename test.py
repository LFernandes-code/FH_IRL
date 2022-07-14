import sys
import numpy as np
import math
import random

import gym
import gym_game

import time


if __name__ == "__main__":
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    env.reset()
    for i in range(len(env.available_actions)):
        env.step(i)
    
