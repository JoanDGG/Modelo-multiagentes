
import os
import numpy as np
from numpy.lib.function_base import diff

with open("base.txt", "r") as file:
    lines_strings = file.readlines()  # Lista con renglones (strings)


def print_star_with_graph_ind(ind, nodes_positions_stars):
    print(nodes_positions_stars[ind][1], end=" ")


def calculate_starting_node(position: tuple, graph: dict, nodes_positions_stars: list, destination_stars: dict, destiny_position: tuple):
    #print("Graph:\n", graph)

    possible_startings = []

    car_rows, car_cols = position
    
    for graph_origin_node in graph:
        origin_node_positions_star = nodes_positions_stars[graph_origin_node]
        origin_node_positions = origin_node_positions_star[0]
        for origin_adj_node in graph[graph_origin_node]:
            try:
                origin_adj_node_ind = origin_adj_node[0]
                origin_adj_node_positions_star = nodes_positions_stars[origin_adj_node_ind]
                origin_adj_node_positions = origin_adj_node_positions_star[0]
                # Line to the right.
                # pos cols greater than origin smaller than destiny.
                if origin_adj_node[1] == "right":
                    if car_cols >= origin_node_positions[0][1] and car_cols <= origin_adj_node_positions[0][1]:
                        if (car_rows - origin_node_positions[0][0] in [0, 1]):
                            possible_startings += [origin_adj_node_ind]
                # Line to the left.
                # pos cols smaller than origin greater than destiny.
                elif origin_adj_node[1] == "left":
                    if car_cols <= origin_node_positions[0][1] and car_cols >= origin_adj_node_positions[0][1]:
                        if (car_rows - origin_node_positions[0][0] in [0, 1]):
                            possible_startings += [origin_adj_node_ind]
                # Line to up.
                # pos rows smaller than origin greater than destiny.
                elif origin_adj_node[1] == "up":
                    if car_rows <= origin_node_positions[0][0] and car_rows >= origin_adj_node_positions[0][0]:
                        if (car_cols - origin_node_positions[0][1]) in [0, 1]:
                            possible_startings += [origin_adj_node_ind]
                # Line to down.
                # pos rows greater then origin smaller than destiny
                elif origin_adj_node[1] == "down":
                    if car_rows >= origin_node_positions[0][0] and car_rows <= origin_adj_node_positions[0][0]:
                        if (car_cols - origin_node_positions[0][1]) in [0, 1]:
                            possible_startings += [origin_adj_node_ind]
            except:
                destiny_star_rows, destiny_star_cols = destination_stars[origin_adj_node_ind]
                # Line to the right.
                # pos cols greater than origin smaller than destiny.
                if origin_adj_node[1] == "right":
                    if car_cols >= origin_node_positions[0][1] and car_cols <= destiny_star_rows:
                        if (car_rows - origin_node_positions[0][0] in [0, 1]):
                            if destiny_star_rows == destiny_position[0] and destiny_star_cols == destiny_position[1]:
                                possible_startings += [origin_adj_node_ind]
                # Line to the left.
                # pos cols smaller than origin greater than destiny.
                elif origin_adj_node[1] == "left":
                    if car_cols <= origin_node_positions[0][1] and car_cols >= destiny_star_cols:
                        if (car_rows - origin_node_positions[0][0] in [0, 1]):
                            if destiny_star_rows == destiny_position[0] and destiny_star_cols == destiny_position[1]:
                                possible_startings += [origin_adj_node_ind]
                # Line to up.
                # pos rows smaller than origin greater than destiny.
                elif origin_adj_node[1] == "up":
                    if car_rows <= origin_node_positions[0][0] and car_rows >= destiny_star_rows:
                        if (car_cols - origin_node_positions[0][1]) in [0, 1]:
                            if destiny_star_rows == destiny_position[0] and destiny_star_cols == destiny_position[1]:
                                possible_startings += [origin_adj_node_ind]
                # Line to down.
                # pos rows greater then origin smaller than destiny
                elif origin_adj_node[1] == "down":
                    if car_rows >= origin_node_positions[0][0] and car_rows <= destiny_star_rows:
                        if (car_cols - origin_node_positions[0][1]) in [0, 1]:
                            if destiny_star_rows == destiny_position[0] and destiny_star_cols == destiny_position[1]:
                                possible_startings += [origin_adj_node_ind]

    #print("Los possible startings son ", possible_startings)
    
    min_starting_distance_ind = None
    min_starting_distance = np.inf
    for possible_starting_ind, possible_starting in enumerate(possible_startings):
        try:
            cols_diff = car_cols - nodes_positions_stars[possible_starting][1][1]
            rows_diff = car_rows - nodes_positions_stars[possible_starting][1][0]
        except:
            cols_diff = car_cols - destination_stars[possible_starting][1]
            rows_diff = car_rows - destination_stars[possible_starting][0]

        distance = np.sqrt((cols_diff ** 2) + (rows_diff ** 2))

        if distance < min_starting_distance:
            min_starting_distance_ind = possible_starting_ind
    
    if min_starting_distance_ind != None:
        return possible_startings[possible_starting_ind]
    

            

    

