from gym_game.envs.flower_hunter import *
import os
import ast
from tqdm import tqdm

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

def process_perceptor_files(level, env, cluster_threshold):
    map_name = "Maps/" + level + ".csv"
    level_cluster =  "Clusters/" + level + "_clusters"
    level_clusters = os.listdir(level_cluster)
    dir = ""
    for cluster in tqdm(level_clusters):
        if int(cluster.split('_____')[1]) >= cluster_threshold:
            cluster_elements = os.listdir(level_cluster + "/" + cluster)
            dir = level_cluster + "/" + cluster
            for element in cluster_elements:
                if element[0] == 'P' and element[-3:] == 'txt':
                    file = open((dir + "/" + element),'r')
                    processed_file = open((dir + "/" + "A_" + element),'w')
                    for line in file.readlines():
                        data = env.observe_world(ast.literal_eval(line[:-1]))
                        processed_file.write(str(data))
                        processed_file.write("\n")



level = 'Level1'
env = gym.make("FlowerHunter-v0", map_name = level)
env.reset()
cluster_threshold = 6
#generate_trace_perceptor(level, cluster_threshold)
process_perceptor_files(level, env, cluster_threshold)