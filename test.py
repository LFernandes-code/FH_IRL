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
    a = [1,2,3]
    a.remove(2)
    a.remove(4)
    print(a)
    