# Detection of intersections that have no traffic lights.
right_down_mask = np.array([[">", ">"], ["v", "v"]])

down_left_mask1 = np.array([["v", "v"], ["<", "<"]])
down_left_mask2 = np.array([["<", "v"], ["<", "v"]])

left_up_mask = np.array([["^", "<"], ["^", "<"]])

up_right_mask1 = np.array([[">", ">"], ["^", "^"]])
up_right_mask2 = np.array([["^", ">"], ["^", ">"]])

right_up_mask = np.array([["^", "^"], [">", ">"]])



"""DISCLAIMER ONLY USE PREVIOUS MASKS """

intersection_to_positions_stars = {">>vv": [((-1, 0),
                                            (-1, 1),
                                            (0, 0),
                                            (0, 1)),
                                            ((1, -1),
                                            (0, 0))],
 "vv<<": [((1, 0), (1, 1), (2, 0), (2, 1)), ((0, -1), (1, 0))],
 "<v<v": [((0, 1), (0, 2), (1, 1), (1, 2)), ((-1, 0), (0, 1))],
 "^<^<": [((0, -1), (0, 0), (1, -1), (1, 0)), ((-1, 1), (0, 0))],
 ">>^^": [((-1, 0), (-1, 1), (0, 0), (0, 1)), ((1, 2), (0, 1))],
 "^>^>": [((0, -1), (0, 0), (1, -1), (1, 0)), ((2, 1), (1, 0))],
 "^^>>": [((1, 0), (1, 1), (2, 0), (2, 1)), ((0, -1), (1, 0))]
}



masks = [right_down_mask, down_left_mask1, down_left_mask2,
         left_up_mask, up_right_mask1, up_right_mask2, right_up_mask]

lines_list_strings = []
for line in lines_strings:
    lines_list_strings += [list(line.replace("\n", ""))]

lines_np = np.array(lines_list_strings, dtype=str)
#print(lines_np)

lines_np_shape = lines_np.shape


nodes_positions_stars = []

