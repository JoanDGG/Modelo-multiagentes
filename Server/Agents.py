# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python mesa back-end for agents. Based on the code provided by Octavio Navarro.
# Last modified 2 December 2021

from mesa import Agent
from PruebaGrafo import *
import math

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        arrived: Check if agent has arrived the destination
        destination: Final position that the agent wants to get to
        directions: List of possible directions the car can go (updated with directions from road)
        stars_list: List of key positions in the grid for best path to destination
        next_star: Closest key position of the path
        pos: Current agent's position
        previous_20_pos: List of previous 20 positions of the agent
    """
    def __init__(self, unique_id: int, model, pos: tuple, destination: tuple):
        """
        Creates a new car agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            pos: Agent's original position
            destination: Agent's destination position
        """
        super().__init__(unique_id, model)
        self.destination = destination
        self.directions = ["left"]
        self.pos = pos
        self.previous_20_pos = []

        self.stars_list = google_maps_stars(coord2matrix(self.pos[0], self.pos[1], self.model.grid.height),
                                            coord2matrix(self.destination[0], self.destination[1], self.model.grid.height))
        for ind, star in enumerate(self.stars_list):
            self.stars_list[ind] = matrix2coord(star[0], star[1], self.model.grid.height)
        
        self.next_star = self.stars_list[0]
        self.arrived = False

    def step(self):
        """ 
        Determines the action for the next step according to the agent's behaviour
        """
        agents_in_current_cell = self.model.grid.get_cell_list_contents([self.pos])
        # Check if car is in a destination cell
        destination_agent = [agent for agent in agents_in_current_cell if isinstance(agent, Destination)]
        if(len(destination_agent) > 0):
            # Dont move
            return

        neighbour_cells = self.model.grid.get_neighborhood(
            self.pos,
            moore=False, # Moore neighborhood (including diagonals)
            include_center=True)
        
        # Search for road in current cell
        road_agent = [agent for agent in agents_in_current_cell if isinstance(agent, Road)]
        # Search for traffic light in current cell
        traffic_light_agent = [agent for agent in agents_in_current_cell if isinstance(agent, Traffic_Light)]
        
        if(self.destination in neighbour_cells):
            # Move to destination
            self.model.grid.move_agent(self, self.destination)
            if (len(road_agent) > 0):
                road_agent[0].occupied_next = False
            if (len(traffic_light_agent) > 0):
                traffic_light_agent[0].occupied_next = False 
            self.arrived = True
            return

        directions_to_check = []
        if(len(road_agent) > 0):
            directions_to_check = road_agent[0].directions
        elif(len(traffic_light_agent) > 0):
            directions_to_check = self.directions
        
        possible_steps = []
        if("right" in directions_to_check):
            possible_steps += [cell for cell in neighbour_cells if(cell[0] >= self.pos[0])]
        if("left" in directions_to_check):
            possible_steps += [cell for cell in neighbour_cells if(cell[0] <= self.pos[0])]
        if("up" in directions_to_check):
            possible_steps += [cell for cell in neighbour_cells if(cell[1] >= self.pos[1])]
        if("down" in directions_to_check):
            possible_steps += [cell for cell in neighbour_cells if(cell[1] <= self.pos[1])]
        
        if(len(traffic_light_agent) > 0):
            if(not traffic_light_agent[0].state):
                # Stop if traffic light is in red
                return
        elif(self.next_star in possible_steps):
            if(self.next_star != self.destination):
                # Calculate next star if found the current one
                star_index = self.stars_list.index(self.next_star)
                self.next_star = self.stars_list[star_index + 1]
            else:
                self.arrived = True

        # Choose next cell to move
        cell_to_move = None
        empty_positions = []
        road_agents = []
        for i in range(0, len(possible_steps)):
            list_with_agent_in_cell = self.model.grid.get_cell_list_contents([possible_steps[i]])
            road_agent_in_cell = [agent for agent in list_with_agent_in_cell if isinstance(agent, Road)]
            traffic_light_agent_in_cell = [agent for agent in list_with_agent_in_cell if isinstance(agent, Traffic_Light)]
            # Check if theres an empty cell or will be empty
            if(len(road_agent_in_cell) > 0):
                if not road_agent_in_cell[0].occupied_next:
                    empty_positions.append(possible_steps[i])
                    road_agents.append(road_agent_in_cell[0])
            elif(len(traffic_light_agent_in_cell) > 0):
                if not traffic_light_agent_in_cell[0].occupied_next:
                    empty_positions.append(possible_steps[i])
                    road_agents.append(traffic_light_agent_in_cell[0])

        if self.previous_20_pos.count(self.pos) > 5:
            # Recalculate stars list if stuck
            self.stars_list = google_maps_stars(coord2matrix(self.pos[0], self.pos[1], self.model.grid.height),
                                                coord2matrix(self.destination[0], self.destination[1], self.model.grid.height))
            for ind, star in enumerate(self.stars_list):
                self.stars_list[ind] = matrix2coord(star[0], star[1], self.model.grid.height)
            self.next_star = self.stars_list[0]

        # Calculate closest cell to next star
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
                self.directions = road_agent[0].directions
            elif(len(traffic_light_agent) > 0):
                traffic_light_agent[0].occupied_next = False
            next_road_agent.occupied_next = True
            self.model.grid.move_agent(self, cell_to_move)
            self.previous_20_pos = add_to_20_pos(self.previous_20_pos, cell_to_move)

class Traffic_Light(Agent):
    """
    Traffic light agent. Just to add traffic lights to the grid.
    Attributes:
        state: Wether the traffic light is on green (True) or red (False)
        occupied_next: Check if this cell will be occupied next step
    """
    def __init__(self, unique_id, model, state = False):
        """
        Creates a new traffic light agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Wether the traffic light is on green (True) or red (False)
        """
        super().__init__(unique_id, model)
        self.state = state
        self.occupied_next = False

    def step(self):
        pass

class Destination(Agent):
    """
    Destination agent. Just to add destinations to the grid.
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
    Road agent. Just to add roads to the grid.
    Attributes:
        directions: List of possibles directions in this cell
        occupied_next: Check if this cell will be occupied next step
    """
    def __init__(self, unique_id, model, directions = ["left"]):
        """
        Creates a new road agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            directions: List of possibles directions in this cell
        """
        super().__init__(unique_id, model)
        self.directions = directions
        self.occupied_next = False

    def step(self):
        pass
