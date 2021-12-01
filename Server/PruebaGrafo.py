from collections import deque 
from txt_to_graph import *

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

#print("Stars:\n", nodes_positions_stars, "\nDestinations:\n", destination_stars)

def google_maps_stars(position: tuple, destiny_position: tuple):

    starting_node = calculate_starting_node(position, graph, nodes_positions_stars, destination_stars, destiny_position)
    #print(f"The starting node for {position} is ")
    """
    try:
        #return nodes_positions_stars[starting_node][1]
        print(f"node star {nodes_positions_stars[starting_node][1]}")
    except:
        #return destination_stars[starting_node]
        print(f"node star {destination_stars[starting_node]}")"""

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
    
    #print("the destiny position star ", destination_stars[destiny_node_key])
    #print(f"Finding shortest path from {starting_node} to {destination_node_ind} in {graph_aux}")

    #print("graph aux", graph_aux)
    node_ind_shortest_path = find_shortest_path(graph_aux, starting_node, destiny_node_ind)
    
    print(f"Printing shortest path for node from {position} to {destiny_position}")
    if(node_ind_shortest_path != None):
        for node_ind in node_ind_shortest_path:
            try:
                #return nodes_positions_stars[starting_node][1]
                print(f"node star {nodes_positions_stars[node_ind][1]}")
            except:
                #return destination_stars[starting_node]
                print(f"node star {destination_stars[node_ind]}")
    else:
        print("Path not found")
    print("-----------------------------------------")

google_maps_stars((17, 10), (18, 14))


#google_maps_stars((8, 4), (2, 4))
#google_maps_stars((17, 4), (4, 10))
#google_maps_stars((6, 1), (13, 2))
#google_maps_stars((2, 1), (13, 15))
#google_maps_stars((17, 4), (13, 15))

#for i in range(4, 11):
#   google_maps_stars((17, i), (13, 15))

#google_maps_stars((17, 10), (13, 15))
#google_maps_stars((16, 12), (2, 4))
#google_maps_stars((24, 15), (23, 19))
#google_maps_stars((21, 1), (7, 22))