for mask in masks:
    for i in range(lines_np_shape[0] - 1):  # Go through the rows.
        # Go through the columns.
        for j in range(lines_np_shape[1] - 1):
            #print(lines_np[i : i + 2, j : j + 2] == mask)
            if (lines_np[i : i + 2, j : j + 2] == mask).all():
                """ Revisamos que rodeando la mascara no haya s"""


                surrounding_positions = [(i - 1, j - 1),
                                         (i, j - 1),
                                         (i + 1, j - 1),
                                         (i + 2, j - 1,
                                         (i - 1, j),
                                         (i - 1, j + 1),
                                         (i - 1, j + 2),
                                         (i, j + 2),
                                         (i + 1, j + 2),
                                         (i + 2, j + 2),
                                         (i + 2, j + 1),
                                         (i + 2, j))]

                traffic_surrounding_intern_list = []
                for surr_pos in surrounding_positions:
                    if surr_pos[0] < lines_np_shape[0] and surr_pos[1] < lines_np_shape[1]:
                        if lines_np[surr_pos[0], surr_pos[1]] == "s" or lines_np[surr_pos[0], surr_pos[1]] == "S":
                            traffic_surrounding_intern_list.append(True)
                        else:
                            traffic_surrounding_intern_list.append(False)

                if True not in traffic_surrounding_intern_list:
                    """ Detectamos exitosamente las intersecciones que no 
                        tienen semáforo. """

                    node_position_star = []

                    intersection_string = (mask[0, 0] +
                                        mask[0, 1] +
                                        mask[1, 0] +
                                        mask[1, 1])

                    operations_positions_stars \
                        = intersection_to_positions_stars[
                            intersection_string]

                    intersection_positions = []

                    # operations to get positions
                    for operation_position in operations_positions_stars[0]:
                        intersection_positions.append((i + operation_position[0],
                                                    j + operation_position[1]))

                    node_position_star.append(intersection_positions)

                    preferable_star_position = (i + operations_positions_stars[1][0][0],
                                                j + operations_positions_stars[1][0][1])

                    second_star_position = (i + operations_positions_stars[1][1][0],
                                            j + operations_positions_stars[1][1][1])          

                    #print(lines_np[preferable_star_position[0], preferable_star_position[1]])
                    if lines_np[preferable_star_position[0], preferable_star_position[1]] == "D":
                        star_position = second_star_position
                    else:
                        star_position = preferable_star_position

                    node_position_star.append(star_position)
                    nodes_positions_stars.append(node_position_star)

#print("nodes stars found with no lights")
for node_ind, node_position_star in enumerate(nodes_positions_stars):
    #print(node_position_star[1])
    no_lights_ind = node_ind

#print("nodes no traffic light", len(nodes_positions_stars))

"""DISCLAIMER CREATE BLOCKS OF AT LEAST 6"""

# Detection of intersections with traffic lights.

s_positions = []

for i in range(lines_np_shape[0]):
    for j in range(lines_np_shape[1]):
        character = lines_np[i, j]
        if character == "s" or character == "S":
            character_part_of_other = False
            for s_position in s_positions:
                diff_rows = np.abs(s_position[0] - i)
                diff_cols = np.abs(s_position[1] - j)
                #print(f"diff rows {diff_rows} diff cols {diff_cols}")
                if diff_rows + diff_cols <= 4:
                    character_part_of_other = True
                    break
            if not character_part_of_other:
                s_positions.append((i, j))


""" DISCLAIMER DESTINATIONS CANNOT BE IN TRAFFIC LIGHT INTERSECTION"""
""" DISCLAIMER DESTINATIONS CANNOT BE IN TRAFFIC LIGHT POSITION"""
# Figuring out star positions.
for s_position in s_positions:
    #print(f"s position {s_position}")
    left = (s_position[0], s_position[1] - 1)
    right = (s_position[0], s_position[1] + 1)

    node_position_star = []

    if lines_np[left] == ">" or lines_np[right] == ">":
        # Add the 4 positions of the intersection.
        intersection_positions = [(s_position[0], s_position[1] + 1),
                                  (s_position[0], s_position[1] + 2),
                                  (s_position[0] + 1, s_position[1] + 1),
                                  (s_position[0] + 1, s_position[1] + 2)]

        star_position = (s_position[0] + 1, s_position[1] + 2)

    elif lines_np[left] == "<" or lines_np[right] == "<":
        intersection_positions = [(s_position[0], s_position[1] - 2),
                                  (s_position[0], s_position[1] - 1),
                                  (s_position[0] + 1, s_position[1] - 2),
                                  (s_position[0] + 1, s_position[1] - 1)]

        star_position = (s_position[0], s_position[1] - 1)

    elif lines_np[left] == "#" or lines_np[right] == "#":
        s_to_left_pos = (s_position[0] + 1, s_position[1] - 1)
        s_to_right_pos = (s_position[0] + 1, s_position[1] + 2)  # There's two SS when traffic light on vertical road.

        intersection_positions = [(s_position[0] + 1, s_position[1]),
                                  (s_position[0] + 2, s_position[1]),
                                  (s_position[0] + 1, s_position[1] + 1),
                                  (s_position[0] + 2, s_position[1] + 1)]


        if s_to_left_pos[0] < lines_np_shape[0] and s_to_left_pos[1] < lines_np_shape[1]:
            if lines_np[s_to_left_pos[0], s_to_left_pos[1]] == "s" or lines_np[s_to_left_pos[0], s_to_left_pos[1]] == "S":
                #print("s to the left")
                star_position = (s_position[0] + 2, s_position[1])

        if s_to_right_pos[0] < lines_np_shape[0] and s_to_right_pos[1] < lines_np_shape[1]:
            if lines_np[s_to_right_pos[0], s_to_right_pos[1]] == "s" or lines_np[s_to_right_pos[0], s_to_right_pos[1]] == "S":
                #print("s to the right")
                star_position = (s_position[0] + 1, s_position[1])

    node_position_star.append(intersection_positions)
    node_position_star.append(star_position)

    nodes_positions_stars.append(node_position_star)

