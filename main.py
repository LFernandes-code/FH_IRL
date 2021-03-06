from shutil import register_unpack_format
import sys
import pickle

import gym
import gym_game
from stable_baselines3.common import base_class
import imitation

class IRL_Agent():
    #base_class.BasePolicy
    def __init__(self, irl_alg, cluster):
        self.policy = self.load_policy(irl_alg, cluster)

    def load_policy(self, irl_alg, cluster):
        irl_cluster_file = "IRL/" + irl_alg + "_" + cluster + ".pl"

        with open(irl_cluster_file, 'rb') as f:
            policy =  pickle.load(f)
            return policy

    def select_action(self, obs):
        return self.policy.predict(obs)

def test_all_clusters():
    clusters = ["10_____29","15_____8","9_____12","5_____10","2_____10"]
    for cluster in clusters:
        agent = IRL_Agent("BC", cluster)
        env = gym.make("FlowerHunter-v0", map_name = "Level1")
        obs = env.reset()
        done = False

        act = agent.select_action(obs)[0]
        max_steps = 4000
        current_step = 0
        while not done:
            print(current_step)
            obs, _, done,_ = env.step(act)
            act = agent.select_action(obs)[0]

            current_step += 1
            if current_step >= max_steps:
                print("Max step reached")
                done = True
                env.write_trace()
        
        print("done: ", cluster)

def test_specific_cluster(cluster, alg, level):
    
    agent = IRL_Agent(alg, cluster)
    env = gym.make("FlowerHunter-v0", map_name = level)
    obs = env.reset()
    done = False

    act = agent.select_action(obs)[0]
    max_steps = 4000
    current_step = 0
    while not done:
        print(current_step)
        obs, _, done,_ = env.step(act)
        act = agent.select_action(obs)[0]

        current_step += 1
        if current_step >= max_steps:
            print("Max step reached")
            done = True
            env.write_trace()
    
    print("done: ", cluster)

if __name__ == "__main__":
    test_specific_cluster("15_____8","GAIL","Level1")
    