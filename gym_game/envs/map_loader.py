#read file X
#convert pos to player relative X
#create nodes
#A*
import math
import heapq
from unicodedata import name
from warnings import warn
import time
import matplotlib.pyplot as plt

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent = None, position = None, action = None):
        self.parent = parent
        self.position = position
        self.action = action

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
        path.append(current.action)
        current = current.parent
    final_path = path[::-1] 
    return final_path[1:]
"""
def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1] 
"""

class Mem_Map():
    def __init__(self, map_name):
        self.start_player_position = (0,0)
        self.start_player_cell = (0,0)

        #number of items
        self.number_of_coins = 0
        self.number_of_enemies = 0
        self.number_of_cakes = 0

        self.positions = self.load_map(map_name)

    def load_map(self, map_file):
        #open map file
        file_path = "Maps/" + map_file + ".csv"
        file = open(file_path, "r")
        lines = file.readlines()
        sprite_size = 20

        #temporary list
        _position_pairs = []
        #final position list
        reletavive_position_pairs = []
       
        line_count = 0
        for line in lines:
            column_count = 0
            
            line = line.replace('	', '')
            line = line.replace(';', '')
            
            for letter in line:
                if letter == '.':
                    _position_pairs.append((column_count,line_count))
                elif letter == '0':
                    _position_pairs.append((column_count,line_count))
                    #end_pos = (column_count,line_count)
                elif letter == "r":
                    _position_pairs.append((column_count,line_count))
                    self.number_of_cakes += 1
                elif letter == "m":
                    _position_pairs.append((column_count,line_count))
                    self.number_of_coins += 1
                elif letter == "f":
                    _position_pairs.append((column_count,line_count))
                    self.number_of_enemies += 1
                elif letter == 'p':
                    self.start_player_cell = (column_count,line_count)
                    self.start_player_position = (column_count * sprite_size ,line_count * sprite_size)
                    
                column_count += 1
            line_count += 1
        #changing postion to be relative to the player starting position
        for position in _position_pairs:
            relative_pos = tuple(map(lambda i, j: i - j, position, self.start_player_cell))
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

    def draw_map(self):
        x,y = map(list, zip(*self.positions))
        plt.scatter(x, y, c="red", alpha=0.5)
        plt.show()
    
    def draw_path(self, path, star_position):
        x,y = map(list, zip(*self.positions))
        x2 = [star_position[0]]
        y2 = [star_position[1]]
        position_x = star_position[0]
        position_y = star_position[1]
        for action in path:
            position_x = position_x + action[0]
            position_y = position_y + action[1]
            x2.append(position_x)
            y2.append(position_y)
         
        plt.scatter(x, y, c='b', alpha=0.5)
        plt.scatter(x2, y2, c='r', alpha=1)
        plt.show()

    def a_star(self, start_position, end_position, max_iterations = 2000):
        if type(start_position[0]) == float:
            start_position = tuple(map(int, start_position))
        
        if type(end_position[0]) == float:
            end_position = tuple(map(int, end_position))
            
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
                node_Action = tuple(map(lambda i, j: i - j, position, current_node.position))
                new_node = Node(current_node, position, node_Action)
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
    Map = Mem_Map('Level1')
    path = Map.a_star((0,0), (102.0, 43.0))
    #print(path)
    Map.draw_path(path, (0,0))
    print("--- %s seconds ---" % (time.time() - start_time))