#print("nodes stars lights")
for i in range(no_lights_ind + 1, len(nodes_positions_stars)):
    pass#print(nodes_positions_stars[i][1])

destination_stars = {}
beginning_ind_for_d_node = len(nodes_positions_stars)
for i in range(lines_np_shape[0]):
    for j in range(lines_np_shape[1]):
        if np.all(lines_np[i][j] == "D"):
            destination_stars[beginning_ind_for_d_node] = (i, j)
            beginning_ind_for_d_node += 1
#print("nodes destinations stars")
#print(destination_stars)


#graph_adj_list = [["v", ">", 0, "^"]]
graph = {}

for node_ind, node in enumerate(nodes_positions_stars):
    representative = node[0][0]
    node_destiny: int
    graph[node_ind] = []
    nodes_to_right = []
    nodes_to_left = []
    nodes_to_up = []
    nodes_to_down = []

    # Make chosen nodes None so that they can be chosen again
    node_to_right = None
    node_to_left = None
    node_to_up = None
    node_to_down = None

    for node2_index, node2 in enumerate(nodes_positions_stars):
        # Misma fila distinta columna.
        if node2[0][0][0] == representative[0] and node2[0][0][1] != representative[1]:

            node_positions = node[0]
            col_max_from_node_pos = max([pos[1] for pos in node_positions])
            row_min_from_node_pos = min([pos[0] for pos in node_positions])
            """if node[1] == (8, 8):
                print(row_min_from_node_pos, col_max_from_node_pos)"""
            
            direction_to_review = (node2[0][0][1] - representative[1]) / np.abs(node2[0][0][1] - representative[1]) 
            """if node[1] == (8, 8):
                print("destiny star at ", node2[1])
                print(direction_to_review)"""

            start_row = row_min_from_node_pos
            end_row = row_min_from_node_pos + 2
            start_col = int(col_max_from_node_pos + 1 * direction_to_review)
            end_col = int(col_max_from_node_pos + 4 * direction_to_review)
            step = int(direction_to_review)

            """if node[1] == (8, 8):
                print("start row ", start_row)
                print("end row ", end_row)
                print("start_col ", start_col)
                print("end_col ", end_col)
                print(lines_np[start_row : end_row : 1, start_col : end_col : step])         
                print(lines_np[8 : 10 : 1, start_col : end_col : step])
                #print(block_review_right)"""

            block_to_review = lines_np[start_row : end_row : 1, start_col : end_col : step]

            block_review_left = block_to_review == "<"
            block_review_right = block_to_review == ">"

            #print("Reviewing node star ", node2[1], "block \n", block_to_review)
            #print("Reviewing node star ", node2[1], "block lefts\n", block_review_left)
            #print("Reviewing node star ", node2[1], "block rights\n", block_review_right)
            

            if np.any(block_review_right):
                if node2[0][0][1] > representative[1]:
                    nodes_to_right.append(node2_index)


            elif np.any(block_review_left):
                if node2[0][0][1] < representative[1]:
                    nodes_to_left.append(node2_index)

    #print("node star ", node[1], "nodes to right ", nodes_to_right)
    #print("node star ", node[1], "nodes to left ", nodes_to_left)

    # We use the up left to calculate distances and other things.
    distances_to_right_nodes = [np.abs(nodes_positions_stars[node_to_right][0][0][1] - representative[1]) for node_to_right in nodes_to_right]

    #print("distances to right nodes are ", distances_to_right_nodes)

    distances_to_left_nodes = [np.abs(nodes_positions_stars[node_to_left][0][0][1] - representative[1]) for node_to_left in nodes_to_left]

    #print("distances to left nodes are ", distances_to_left_nodes)

    #quit()
    min_distance_right = np.Inf
    min_distance_left = np.Inf

    for i in range(len(distances_to_right_nodes)):
        if distances_to_right_nodes[i] < min_distance_right:
            node_to_right = nodes_to_right[i]
            min_distance_right = distances_to_right_nodes[i]

    if node_to_right != None:  # We know that node_destiny might not exist
        graph[node_ind].append([node_to_right, "right"])

        #  CHeck to add destinations.
        for destination_node_ind in destination_stars:
            dest_row, dest_col = destination_stars[destination_node_ind]
            # Destination in intersection.
            """if node[1] == (2, 2):
                print("destination ", dest_row, dest_col)
                print("intersection positions ", node[0])
                print("representative col ", representative[1])
                print("destiny col ", node2[0][0][1])
                print("d col between origin node2 cols ", dest_col > representative[1] and dest_col < node2[0][0][1]) 
                print("row difference between destiny and repr row", (dest_row - representative[0]))
                print("belongs to this node ", (dest_row - representative[0]) in [-1, 0, 1, 2])
                print()"""
            if (dest_row, dest_col) in node[0]:
                graph[node_ind].append([destination_node_ind, "right"])

            # col greater than origin col, smaller than destiny node col
            # Row is upwards max 1 or downwards max 2
            elif dest_col > node[0][0][1] and dest_col < nodes_positions_stars[node_to_right][0][0][1]:
                if (dest_row - node[0][0][0]) in [-1, 0, 1, 2]:
                    graph[node_ind].append([destination_node_ind, "right"])

    for i in range(len(distances_to_left_nodes)):
        if distances_to_left_nodes[i] < min_distance_left:
            node_to_left = nodes_to_left[i]
            min_distance_left = distances_to_left_nodes[i]

    if node_to_left != None:  # We know that node_destiny might not exist
        graph[node_ind].append([node_to_left, "left"])
        #  CHeck to add destinations.
        for destination_node_ind in destination_stars:
            dest_row, dest_col = destination_stars[destination_node_ind]
            # Destination in intersection.
        
            if (dest_row, dest_col) in node[0]:
                graph[node_ind].append([destination_node_ind, "left"])

            # col smaller than origin col, greater than destiny node col
            # Row is upwards max 1 or downwards max 2
            elif dest_col < node[0][0][1] and dest_col > nodes_positions_stars[node_to_left][0][0][1]:
                if (dest_row - node[0][0][0]) in [-1, 0, 1, 2]:
                    graph[node_ind].append([destination_node_ind, "left"])



    for node2_index, node2 in enumerate(nodes_positions_stars):
        # Misma columna distinta fila.
        if node2[0][0][1] == representative[1] and node2[0][0][0] != representative[0]:
            node_positions = node[0]
            col_min_from_node_pos = min([pos[1] for pos in node_positions])
            row_max_from_node_pos = max([pos[0] for pos in node_positions])
            
            direction_to_review = (node2[0][0][0] - representative[0]) / np.abs(node2[0][0][0] - representative[0]) 

            start_row = int(row_max_from_node_pos + 1 * direction_to_review)
            end_row = int(row_max_from_node_pos + 4 * direction_to_review)
            start_col = col_min_from_node_pos
            end_col = col_min_from_node_pos + 2
            step = int(direction_to_review)

            block_to_review = lines_np[start_row : end_row : step, start_col : end_col : 1]

            block_review_up = block_to_review == "^"
            block_review_down = block_to_review == "v"            

            if np.any(block_review_down):
                if node2[0][0][0] > representative[0]:
                    nodes_to_down.append(node2_index)

            elif np.any(block_review_up):
                if node2[0][0][0] < representative[0]:
                    nodes_to_up.append(node2_index)

    # We use the up left to calculate distances and other things.
    distances_to_up_nodes = [np.abs(nodes_positions_stars[node_to_up][0][0][0] - representative[0]) for node_to_up in nodes_to_up]
    
    distances_to_down_nodes = [np.abs(nodes_positions_stars[node_to_down][0][0][0] - representative[0]) for node_to_down in nodes_to_down]


    min_distance_up = np.Inf
    min_distance_down = np.Inf

    for i in range(len(distances_to_up_nodes)):
        if distances_to_up_nodes[i] < min_distance_up:
            node_to_up = nodes_to_up[i]
            min_distance_up = distances_to_up_nodes[i]

    if node_to_up != None:  # We know that node_destiny might not exist
        graph[node_ind].append([node_to_up, "up"])

        #  CHeck to add destinations.
        for destination_node_ind in destination_stars:
            dest_row, dest_col = destination_stars[destination_node_ind]
            # Destination in intersection.
        
            if (dest_row, dest_col) in node[0]:
                graph[node_ind].append([destination_node_ind, "up"])

            # row smaller than origin row, greater than destiny node row
            # col is left max 1 or right max 2
            elif dest_row < node[0][0][0] and dest_row > nodes_positions_stars[node_to_up][0][0][0]:
                if (dest_col - node[0][0][1]) in [-1, 0, 1, 2]:
                    graph[node_ind].append([destination_node_ind, "up"])


    for i in range(len(distances_to_down_nodes)):
        if distances_to_down_nodes[i] < min_distance_down:
            #print("old down min is ", min_distance_down)
            #print("new one is ", distances_to_down_nodes[i])
            node_to_down = nodes_to_down[i]
            min_distance_down = distances_to_down_nodes[i]
    #print("node to down is", node_to_down)
    if node_to_down != None:  # We know that node_destiny might not exist
       #print("node to down is", nodes_positions_stars[node_to_down][1])
        graph[node_ind].append([node_to_down, "down"])
        
        #  CHeck to add destinations.
        for destination_node_ind in destination_stars:
            dest_row, dest_col = destination_stars[destination_node_ind]
            # Destination in intersection.
        
            if (dest_row, dest_col) in node[0]:
                graph[node_ind].append([destination_node_ind, "down"])

            # row greater than origin row, smaller than destiny node row
            # col is left max 1 or right max 2
            elif dest_row > node[0][0][0] and dest_row < nodes_positions_stars[node_to_down][0][0][0]:
                if (dest_col - node[0][0][1]) in [-1, 0, 1, 2]:
                    graph[node_ind].append([destination_node_ind, "down"])


    """
    print("for node star ", node[1], " up down right left nodes are")

    for node_to_upf in nodes_to_up:
        print_star_with_graph_ind(node_to_upf, nodes_positions_stars)
    print()
    for node_to_downf in nodes_to_down:
        print_star_with_graph_ind(node_to_downf, nodes_positions_stars)
    print()
    for node_to_rightf in nodes_to_right:
        print_star_with_graph_ind(node_to_rightf, nodes_positions_stars)
    print()
    for node_to_leftf in nodes_to_left:
        print_star_with_graph_ind(node_to_leftf, nodes_positions_stars)
    print()

    print("distances are: ")
    print("up: ", distances_to_up_nodes)
    print("down: ", distances_to_down_nodes)
    print("right: ", distances_to_right_nodes)
    print("left: ", distances_to_left_nodes)

    print("chosen ones are")
    try:
        print("up: ", nodes_positions_stars[node_to_up][1])
    except:
        pass
    
    try:
        print("right: ", nodes_positions_stars[node_to_right][1])
    except:
        pass

    try:
        print("left: ", nodes_positions_stars[node_to_left][1])
    except:
        pass

    try:
        print("down: ", nodes_positions_stars[node_to_down][1])
    except:
        pass
    print("\n\n")"""

"""
for key in graph:
    print(f"Nodo {nodes_positions_stars[key][1]}")
    for adj_list in graph[key]:
        try:
            print(f"hacia {nodes_positions_stars[adj_list[0]][1]}")
        except:
            print(f"hacia {destination_stars[adj_list[0]]}")
    print()
"""

