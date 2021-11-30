from collections import deque 
from txt_to_graph import *

"""graph = {1: [2, 3],
         2: [],
         3: [4, 5, 11],
         4: [],
         5: [6, 7],
         6: [],
         7: [8],
         8: [9, 10, 16],
         9: [],
         10: [5, 11],
         11: [12, 13, 14],
         12: [],
         13: [1],
         14: [15, 22, 23, 24],
         15: [10, 16, 17],
         16: [],
         17: [18, 19],
         18: [],
         19: [20, 21, 22],
         20: [],
         21: [],
         22: [25],
         23: [],
         24: [],
         25: [26],
         26: [13, 14, 27],
         27: []}"""


def find_shortest_path(graph, start, end):

    dist = {start: [start]}
    q = deque([start])
    while len(q):
        at = q.popleft()  # at is index of node.
        for next in graph[at]:
            if next[0] not in dist:  # next[0] has the index not the direction
                dist[next[0]] = dist[at]+[next[0]]  # next[0] has the index not the direction
                q.append(next[0])  # next[0] has the index not the direction
    return dist.get(end)


def google_maps_stars(position: tuple, destiny_position: tuple):
    print("hello anyone home")

    starting_node = calculate_starting_node(position, graph, nodes_positions_stars, destination_stars)
    print(f"The starting node for {position} is {starting_node}")

    #try:
    #    return nodes_positions_stars[starting_node][1]
        #print(f"starting {nodes_positions_stars[starting_node][1]}")
    #except:
    #    return destination_stars[starting_node]
        #print(f"starting {destination_stars[starting_node]}")

    # Add empty lists to destination node indices.
    max_node_index = max(destination_stars)

    for i in range(max_node_index + 1):
        try:
            graph[i]
        except:
            graph[i] = []

    for destiny_node_key in destination_stars:
        if destination_stars[destiny_node_key] == destiny_position:
            destiny_node_ind = destiny_node_key 

    node_ind_shortest_path = find_shortest_path(graph, starting_node, destiny_node_ind)

    print(f"Printing shortest path for node from {position} to {destiny_position}")
    for node_ind in node_ind_shortest_path:
        try:
            #return nodes_positions_stars[starting_node][1]
            print(f"node star {nodes_positions_stars[node_ind][1]}")
        except:
            #return destination_stars[starting_node]
            print(f"node star {destination_stars[node_ind]}")

google_maps_stars((17, 4), (4, 10))
    





