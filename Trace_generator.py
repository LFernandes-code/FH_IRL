from gym_game.envs.flower_hunter import *
import os
import ast
from tqdm import tqdm

import gym_game
import gym

from imitation.data.types import TrajectoryWithRew
import numpy as np

def generate_trace_perceptor(level, cluster_threshold):
    map_name = "Maps/" + level + ".csv"
    level_cluster =  "Clusters/" + level + "_clusters"

    num_directions = 8
    frame_rate = 0.0

    pygame.init()
    big_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 62)
    medium_fontzy = pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 32)
    small_fontzy =  pygame.font.Font(os.path.join("Fonts", 'MacondoSwashCaps.ttf'), 24)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    level_clusters = os.listdir(level_cluster)
    dir = ""
    for cluster in level_clusters:
        if int(cluster.split('_____')[1]) >= cluster_threshold:
            cluster_elements = os.listdir(level_cluster + "/" + cluster)
            dir = level_cluster + "/" + cluster
            for element in cluster_elements:
                if element[0] == 'T' and element[-3:] == 'txt':
                    trace_file = dir + "/" + element
                    replay_from_trace(trace_file, frame_rate, level, SCREEN_HEIGHT, SCREEN_WIDTH, small_fontzy, medium_fontzy, big_fontzy, num_directions, True, cluster.split('_____')[0])

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
                    last_state = ""
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
                        last_state = str(data)
                        processed_file.write(str(data))
                        processed_file.write("||")
                        processed_file.write(str(ac))
                        processed_file.write("\n")
                    
                    processed_file.write(last_state)
                    processed_file.write("||")
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
"""
def evaluate_state(state):
    # State[dist_to_objective, dist_to_enemy, dist_to_coin, dist_to_cake, health, %coins, %kills]
    reward = 0
    if state[4] == 0:
        reward = 10000 - state[0]
    elif state[0] <= 30:
        reward = 10000 
    # add reward based of % coins collected
    reward += (state[-2]/10 * 1000)
    # add reward based of % enemies killed
    reward += (state[-1]/10 * 1000)
    return reward
"""
def generate_trajectories(cluster_id, cluster_folder, env, distance_value = 180):
    traj = []
    cluster_dir = "Clusters/" + cluster_folder + "/" + cluster_id
    cluster_files = os.listdir(cluster_dir)

    for file in cluster_files:
        if file[0] == 'A':
            trace_file = open((cluster_dir + "/" + file), "r")
            obs = []
            acts = []
            rews = []
            i = 0
            print(file)
            lines = trace_file.readlines()
            for line_id in range(len(lines) - 1):
                c_line = lines[line_id]
                n_line = lines[line_id + 1]
                c_state = ast.literal_eval(c_line.split('||')[0])
                n_state = ast.literal_eval(n_line.split('||')[0])
                state_list = [c_state]
                # analise action
                action = c_line.split('||')[1]
                action_ids = []
                if action[:-1] == '[]':
                    action_ids.append(len(env.available_actions) - 1)
                elif 'sw' in action:
                    action_ids.append(4)
                elif ',' in action:
                        #two actions
                        ac = ast.literal_eval(action[:-1])
                        action_ids.append(env.available_actions.index(ac[0]))
                        action_ids.append(env.available_actions.index(ac[1]))  
                        state_list.append(c_state)    
                else:
                    # one action
                    ac = action[:-1].replace('[','').replace(']','').replace("'",'')
                    action_ids.append(env.available_actions.index(ac))
               
                #check complex action
                min_dist = min(n_state[:4])
                if min_dist < distance_value:
                    min_index=n_state[:4].index(min_dist)
                    action_ids.clear()
                    state_list.clear()
                    action_ids.append(min_index + 5)
                    state_list.append(c_state)

                if line_id == len(lines) - 2:
                    obs.append(n_state)

                acts += action_ids
                obs += state_list
                for state in state_list:
                    rews.append(float(env.evaluate_state(state)))
            
            tr = TrajectoryWithRew(obs=obs,acts=acts,infos=None,terminal=True,rews=np.array(rews))
            traj.append(tr)

    return traj


def generate_action_sequences(cluster_id, cluster_folder, env, distance_value = 180):
    traj = []
    cluster_dir = "Clusters/" + cluster_folder + "/" + cluster_id
    cluster_files = os.listdir(cluster_dir)

    for file in cluster_files:
        if file[0] == 'A':
            trace_file = open((cluster_dir + "/" + file), "r")
            acts = []
            i = 0
            print(file)
            lines = trace_file.readlines()
            for line_id in range(len(lines) - 1):
                c_line = lines[line_id]
                n_line = lines[line_id + 1]
                c_state = ast.literal_eval(c_line.split('||')[0])
                n_state = ast.literal_eval(n_line.split('||')[0])
                # analise action
                action = c_line.split('||')[1]
                action_ids = []
                if action[:-1] == '[]':
                    action_ids.append(len(env.available_actions) - 1)
                elif 'sw' in action:
                    action_ids.append(4)
                elif ',' in action:
                        #two actions
                        print(action)
                        ac = ast.literal_eval(action[:-1])
                        action_ids.append(env.available_actions.index(ac[0]))
                        action_ids.append(env.available_actions.index(ac[1]))      
                else:
                    # one action
                    ac = action[:-1].replace('[','').replace(']','').replace("'",'')
                    action_ids.append(env.available_actions.index(ac))
                    
               
                #check complex action
                min_dist = min(n_state[:4])
                if min_dist < distance_value:
                    min_index=n_state[:4].index(min_dist)
                    action_ids.clear()
                    action_ids.append(min_index + 5)
            
                acts += action_ids
            
            traj.append(acts)

    return traj

if __name__ == "__main__":
    level = 'Level1'
    env = gym.make("FlowerHunter-v0", map_name = level)
    cluster_threshold = 6
    ac_plan = generate_trajectories("78_1", "Level1_clusters", env)
    #print(ac_plan)
    #generate_trace_perceptor(level, cluster_threshold)
    #process_perceptor_files(level, env, cluster_threshold)