from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from Agents import *

class TrafficModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self):

        self.destinations = []
        dataDictionary = {">" : "Right",
                          "<" : "Left",
                          "^" : "Up",
                          "v" : "Down"}

        with open('base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1  # because of /n.
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height,torus = False) 
            self.schedule = RandomActivation(self)  # Agents activate randomly each step.

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col in ["S", "s"]:
                        agent = Traffic_Light(f"tl{r*self.width+c}", self, False if col == "S" else True)
                        self.schedule.add(agent)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "#":
                        agent = Obstacle(f"ob{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                    elif col == "D":
                        agent = Destination(f"d{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

        # N agent cars = len(self.destinations)
        # Add the agent to a random empty grid cell
        for i in destination_stars:
            # Place car where there is no other car and is a Road
            pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
            pos = pos_gen(self.grid.width, self.grid.height)
            # Si no hay coche y hay road
            agents_in_pos = self.grid.get_cell_list_contents([pos])
            print(agents_in_pos)
            car_agents = [agent for agent in agents_in_pos if isinstance(agent, Car)]
            road_agents = [agent for agent in agents_in_pos if isinstance(agent, Road)]
            while (road_agents == [] or car_agents != []):
                pos = pos_gen(self.grid.width, self.grid.height)
                agents_in_pos = self.grid.get_cell_list_contents([pos])
                car_agents = [agent for agent in agents_in_pos if isinstance(agent, Car)]
                road_agents = [agent for agent in agents_in_pos if isinstance(agent, Road)]
            print(f"Car pos: {pos}")
            # car.destination = self.destinations[i].pos
            a = Car(i+1000, self, pos, destination_stars[i])
            self.schedule.add(a)
            self.grid.place_agent(a, pos)

        self.running = True 

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        if self.schedule.steps % 10 == 0:
            for agents, x, y in self.grid.coord_iter():
                for agent in agents:
                    if isinstance(agent, Traffic_Light):
                        agent.state = not agent.state