from gym_game.envs.flower_hunter import *
import os
import ast

import gym_game
import gym

def generate_trace_perceptor(level, cluster_threshold):
    map_name = "Maps/" + level + ".csv"
    level_cluster =  "Clusters/" + level + "_clusters"

    num_directions = 8
    frame_rate = 0.0

    pygame.init()
    big_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 62)
    medium_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 32)
    small_fontzy =  pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 24)
    screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
    
    level_clusters = os.listdir(level_cluster)
    dir = ""
    for cluster in level_clusters:
        if int(cluster.split('_____')[1]) >= cluster_threshold:
            cluster_elements = os.listdir(level_cluster + "/" + cluster)
            dir = level_cluster + "/" + cluster
            for element in cluster_elements:
                if element[0] == 'T' and element[-3:] == 'txt':
                    trace_file = dir + "/" + element
                    replay_from_trace(trace_file, frame_rate, level, MAP_HEIGHT, MAP_WIDTH, small_fontzy, medium_fontzy, big_fontzy, num_directions, True, cluster.split('_____')[0])


def translate_percetor(perceptor_line, env):
    #obs: [dist_to_objective, dist_to_enemy, dist_to_coin, dist_to_cake, health, %coins, %kills]
    obs = []
    per = ast.literal_eval(perceptor_line)
    #dist_to_objective
    if per[-10][:-1] == 'inf':
        obs.append(int(env.observation_space.high[0]))
    #dist_to_enemy
    if per[0][:-1] == 'inf':
        obs.append(int(env.observation_space.high[1]))
    #dist_to_coin
    if per[2][:-1] == 'inf':
        obs.append(int(env.observation_space.high[2]))
    #dist_to_cake
    if per[1][:-1] == 'inf':
        obs.append(int(env.observation_space.high[3]))
    #health
    obs.append(int(per[-9][:-1]))
    #% of coins
    if env.map.number_of_coins != 0:
        obs.append(float(per[-8][:-1]) / env.map.number_of_coins)
    else:
        obs.append(1)
    #% of enemies
    if env.map.number_of_enemies != 0:
        obs.append(float(per[-7][:-1]) / env.map.number_of_enemies)
    else: 
        obs.append(1)
    
    return obs



level = 'Level1'
env = gym.make("FlowerHunter-v0", map_name = level)
env.reset()
#generate_trace_perceptor(level, 6)
line_test = "['inf_', 'inf_', 'inf_', '0_', '0_', '0_', '0_', '0_', '0_', '0_', '0_', '0_', '0_', '0_', '0_', 'inf_', '100_', '0_', '0_', '0_', '[[359, 359, 359, 339, 346, 369, 369, 359]]_', '[[0, 0, 0, 0, 0, 0, 0, 0]]_', '[[0, 0, 0, 0, 0, 0, 0, 0]]_', '[[0, 0, 0, 0, 0, 0, 0, 0]]_', '[[0, 0, 0, 0, 0, 0, 0, 0]]']"
print(translate_percetor(line_test, env))