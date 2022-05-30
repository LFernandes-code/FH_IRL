import gym
from gym import spaces
import numpy as np
from gym_game.envs.infinite_game import PyGame2D

class FHEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self, map_name):
        print(map_name)
        self.pygame = PyGame2D(map_name)
        # actions: RIGHT, LEFT, UP, DOWN, ATTACK, EMPTY
        self.action_space = spaces.Discrete(6)
        #obs: dist_to_objective, dist_to_enemy, dist_to_coin, dist_to_cake, health
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0]), np.array([300, 300, 300, 300, 100]), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = PyGame2D()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view()