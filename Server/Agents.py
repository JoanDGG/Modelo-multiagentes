from mesa import Agent
from PruebaGrafo import *
import math

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, pos, destination):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.destination = destination
        self.direction = ["left"]
        self.pos = pos

        self.star_lists = google_maps_stars(coord2matrix(self.pos[0], self.pos[1], self.model.grid.height),
                                            coord2matrix(self.destination[0], self.destination[1], self.model.grid.height))
        print("with google maps, i know my intersections ", self.star_lists)
        for ind, star in enumerate(self.star_lists):
            self.star_lists[ind] = matrix2coord(star[0], star[1], self.model.grid.height)
        print("i flipped them ", self.star_lists)
        
        self.next_star = self.star_lists[0]
        self.arrived = False
        print(self.star_lists)


    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """

        # Check if actual cell is destination
        present_in_cell = self.model.grid.get_cell_list_contents([self.pos])
        destination_agent = [agent for agent in present_in_cell if isinstance(agent, Destination)]
        # Checar si es false cuando no hay
        if(destination_agent):
            # Dont move
            return

        neighbour_cells = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Moore neighborhood (including diagonals)
            include_center=True)
        
        # Get the road agent of actual cell
        # PENDIENTE: eliminar celdas que no son del carril opuesto
        road_agent = [agent for agent in present_in_cell if isinstance(agent, Road)]
        traffic_light_agent = [agent for agent in present_in_cell if isinstance(agent, Traffic_Light)]
        possible_steps = []
        if(len(road_agent) > 0):
            if("right" in road_agent[0].direction):
                possible_steps += [cell for cell in neighbour_cells if(cell[0] >= self.pos[0])]
            if("left" in road_agent[0].direction):
                possible_steps += [cell for cell in neighbour_cells if(cell[0] <= self.pos[0])]
            if("up" in road_agent[0].direction):
                possible_steps += [cell for cell in neighbour_cells if(cell[1] >= self.pos[1])]
            if("down" in road_agent[0].direction):
                possible_steps += [cell for cell in neighbour_cells if(cell[1] <= self.pos[1])]
        elif(len(traffic_light_agent) > 0):
            print(f"There is a traffic light, actual directions{self.direction}")
            if("right" in self.direction):
                possible_steps += [cell for cell in neighbour_cells if(cell[0] >= self.pos[0])]
            if("left" in self.direction):
                possible_steps += [cell for cell in neighbour_cells if(cell[0] <= self.pos[0])]
            if("up" in self.direction):
                possible_steps += [cell for cell in neighbour_cells if(cell[1] >= self.pos[1])]
            if("down" in self.direction):
                possible_steps += [cell for cell in neighbour_cells if(cell[1] <= self.pos[1])]
        print(possible_steps)
        #possible_steps.append(self.pos)

        if(self.destination in possible_steps):
            # Move to destination
            self.model.grid.move_agent(self, self.destination)
            self.arrived = True
        else:
            traffic_light_agent = [agent for agent in present_in_cell if isinstance(agent, Traffic_Light)]
            
            if(len(traffic_light_agent) > 0):
                if(not traffic_light_agent[0].state):
                    # Stop if red light
                    return
            elif(self.next_star in possible_steps):
                if(self.next_star != self.destination):
                    star_index = self.star_lists.index(self.next_star)
                    self.next_star = self.star_lists[star_index + 1]
                else:
                    self.arrived = True
            # Calculate cell_to_move:
            # Check which grid cells are empty

            # Calculate closest cell to next star
            cell_to_move = None
            empty_positions = []
            road_agents = []
            for i in range(0, len(possible_steps)):
                list_with_agent_in_cell = self.model.grid.get_cell_list_contents([possible_steps[i]])
                print(list_with_agent_in_cell)
                road_agent_in_cell = [agent for agent in list_with_agent_in_cell if isinstance(agent, Road)]
                traffic_light_agent_in_cell = [agent for agent in list_with_agent_in_cell if isinstance(agent, Traffic_Light)]
                # If theres an empty cell or will be empty
                if(len(road_agent_in_cell) > 0):
                    if not road_agent_in_cell[0].occupied_next:
                        empty_positions.append(possible_steps[i])
                        road_agents.append(road_agent_in_cell[0])
                elif(len(traffic_light_agent_in_cell) > 0):
                    if not traffic_light_agent_in_cell[0].occupied_next:
                        empty_positions.append(possible_steps[i])
                        road_agents.append(traffic_light_agent_in_cell[0])

            distance = math.inf
            index_min_distance = None
            for index, cell in enumerate(empty_positions):
                distance_from_cell = math.sqrt((cell[0] - self.next_star[0])**2+(cell[1] - self.next_star[1])**2)
                if(distance_from_cell < distance):
                    distance = distance_from_cell
                    index_min_distance = index

            if(isinstance(index_min_distance, int)):
                cell_to_move = empty_positions[index_min_distance]
                next_road_agent = road_agents[index_min_distance]
                
            if(cell_to_move):
                # Move to next_cell
                if(len(road_agent) > 0):
                    road_agent[0].occupied_next = False
                    self.direction = road_agent[0].direction
                elif(len(traffic_light_agent) > 0):
                    traffic_light_agent[0].occupied_next = False
                next_road_agent.occupied_next = True
                self.model.grid.move_agent(self, cell_to_move)
            else:
                print(f"El agente {self.unique_id} no se puede mover de {self.pos} a {cell_to_move}. No hay celdas vacias")

class Traffic_Light(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, state = False):
        super().__init__(unique_id, model)
        self.state = state
        self.occupied_next = False

    def step(self):
        pass

class Destination(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model, direction = ["left"]):
        super().__init__(unique_id, model)
        self.direction = direction # Añadir posibles direcciones desde codigo monstruo
        self.occupied_next = False

    def step(self):
        pass
