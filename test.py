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
    env.step(3)
    """
    done = False
    for i in range(2500):
        print(i)
        if i < 150:
            _, _ , done , _ = env.step(0)
        else:
            _, _ , done , _ = env.step(3)
        
        if done:
            break
        
        env.render()
    
    """