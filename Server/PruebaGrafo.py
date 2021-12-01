from collections import deque 
from txt_to_graph import *

def find_shortest_path(graph, start, end):
    dist = {start: [start]}
    q = deque([start])
    while len(q):
        at = q.popleft()  # at is index of node.
        """print(at)
        try:
            #return nodes_positions_stars[starting_node][1]
            print(f"node star {nodes_positions_stars[at][1]}")
        except:
            #return destination_stars[starting_node]
            print(f"node star {destination_stars[at]}")"""
        for next in graph[at]:
            if next[0] not in dist:  # next[0] has the index not the direction
                dist[next[0]] = dist[at]+[next[0]]  # next[0] has the index not the direction
                q.append(next[0])  # next[0] has the index not the direction
    return dist.get(end)

#print("Stars:\n", nodes_positions_stars, "\nDestinations:\n", destination_stars)

def google_maps_stars(position: tuple, destiny_position: tuple):

    starting_node = calculate_starting_node(position, graph, nodes_positions_stars, destination_stars, destiny_position)
    print(f"The starting node for {position} is {starting_node}")
    
    try:
        #return nodes_positions_stars[starting_node][1]
        print(f"node star {nodes_positions_stars[starting_node][1]}")
    except:
        #return destination_stars[starting_node]
        print(f"node star {destination_stars[starting_node]}")

    graph_aux = graph.copy()
    max_node_index = max(destination_stars)
    
    for i in range(max_node_index + 1):
        try:
            graph_aux[i]
        except:
            graph_aux[i] = []

    for destiny_node_key in destination_stars:
        if destination_stars[destiny_node_key] == destiny_position:
            #print(destination_stars[destiny_node_key], "==", destiny_position)
            destiny_node_ind = destiny_node_key
            break
    
    print("the destiny position star ", destination_stars[destiny_node_key])
    #print(f"Finding shortest path from {starting_node} to {destination_node_ind} in {graph_aux}")

    #print("graph aux", graph_aux)
    node_ind_shortest_path = find_shortest_path(graph_aux, starting_node, destiny_node_ind)
    stars_list = []
    print(f"Printing shortest path for node from {position} to {destiny_position}")
    if(node_ind_shortest_path != None):
        for node_ind in node_ind_shortest_path:
            try:
                #return nodes_positions_stars[starting_node][1]
                stars_list.append(nodes_positions_stars[node_ind][1])
                print(f"node star {nodes_positions_stars[node_ind][1]}")
            except:
                #return destination_stars[starting_node]
                stars_list.append(destination_stars[node_ind])
                print(f"node star {destination_stars[node_ind]}")
    else:
        print("Path not found")
    #print("-----------------------------------------")
    return stars_list

def intersection_directions():
    inter_position_to_dirs = {}
    #print(nodes_positions_stars)
    for node_position_star_ind, node_position_star in enumerate(nodes_positions_stars):
        #print(node_position_star[1])
        directions = set()
        for outlink in graph[node_position_star_ind]:
            directions.add(outlink[1])
        for inter_position in node_position_star[0]:
            inter_position_to_dirs[(inter_position[1], inter_position[0])] = list(directions)

    return inter_position_to_dirs

inters_positions_to_dirs = intersection_directions()

def matrix2coord(row, col, height):
    return(col, height - row - 1)

def coord2matrix(x, y, height):
    return(height - y - 1, x)