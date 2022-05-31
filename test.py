import sys
import numpy as np
import math
import random

import gym
import gym_game

import time



key_up = []
key_down = []

def action(action):
    global key_down
    global key_up
    if not key_down:
        key_down.append(action)
        print('pressed key event')
    else:
        for key in key_down:
            key_up.append(key)
        key_down = []

    print(key_down, key_up)


if __name__ == "__main__":
    
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    env.reset()
    for i in range(1000):
        env.step(0)
        env.render()
    

    #action(1)
    #action(1)
    #action(1)
    #action(0)
    #action(0)