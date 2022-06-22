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

def get_action(a_id):
    acs = ['d', 'a', 'w', 's', 'attack', 'go_collect', 'go_health', 'go_obj', 'wait']
    if a_id < 4:
        print(acs[a_id])
    elif a_id < 8:
        print(acs[a_id])
    
if __name__ == "__main__":
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    env.reset()
    """
    # 1 tick = 0.004seconds
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
  