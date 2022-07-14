import sys
import numpy as np
import math
import random

import gym
import gym_game

import time
from gym_game.envs.map_loader import * 

MAP_HEIGHT = 600
MAP_WIDTH = 600


def convert_position_to_cell(position):
    cell = tuple(map(lambda i: ((i + 10) / 5) // 4 , position))
    print(position)
    print(cell)
    return tuple(map(lambda i: ((i + 10) / 5) // 4 , position))

if __name__ == "__main__":
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    env.reset()
    done = False
    while not done:
        _, _, done,_ = env.step(5)
        env.render()
    """
    tup = (114.0, 59.0)
    if type(tup[0]) == float:
        tup = tuple(map(int, tup))
    print(tup)
    """
   
