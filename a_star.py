# MaxieLife

import heapq
# import math
import csv

nodes_file = "nodes.csv"
def astar(adj_list, source, destination, num_iterations):
    def euclidean_distance(node1, node2):
        # euclidean heuristic
        x1, y1 = node1
        x2, y2 = node2
        return (x1 - x2) ** 2 + (y1 - y2) ** 2
               # omitted sqrt to save on time and space complexity since we don`t need an actual distance
               # math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # read node coordinates from nodes.csv
    node_coordinates = {}
    with open(nodes_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            node_id = int(row['node_id'])
            x, y = float(row['x']), float(row['y'])
            node_coordinates[node_id] = (x, y)

    # priority queue for open list
    open_list = []

    # set to store explored nodes
    explored_nodes = set()

    # dictionary to store parent info
    parent = {}

    # dictionary to store g-values
    g_values = {node: float('inf') for node in adj_list}

    # initialize starting node
    g_values[source] = 0
    f_value = g_values[source] + euclidean_distance(node_coordinates[source], node_coordinates[destination])

    # add starting node to open list
    heapq.heappush(open_list, (f_value, source))

    iterations = 0

    while open_list and iterations < num_iterations * 150:
        iterations += 1

        # pop node with the smallest f-value from open list
        current_f, current_node = heapq.heappop(open_list)

        # mark the current node as explored
        explored_nodes.add(current_node)

        # if destination is reached, reconstruct and return path
        if current_node == destination:
            path = [destination]
            while destination in parent:
                destination = parent[destination]
                path.append(destination)
            return path[::-1]

        # explore neighbors of the current node
        for neighbor, weight in adj_list[current_node].items():
            # calculate tentative g-value
            tentative_g = g_values[current_node] + euclidean_distance(node_coordinates[neighbor], node_coordinates[destination])

            # if the tentative g-value is better, update the information
            if tentative_g < g_values[neighbor]:
                g_values[neighbor] = tentative_g
                f_value = tentative_g + euclidean_distance(node_coordinates[neighbor], node_coordinates[destination])

                # add to open list if not already there
                if neighbor not in explored_nodes:
                    heapq.heappush(open_list, (f_value, neighbor))

                # update parent information
                parent[neighbor] = current_node

    # return list of explored nodes after N number of iterations (if path was not found)
    print(list(explored_nodes))
    return list(explored_nodes)