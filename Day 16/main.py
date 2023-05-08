import copy
import time

def get_data():
    with open("data.txt", "r") as f:
        data = [i.split(", ") for i in f.read().replace("Valve ", "").replace(" has flow rate=", ", ").replace("; tunnels lead to valves ", ", ").replace("; tunnel leads to valve ", ", ").split("\n")]
        data = [[i[0], int(i[1]), i[2:]] for i in data]
    return data


class Node:
    def __init__(self, node_list):
        self.valve = node_list[0] # Node name
        self.open = False
        self.flow_rate = node_list[1]
        self.connections_strings = node_list[2]
        self.connected_nodes = []
        self.node_distances = {}

    def make_connections(self, nodes):
        for node_string in self.connections_strings:
            self.connected_nodes.append(nodes[node_string])
        return self

    def __repr__(self):
        #return str(self.valve)
        #return str("[" + self.valve + ", " + str(self.flow_rate) + ", " + str([i.valve for i in self.connected_nodes]) + "]")
        return str(self.open)


def dfs(current_node, end_nodes, current_distance = None, distances = None, visited = None):
    # Do recursive dfs from an initial node until an end node is found. Add end node to distances dictionary with distance from start node
    if current_distance is None:
        current_distance = 0
    if distances is None:
        distances = {i : float("inf") for i in end_nodes}
    if visited is None:
        visited = [current_node]
    else:
        visited.append(current_node)
    
    if current_node in end_nodes:
        if current_distance < distances[current_node] and not any([i in visited for i in end_nodes if i != current_node]):
            distances[current_node] = current_distance
    for node in current_node.connected_nodes:
        if node not in visited:
            distances = dfs(node, end_nodes, current_distance + 1, distances, copy.copy(visited))
    return distances


def add_pressure(pressure_total, time_used, non_zero_nodes_dict):
    #print(non_zero_nodes_dict)
    for node in non_zero_nodes_dict.values():
        if node.open:
            pressure_total += node.flow_rate * time_used
    #print(f"{time_used=}")
    #print(f"{pressure_total=}")
    return pressure_total


def recursive_traversal(current_node, non_zero_nodes_dict, time = None, pressure_total = None, max_pressure = None):
    #print(pressure_total, max_pressure)
    if time is None:
        time = 30
    if pressure_total is None:
        pressure_total = 0
    if max_pressure is None:
        max_pressure = 0
    if not current_node.open and current_node.flow_rate != 0: # Always open a node if it is not open.
        time -= 1
        pressure_total = add_pressure(pressure_total, 1, non_zero_nodes_dict)
        current_node.open = True
        non_zero_nodes_dict[current_node.valve].open = True

    for node in current_node.node_distances:
        #print(current_node.node_distances[node])
        if time - current_node.node_distances[node] > 0 and (not node.open or all([i.open for i in copy.deepcopy(current_node).node_distances])):
            max_pressure = recursive_traversal(copy.deepcopy(node), copy.deepcopy(non_zero_nodes_dict), time - current_node.node_distances[node], add_pressure(pressure_total, current_node.node_distances[node], non_zero_nodes_dict), max_pressure)
    if add_pressure(pressure_total, time, non_zero_nodes_dict) > max_pressure:
        max_pressure = add_pressure(pressure_total, time, non_zero_nodes_dict)
        #print(max_pressure)
    return max_pressure
        

def p2adjust(non_zero_nodes_dict):
    total = 0
    for node in non_zero_nodes_dict.values():
        if node.open:
            total += 26 * node.flow_rate
    return total


def recursive_traversal_p2(current_node, non_zero_nodes_dict, time = None, pressure_total = None, max_pressure = None, first_node = None):
    #print(pressure_total, max_pressure)
    if first_node is None:
        first_node = current_node
    if time is None:
        time = 26
    if pressure_total is None:
        pressure_total = 0
    if max_pressure is None:
        max_pressure = 0
    if not current_node.open and current_node.flow_rate != 0: # Always open a node if it is not open.
        time -= 1
        pressure_total = add_pressure(pressure_total, 1, non_zero_nodes_dict)
        current_node.open = True
        non_zero_nodes_dict[current_node.valve].open = True

    for node in current_node.node_distances:
        #print(current_node.node_distances[node])
        if time - current_node.node_distances[node] > 0 and (not node.open):
            max_pressure = recursive_traversal_p2(copy.deepcopy(node), copy.deepcopy(non_zero_nodes_dict), time - current_node.node_distances[node], add_pressure(pressure_total, current_node.node_distances[node], non_zero_nodes_dict), max_pressure, first_node)
    if add_pressure(pressure_total, time, non_zero_nodes_dict) > 1000:
        temp_final_pressure = add_pressure(pressure_total, time, non_zero_nodes_dict) + recursive_traversal(first_node, non_zero_nodes_dict, time = 26) - p2adjust(non_zero_nodes_dict)
        #print(f"{temp_final_pressure=}")
        if temp_final_pressure > max_pressure:
            max_pressure = temp_final_pressure
            #print(max_pressure)
    return max_pressure  


def main(): # Strategy: Find shortest paths between each node with a flow rate using DFS, make new (Weighted) graph with just these nodes and the starting node, do travelling salesman by hand on resulting graph?
    start_time = time.perf_counter()
    data = get_data()
    nodes_dict = {i[0] : Node(i) for i in data}
    #print(nodes_dict)
    nodes = [i for i in nodes_dict.values()]
    for i in nodes:
        i.make_connections(nodes_dict)

    non_zero_nodes = [i for i in nodes if i.flow_rate != 0]
    #print(nodes)
    #distances = dfs(nodes_dict["AA"], non_zero_nodes)
    #nodes_dict["AA"].node_distances = dfs(nodes_dict["AA"], non_zero_nodes)
    #print(nodes_dict["AA"].node_distances)
    for node in non_zero_nodes + [nodes_dict["AA"]]:
        node.node_distances = dfs(node, [i for i in non_zero_nodes if i != node])
        to_del = []
        for key in node.node_distances:
            if node.node_distances[key] == float("inf"):
                to_del.append(key)
        for key in to_del:
            del node.node_distances[key]
        #print(node.valve, node.flow_rate, node.node_distances)

    # Start with 30 minutes, time's up at 0
    current_node = nodes_dict["AA"]
    non_zero_nodes_dict = {i.valve:i for i in non_zero_nodes}
    max_pressure = recursive_traversal(current_node, non_zero_nodes_dict)
    print(f"Part 1: {max_pressure}")
    end_time = time.perf_counter()
    print(f"Part 1 time: {end_time - start_time} seconds")
    start_time = time.perf_counter()
    print("Warning: Part 2 takes about 45 seconds to finish running")
    max_pressure = recursive_traversal_p2(current_node, non_zero_nodes_dict)
    print(f"Part 2: {max_pressure}")
    end_time = time.perf_counter()
    print(f"Part 2 time: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
