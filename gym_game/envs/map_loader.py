#read file X
#convert pos to player relative X
#create nodes
#A*

import collections
import math

class Mem_Map():
    def __init__(self, map_name):
        self.positions = self.load_map(map_name)

    def load_map(self, map_file):
        #open map file
        file_path = "Maps/" + map_file + ".csv"
        file = open(file_path, "r")
        lines = file.readlines()
        line_count = 0

        #temporary list
        _position_pairs = []
        #final position list
        reletavive_position_pairs = []
        player_position = ()
            
        for line in lines:
            line = line.replace('	', '')
            line = line.replace(';', '')
            column_count = 0
            for letter in line:
                if letter == '.':
                    _position_pairs.append((column_count,line_count))
                elif letter == "r":
                    _position_pairs.append((column_count,line_count))
                elif letter == "m":
                    _position_pairs.append((column_count,line_count))
                elif letter == "f":
                    _position_pairs.append((column_count,line_count))
                elif letter == 'p':
                    player_position = (column_count,line_count)
                    
                column_count += 1
            line_count += 1

        #changing postion to be relative to the player starting position
        for position in _position_pairs:
            relative_pos = tuple(map(lambda i, j: i - j, position, player_position))
            reletavive_position_pairs.append(relative_pos)
        reletavive_position_pairs.append((0,0))
        
        return reletavive_position_pairs

    def get_neightbours(self, position):
        (x,y) = position
        temp_neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1),(x+1, y+1),(x-1, y-1), (x+1, y-1), (x-1, y+1)]
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1),(x+1, y+1),(x-1, y-1), (x+1, y-1), (x-1, y+1)]
        for neighbor in temp_neighbors:
            if neighbor not in self.positions:
                neighbors.remove(neighbor)
        return neighbors
    
    def h(self, position, end_postion):
        (x1,y1) = position
        (x2,y2) = end_postion
        return math.fabs(x1 - x2) + math.fabs(y1 - y2)

    def a_star(start_position, end_position):
        pass

map = Mem_Map('Level1')