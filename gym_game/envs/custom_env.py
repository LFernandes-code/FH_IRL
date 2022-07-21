from tkinter import NO
from tkinter.tix import Tree
import gym
from gym import spaces
import numpy as np
from gym_game.envs.flower_hunter import PyGame2D
from gym_game.envs.map_loader import *

class FHEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self, map_name):
        self.game_actions = ['n', ' ', 'w', 's', 'a', 'd', 'wa', 'wd', 'sa', 'sd', 'w ', 's ', 'a ', 'd ', 'wa ', 'wd ', 'sa ', 'sd ']
        self.available_actions = ['w', 's', 'a', 'd',' attack', 'go_objective', 'go_enemy', 'go_collect', 'go_health', 'wait']
        
        self.map_id = map_name
        self.pygame = PyGame2D(self.map_id, False)
        self.map = Mem_Map(self.map_id)
        
        #actions: 'w', 's', 'a', 'd',' attack', 'go_objective', 'go_enemy', 'go_collect', 'go_health', 'wait'
        self.action_space = spaces.Discrete(10)
        #obs: dist_to_objective, dist_to_enemy, dist_to_coin, dist_to_cake, health, %coins, %kills
        self.observation_space = spaces.Box(np.array([20, 20, 20, 20, 0, 0, 0]), np.array([330, 330, 330, 330, 100, 10, 10]), dtype=np.int)
        
        self.doing_action = False
        self.action_plan = []
        self.current_action = -1

    def reset(self):
        map_used = self.map_id
        del self.pygame
        self.pygame = PyGame2D(map_used)
        obs = self.observe_world(self.pygame.observe())
        return obs

    def step(self, action):
        game_action = self.convert_action_to_game_action(action)

        self.pygame.action(game_action)
        obs = self.observe_world(self.pygame.observe())
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view()

    # Util functions

    def write_trace(self):
        self.pygame.perceptor.write_to_file()
        for pos_to_write in self.pygame.world.pos_to_write:
            self.pygame.postextfile.write(pos_to_write)
        self.pygame.postextfile.close()

    def observe_world(self, reading):
        per = reading
        #obs: [dist_to_objective, dist_to_enemy, dist_to_coin, dist_to_cake, health, %coins, %kills]
        obs = []
        #dist_to_objective
        if per[-10][:-1] == 'inf':
            obs.append(int(self.observation_space.high[0]))
        else:
            value = min(int(self.observation_space.high[0]), int(float(per[-10][:-1])))
            obs.append(value)
        #dist_to_enemy
        if per[0][:-1] == 'inf':
            obs.append(int(self.observation_space.high[1]))
        else:
            value = min(int(self.observation_space.high[0]), int(float(per[0][:-1])))
            obs.append(value)
        #dist_to_coin
        if per[2][:-1] == 'inf':
            obs.append(int(self.observation_space.high[2]))
        else:
            value = min(int(self.observation_space.high[0]), int(float(per[2][:-1])))
            obs.append(value)
        #dist_to_cake
        if per[1][:-1] == 'inf':
            obs.append(int(self.observation_space.high[3]))
        else:
            value = min(int(self.observation_space.high[0]), int(float(per[1][:-1])))
            obs.append(value)
        #health
        obs.append(int(per[-9][:-1]))
        #% of coins
        if self.map.number_of_coins != 0:
            value = int( (float(per[-8][:-1]) / self.map.number_of_coins) *  self.observation_space.high[-2])
            obs.append(value)
        else:
            obs.append(self.observation_space.high[-2])
        #% of enemies
        if self.map.number_of_enemies != 0:
            value = int( (float(per[-7][:-1]) / self.map.number_of_enemies) *  self.observation_space.high[-2])
            obs.append(value)
        else:
            obs.append(self.observation_space.high[-2])
        
        return obs

    def convert_action_to_game_action(self, action):
        #check if action is complex
        if action < 4:
            #basic actions
            return self.game_actions[action + 2]
        
        elif action == 4:
            #(complex) go to dynamic object
            #and attack
            enemy_dir = self.get_direction_of_closest_enemy()
            return self.attack_direction_action(enemy_dir, attack=True)
        
        elif action == 6:
            #(complex) go to dynamic object
            enemy_dir = self.get_direction_of_closest_enemy()
            return self.attack_direction_action(enemy_dir)
        
        elif action < 8:
            #(complex) go to static objects
            item_type = self.available_actions[action].split('_')[1]
            item_position = self.get_position_of_closest_item(item_type)
            if item_position is None:
                return('n')
            elif action == self.current_action and len(self.action_plan) != 0:
                #execute plan
                #print("execute plan")
                return self.action_plan.pop(0)
            else:
                #run A-star
                #print("make plan")
                p_cell = self.convert_position_to_cell((self.pygame.world.player.imagined_x, self.pygame.world.player.imagined_y),False)
                item_cell = self.convert_position_to_cell(item_position)
    
                action_diretions = self.map.a_star(p_cell, item_cell)
                self.current_action = action
                for direction in action_diretions:
                    self.action_plan.append(self.action_tuple_to_key(direction))
                    self.action_plan.append(self.action_tuple_to_key(direction))
                    self.action_plan.append(self.action_tuple_to_key(direction))
                    self.action_plan.append(self.action_tuple_to_key(direction))

                return self.action_plan.pop(0)
        else:
            return('n')

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
        direction_closest_enemy = np.random.choice([0,90,180,270])
        for enemy in self.pygame.world.enemy_group:
            if self.pygame.world.in_view(enemy):
                distance = math.sqrt((self.pygame.world.player.rect.x - enemy.rect.x )**2 + (self.pygame.world.player.rect.y - enemy.rect.y)**2 )
                myradians = math.atan2(enemy.rect.y - self.pygame.world.player.rect.y, enemy.rect.x - self.pygame.world.player.rect.x)
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
            prov_distance = math.sqrt((self.pygame.world.screen_width/2 - item_sprite.rect.x)**2 + (self.pygame.world.screen_height/2 - item_sprite.rect.y)**2)
            if prov_distance < distance:
                position = (self.pygame.world.player.imagined_x + item_sprite.rect.x,  self.pygame.world.player.imagined_y + item_sprite.rect.y)

        return position

    def attack_direction_action(self, direction_closest_enemy, attack = False):
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
        if attack:
            action = action + ' '
        return action

    def convert_position_to_cell(self, position, convert = True):
        if convert:
            screen_dim = (self.pygame.height, self.pygame.width)
            og_pos = tuple(map(lambda i, j, s: i + j + 15 - s/2, position, self.map.start_player_position, screen_dim)) 
            cell = tuple(map(lambda i: ((i + 10) / 5) // 4 , og_pos))
            cell = tuple(map(lambda i, j: i - j, cell, self.map.start_player_cell))
        else:
            cell = tuple(map(lambda i: ((i + 10) / 5) // 4 , position))
        return cell
