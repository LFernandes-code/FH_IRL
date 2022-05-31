import sys
import numpy as np
import math
import random

import gym
import gym_game




"""
key_up = -1
key_down = -1

def action(action):
    global key_down
    global key_up
    if key_down == -1:
        key_down = action
        print('generate event')
    elif action != key_down:
        key_up = key_down
        key_down = action

    print(key_down, key_up)

action(1)
action(1)
action(1)
action(0)
"""
if __name__ == "__main__":
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    MAX_EPISODES = 9999
    MAX_TRY = 1000
    epsilon = 1
    epsilon_decay = 0.999
    learning_rate = 0.1
    gamma = 0.6
    env.reset()
    for i in range(2000):
        if i % 100 == 0:
            env.render()
            env.step(4)
        else:
            env.render()
            env.step(0)