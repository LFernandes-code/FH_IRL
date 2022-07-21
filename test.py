import sys
import numpy as np
import math
import random

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
    file = open("Traces/Gym_Bot_Position_Level1_21-07-2022_08-38-44_185_GAIL15.txt", "r")
    save_location("Traces/Gym_Bot_Position_Level1_21-07-2022_08-38-44_185_GAIL15.txt", "GAIL15")
