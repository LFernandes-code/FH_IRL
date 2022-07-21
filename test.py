import sys
import numpy as np
import math
import random
import os

import gym
import gym_game

import time
from gym_game.envs.map_loader import * 

import matplotlib.pyplot as plt

MAP_HEIGHT = 600
MAP_WIDTH = 600


def save_location(location_file, save_name):

	f = open(location_file)

	output = f.readlines()


	x_list = []
	y_list = []

	for inpy in output:
		x_y = inpy.split("_")
		x_list.append(int(x_y[0]))
		y_list.append(-int(x_y[1].replace('\n','')))


	fig4 = plt.figure()
	ax4 = fig4.add_subplot(111)
	img = plt.imread("./Maps/back_map.png")

	ax4.imshow(img, extent=[-190, 2230, -960, 260])

	for i in range(len(x_list)):
		ax4.scatter(x_list[i], y_list[i], c = "blue", alpha=0.1)

	plt.axis('equal')


	plt.xlim([-200, 2200])
	plt.ylim([-1000, 200])
	fig_name = save_name
	fig4.savefig(fig_name)


def convert_position_to_cell(position):
    cell = tuple(map(lambda i: ((i + 10) / 5) // 4 , position))
    print(position)
    print(cell)
    return tuple(map(lambda i: ((i + 10) / 5) // 4 , position))

if __name__ == "__main__":
    level = "Level1"
    algs = [ "DB", "BC"] #"GAIL",
    
    for alg in algs:
        cluster_folder =  "Traces/" + alg
        cluster_traces = os.listdir(cluster_folder)
        for trace in cluster_traces:
            if trace[0] == 'G':
                tmp = trace.split('_')[-1]
                img = tmp.split('.')[0]
                save_location(cluster_folder + '/' + trace, cluster_folder + '/' +img)

