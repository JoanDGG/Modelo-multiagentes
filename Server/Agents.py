from mesa import Agent
import math

class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, destination):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.destination = destination
        self.next_star = destination
        self.direction = "Left"

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
            moore=True, # Moore neighborhood (including diagonals)
            include_center=True)
        
        # Get the road agent of actual cell
        # PENDIENTE: eliminar celdas que no son del carril opuesto
        road_agent = [agent for agent in present_in_cell if isinstance(agent, Road)]
        if(road_agent):
            if(road_agent.direction == "Right"):
                possible_steps = [cell for cell in neighbour_cells if(cell[0] >= self.pos[0])]
            elif(road_agent.direction == "Left"):
                possible_steps = [cell for cell in neighbour_cells if(cell[0] <= self.pos[0])]
            elif(road_agent.direction == "Up"):
                possible_steps = [cell for cell in neighbour_cells if(cell[1] >= self.pos[1])]
            elif(road_agent.direction == "Down"):
                possible_steps = [cell for cell in neighbour_cells if(cell[1] <= self.pos[1])]
        else:
            if(self.direction == "Right"):
                possible_steps = [cell for cell in neighbour_cells if(cell[0] >= self.pos[0])]
            elif(self.direction == "Left"):
                possible_steps = [cell for cell in neighbour_cells if(cell[0] <= self.pos[0])]
            elif(self.direction == "Up"):
                possible_steps = [cell for cell in neighbour_cells if(cell[1] >= self.pos[1])]
            elif(self.direction == "Down"):
                possible_steps = [cell for cell in neighbour_cells if(cell[1] <= self.pos[1])]
        
        self.direction = road_agent.direction
        #possible_steps.append(self.pos)

        if(self.destination in possible_steps):
            # Move to destination
            self.model.grid.move_agent(self, self.destination)
        else:
            traffic_light_agent = [agent for agent in present_in_cell if isinstance(agent, Traffic_Light)]
            
            if(traffic_light_agent):
                if(not traffic_light_agent.state):
                    # Stop if red light
                    return
            elif(self.next_star in possible_steps):
                # PENDIENTE: Update next star
                pass

            # Calculate cell_to_move:
            # Check which grid cells are empty

            # Calculate closest cell to next star
            cell_to_move = None
            empty_positions = []
            road_agents = []
            for i in range(0, len(possible_steps)):
                list_with_agent_in_cell = self.model.grid.get_cell_list_contents([possible_steps[i]])
                road_agent_in_cell = [agent for agent in list_with_agent_in_cell if isinstance(agent, Road)]
                # If theres an empty cell or will be empty
                if not road_agent_in_cell[0].occupied_next:
                    empty_positions.append(possible_steps[i])
                    road_agents.append(road_agent_in_cell[0])

            distance = math.inf
            index_min_distance = None
            for index, cell in enumerate(empty_positions):
                distance_from_cell = math.sqrt((cell[0] - self.model.drop_zone[0])**2+(cell[1] - self.model.drop_zone[1])**2)
                if(distance_from_cell < distance):
                    distance = distance_from_cell
                    index_min_distance = index

            if(isinstance(index_min_distance, int)):
                cell_to_move = empty_positions[index_min_distance]
                next_road_agent = road_agents[index_min_distance]
                
            if(cell_to_move):
                # Move to next_cell
                road_agent.occupied_next = False
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
    def __init__(self, unique_id, model, direction = "Left"):
        super().__init__(unique_id, model)
        self.direction = direction
        # Añadir varias direcciones para intersecciones
        self.occupied_next = False

    def step(self):
        pass
