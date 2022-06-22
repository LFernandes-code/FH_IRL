#read file X
#convert pos to player relative X
#create nodes
#A*
import math
import heapq
from unicodedata import name
from warnings import warn
import time

from gym_game.envs.flower_hunter import main

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1] 

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

    def a_star(self, start_position, end_position, max_iterations = 1000):
        # Create start and end node
        start_node = Node(None, start_position)
        end_node = Node(None, end_position)

        # Initialize both open and closed list
        frontier = []
        closed_list = []

        # Heapify the frontier and Add the start node
        heapq.heapify(frontier) 
        heapq.heappush(frontier, start_node)

        # Adding a stop condition
        outer_iterations = 0

        # Loop until you find the end
        while len(frontier) > 0:
            outer_iterations += 1

            if outer_iterations > max_iterations:
                # if we hit this point return the path such as it is
                # it will not contain the destination
                warn("giving up on pathfinding too many iterations")
                return return_path(current_node)    
            
            # Get the current node
            current_node = heapq.heappop(frontier)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                return return_path(current_node)

            # Generate children
            children = []
            adj_positions = self.get_neightbours(current_node.position)
            for position in adj_positions:
                # Create new node
                new_node = Node(current_node, position)
                # Append
                children.append(new_node)

            # Loop through children
            for child in children:
                # Child is on the closed list
                if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                    continue
                
                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = self.h(child.position, end_position)
                child.f = child.g + child.h

                # Child is already in the open list
                if len([open_node for open_node in frontier if child.position == open_node.position and child.g > open_node.g]) > 0:
                    continue

                # Add the child to the open list
                heapq.heappush(frontier, child)

        warn("Couldn't get a path to destination")
        return None

if __name__ == "__main__":
    start_time = time.time()
    map = Mem_Map('Level1')
    path = map.a_star((0,0), (21,1))
    print(path)
    print("--- %s seconds ---" % (time.time() - start_time))