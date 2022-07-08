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
                    #files
                    #perceptor file to read
                    perceptor_file = open((dir + "/" + element),'r')
                    #action file to read
                    action_file_location = "Traces_Actions_" + '_'.join(element.split('_')[4:])
                    action_file = open((dir + "/" + action_file_location),'r')
                    #file to write state-action pairs
                    processed_file = open((dir + "/" + "A_" + element),'w')

                    #read lines of files
                    perceptor_lines = perceptor_file.readlines()
                    action_lines = action_file.readlines()
                    #last actions that were executed
                    last_actions = []
            
                    for line_id in range(len(perceptor_lines)):
                        #read line with id to read the same line of both files
                        perceptor_data = perceptor_lines[line_id]
                        action_data = action_lines[line_id]
                        
                        #process the action acording to previus actions
                        ac = process_action(action_data[:-1], last_actions)
                        last_actions = ac
                        #convert perceptor file data to the enviroment values
                        data = env.observe_world(ast.literal_eval(perceptor_data[:-1]))

                        #write processed data
                        processed_file.write(str(data))
                        processed_file.write("||")
                        processed_file.write(str(ac))
                        processed_file.write("\n")

def process_action(action_line, last_actions):
    previous_actions = last_actions
    if action_line == "[]":
        return []
    else:
        if 'sw' in previous_actions:
            previous_actions.remove('sw')
        line_values = action_line[:-1].split(',')

        if len(line_values) == 1:
            return previous_actions
        else:
            actions = line_values[1:]
            for action in actions:
                p_action = action[1:]
                p_action = p_action.replace("'", "")
                if len(p_action) == 2:
                    if p_action[0] in previous_actions:
                        previous_actions.remove(p_action[0])
                    else:
                        previous_actions.append(p_action[0])
                else:
                    previous_actions.append('sw')
            
            return previous_actions

level = 'Level1'
env = gym.make("FlowerHunter-v0", map_name = level)
env.reset()
cluster_threshold = 6
#generate_trace_perceptor(level, cluster_threshold)
process_perceptor_files(level, env, cluster_threshold)