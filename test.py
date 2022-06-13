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
    get_action(0)
    get_action(2)
    get_action(4)
    get_action(7)
    """
    env = gym.make("FlowerHunter-v0", map_name = "Level1")
    env.reset()
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
    """
    action_keys = [pygame.locals.K_RIGHT, pygame.locals.K_LEFT, pygame.locals.K_UP, pygame.locals.K_DOWN, pygame.locals.K_SPACE]
    #create the event
			if self.key_down == -1:
				newevent_down = pygame.event.Event(pygame.locals.KEYDOWN, key=action_keys[action], mod=pygame.locals.KMOD_NONE)
				#add the event to the queue
				pygame.event.post(newevent_down)
				self.key_down = action
			elif action == self.key_down:
				newevent_down = pygame.event.Event(pygame.locals.KEYDOWN, key=action_keys[action], mod=pygame.locals.KMOD_NONE)
				#add the event to the queue
				pygame.event.post(newevent_down)
				self.key_down = action
			else:
				#create the event
				newevent_down = pygame.event.Event(pygame.locals.KEYDOWN, key=action_keys[action], mod=pygame.locals.KMOD_NONE)
				#add the event to the queue
				pygame.event.post(newevent_down)

				newevent_up = pygame.event.Event(pygame.locals.KEYUP, key=action_keys[self.key_down], mod=pygame.locals.KMOD_NONE)
				#add the event to the queue
				pygame.event.post(newevent_up)

				self.key_down = action
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				handle_key_down(self.world, event.key, self.last_sword_parameters)
			if event.type == pygame.KEYUP:
				handle_key_up(self.world, event.key, self.last_sword_parameters)
    """