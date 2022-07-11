import gym
import seals
import gym_game
from imitation.data.types import TrajectoryWithRew
import numpy as np


env = gym.make("FlowerHunter-v0", map_name = "Level1")

#generate trajectories
traj = []
tr = TrajectoryWithRew([0,0],[1],None,terminal=True,rews=np.array([1.0]))
traj.append(tr)
print(traj)
print(type(traj))