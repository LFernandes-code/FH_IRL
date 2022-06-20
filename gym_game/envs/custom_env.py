import gym
from gym import spaces
import numpy as np
from gym_game.envs.flower_hunter import PyGame2D

class FHEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self, map_name):
        self.map = map_name
        self.game_actions = ['n', ' ', 'w', 's', 'a', 'd', 'wa', 'wd', 'sa', 'sd', 'w ', 's ', 'a ', 'd ', 'wa ', 'wd ', 'sa ', 'sd ']
        self.pygame = PyGame2D(self.map)
        # actions: ['w', 's', 'a', 'd', 'attack', 'go_collect', 'go_health', 'go_obj', 'wait']
        self.action_space = spaces.Discrete(8)
        #obs: dist_to_objective, dist_to_enemy, dist_to_coin, dist_to_cake, health, dist_from_start
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0]), np.array([300, 300, 300, 300, 100, 300]), dtype=np.int)
        self.doing_action = False
        self.action_plan = []

    def reset(self):
        map_used = self.map
        del self.pygame
        self.pygame = PyGame2D(map_used)
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        game_action = self.convert_action_to_game_action(action)
        self.pygame.action(game_action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view()

    def convert_action_to_game_action(self, action):
        if action < 4:
            return self.game_actions[action + 2]
        #check if action is complex
        pass