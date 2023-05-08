import pygrille
from multiprocessing import Pool
import sys
from time import perf_counter
sys.setrecursionlimit(25000)

def get_data():
    with open("data.txt","r") as f:
        data = [[ord(i) for i in j] for j in [list(i) for i in f.read().split("\n")]]
    return data


around = [[1, 0], [-1, 0], [0, 1], [0, -1]]
PIXEL_SIZE = 5


class Node:
    def __init__(self, height, position, end_pos):
        self.pos = position
        self.heur = abs(end_pos[0] - position[0]) + abs(end_pos[1] - position[1])
        if height == ord("S"):
            height = ord("a")
        elif height == ord("E"):
            height = ord("z")
        self.height = height
        self.connections = []
        self.last_node = None
        self.distance_to = float("inf")

    def make_connections(self, node_grid):
        for direction in around:
            if 0 <= self.pos[0] + direction[0] < len(node_grid) and 0 <= self.pos[1] + direction[1] < len(node_grid[0]):
                if node_grid[self.pos[0] + direction[0]][self.pos[1] + direction[1]].height <= self.height + 1:
                    self.connections.append(node_grid[self.pos[0] + direction[0]][self.pos[1] + direction[1]])

    def __repr__(self):
        return str(self.pos)


def get_heur(item):
    return item[1].heur + item[0].distance_to


def a_star(node_grid, start_pos, end_pos, visualise):
    # Handle visualisation
    if visualise:
        pygrille_grid = pygrille.Grid(PIXEL_SIZE, [len(node_grid[0]),len(node_grid)], framerate = 60, default_colour = (66, 72, 245), border_width = 3)
        for row_num, row in enumerate(pygrille_grid):
            for pixel_num, pixel in enumerate(row):
                pixel.colour = [255 // (node_grid[pixel_num][row_num].height - 96) for _ in range(2)] + [0]
        pygrille_grid.draw()

    # Do A* algorithm
    visitable = ["temp_begin"]
    current_node = node_grid[start_pos[0]][start_pos[1]]
    current_node.distance_to = 0
    visited = []
    while current_node.pos != end_pos:
        if "temp_begin" in visitable:
            visitable = []
        visited.append(current_node)
        for connected_node in current_node.connections:
            if connected_node not in [i[1] for i in visitable] and connected_node not in visited:
                visitable.append([current_node, connected_node])
        visitable = sorted(visitable, key = get_heur)
        if len(visitable) == 0:
            return float("inf")
        current_node = visitable[0][1]
        current_node.last_node = visitable[0][0]
        current_node.distance_to = current_node.last_node.distance_to + 1
        visitable.pop(0)

    # Move backwards to work out final path
    connections = 0
    current_node = node_grid[end_pos[0]][end_pos[1]]
    while current_node.pos != start_pos:
        connections += 1
        current_node = current_node.last_node
        if visualise:
            pygrille_grid[current_node.pos[1]][current_node.pos[0]].colour = [(i+connections)%200 + 55 for i in (0, 0, 100)]
    if visualise:
        pygrille_grid.draw()
    return connections


def pool_a_star(start_pos):
    return(a_star(start_pos[0], start_pos[1], start_pos[2], start_pos[3]))


def main():
    time_start = perf_counter()
    visited = []
    data = get_data()
    start = ord("S")
    end = ord("E")
    for i in range(len(data)):
        if start in data[i]:
            start_pos = [i, data[i].index(start)]
        if end in data[i]:
            end_pos = [i, data[i].index(end)]
    node_grid = [[Node(data[line_num][place_num], [line_num, place_num], end_pos) for place_num in range(len(data[line_num]))] for line_num in range(len(data))]
    for line in node_grid:
        for item in line:
            item.make_connections(node_grid)
    print(f"Part 1: {a_star(node_grid, start_pos, end_pos, False)}")
    lowest_steps = float("inf")
    start_positions = []
    for line_num, line in enumerate(node_grid):
        for node_num, node in enumerate(line):
            if node.height == ord("a"):
                start_positions.append([node_grid, [line_num, node_num], end_pos, False])
                #temp_steps = a_star(node_grid, [line_num, node_num], end_pos, False)
                #if temp_steps < lowest_steps:
                    #lowest_steps = temp_steps
    with Pool() as p:
        answers = p.map(pool_a_star, start_positions)
    print(f"Part 2: {min(answers)}")
    time_stop = perf_counter()
    print("Elapsed time:", time_stop - time_start)
                
    
    
    


if __name__ == "__main__":
    main()
