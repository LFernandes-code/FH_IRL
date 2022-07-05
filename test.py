import sys
import numpy as np
import math
import random

import gym
import gym_game

import time


if __name__ == "__main__":
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    #env.reset()
    #env.step(3)
    a = "20.44"
    b = int(float(a))
    print(min(b,30))