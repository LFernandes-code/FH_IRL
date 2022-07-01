import gym
from gym import spaces
import numpy as np
from gym_game.envs.flower_hunter import PyGame2D
from gym_game.envs.map_loader import *

class FHEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self, map_name):
        self.game_actions = ['n', ' ', 'w', 's', 'a', 'd', 'wa', 'wd', 'sa', 'sd', 'w ', 's ', 'a ', 'd ', 'wa ', 'wd ', 'sa ', 'sd ']
        self.available_actions = ['w', 's', 'a', 'd', 'go_collect', 'go_health', 'go_objective', 'attack', 'wait']
        
        self.map_id = map_name
        self.pygame = PyGame2D(self.map_id)
        self.map = Mem_Map(self.map_id)
        
        self.action_space = spaces.Discrete(8)
        #obs: dist_to_objective, dist_to_enemy, dist_to_coin, dist_to_cake, health
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0]), np.array([301, 301, 301, 301, 100]), dtype=np.int)
        
        self.doing_action = False
        self.action_plan = []
        self.current_action = -1

    def reset(self):
        map_used = self.map_id
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
        #check if action is complex
        if action < 4:
            #basic actions
            return self.game_actions[action + 2]
        elif action < 7:
            #(complex) go to static objects
            item_type = self.available_actions[action].split('_')[1]
            item_position = self.get_position_of_closest_item(item_type)
            if action == self.current_action:
                #execute plan
                return self.action_plan.pop(0)
            else:
                #run A-star
                p_cell = self.convert_position_to_cell((self.world.player.imagined_x, self.world.player.imagined_y))
                item_cell = self.convert_position_to_cell(item_position)
                action_diretions = self.map.a_star(p_cell, item_cell)
                for direction in action_diretions:
                    self.action_plan.append(self.action_tuple_to_key(direction))
                    self.action_plan.append(self.action_tuple_to_key(direction))

                return self.action_plan.pop(0)
                
        elif action == 7:
            #(complex) go to dynamic object
            enemy_dir = self.get_direction_of_closest_enemy()
            return self.attack_direction_action(enemy_dir)

    def action_tuple_to_key(self, action_tuple):
        (x,y) = action_tuple
        action = ""
        if y > 0:
            action += "s"
        elif y < 0:
            action += "w"
        if x > 0:
            action += "d"
        elif x < 0:
            action += "a"

        return action

    def get_direction_of_closest_enemy(self):
        distance_closest_enemy = self.pygame.perceptor.distance_closest_enemy
        for enemy in self.pygame.world.enemy_group:
            if self.pygame.world.in_view(enemy):
                distance = math.sqrt((self.world.player.rect.x - enemy.rect.x )**2 + (self.world.player.rect.y - enemy.rect.y)**2 )
                myradians = math.atan2(enemy.rect.y - self.world.player.rect.y, enemy.rect.x - self.world.player.rect.x)
                direction = math.degrees(myradians)
                while(direction > 360):
                    direction -= 360

                while(direction < 0):
                    direction += 360

                if distance < distance_closest_enemy:
                    distance_closest_enemy = distance
                    direction_closest_enemy = direction
        
        return direction_closest_enemy

    def get_position_of_closest_item(self, item_type):
        sprite_group = []
        if item_type == 'collect':
            sprite_group = self.pygame.world.money_group
        elif item_type == 'objective':
            sprite_group = self.pygame.world.flower_group
        elif item_type == 'health':
            sprite_group = self.pygame.world.food_group

        distance = float('inf')
        position = None

        for item_sprite in sprite_group:
            prov_distance = math.sqrt((self.world.screen_width/2 - item_sprite.rect.x)**2 + (self.world.screen_height/2 - item_sprite.rect.y)**2)
            if prov_distance < distance:
                position = (self.world.player.imagined_x + item_sprite.rect.x, self.world.player.imagined_y + item_sprite.rect.y)

        return position

    def attack_direction_action(self, direction_closest_enemy):
        action = ''
        if (direction_closest_enemy < 22.5 and direction_closest_enemy >= 0) or (direction_closest_enemy <= 360 and direction_closest_enemy > 337.5):
            action = 'd'
        elif (direction_closest_enemy < 67.5 and direction_closest_enemy >= 22.5):
            action = 'sd'
        elif (direction_closest_enemy < 112.5 and direction_closest_enemy >= 67.5):
            action = 's'
        elif (direction_closest_enemy < 157.5 and direction_closest_enemy >= 112.5):
            action = 'sa'
        elif (direction_closest_enemy < 202.5 and direction_closest_enemy >= 157.5):
            action = 'a'
        elif (direction_closest_enemy < 247.5 and direction_closest_enemy >= 202.5):
            action = 'wa'
        elif (direction_closest_enemy < 292.5 and direction_closest_enemy >= 247.5):
            action = 'w'
        elif (direction_closest_enemy < 337.5 and direction_closest_enemy >= 292.5):
            action = 'wd'
        else:
            print("Error in directions!!!")
            exit()
        if self.pygame.perceptor.distance_closest_enemy < 65:
            action = action + ' '
        return action

    def convert_position_to_cell(self, position):
        return tuple(map(lambda i: ((i + 10) / 5) // 4 , position))