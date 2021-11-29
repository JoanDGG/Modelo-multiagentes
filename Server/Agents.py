from mesa import Agent

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
        self.next_star = None

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if(isinstance(self.model.grid[self.pos], Destination)):
            # Detenerse
            return
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Moore neighborhood (including diagonals)
            include_center=True)
        
        if(self.destination in possible_steps):
            # Moverse a destino
            self.model.grid.move_agent(self, self.destination)
        elif(isinstance(self.model.grid[self.pos], Traffic_Light) and not self.model.grid[self.pos].state):
            # Detenerse en semaforo rojo
            return
        elif(self.next_star in possible_steps):
            # Actualizar estrella
            pass
        # Calcular siguiente_celda
            # Checks which grid cells are empty (considerar direccion de las celdas)
        # freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        # if(siguiente_celda.occupied_next):
            # Parar
        #   return
        # else:
            # Avanzar a celda siguiente
            # self.model.grid.move_agent(self, siguiente_celda)

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
        self.occupied_next = False

    def step(self):
        pass
