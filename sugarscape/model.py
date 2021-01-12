from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

import numpy as np
import random

from agents import Consumer, Sugar

class SugarModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.N_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.agents = []

        # Create agents
        for i in range(self.N_agents):
            a = Consumer(i, self)

            self.schedule.add(a)
            self.agents.append(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            self.grid.place_agent(a, (x, y))
        
        # Create sugar map
        sugar_distribution = np.genfromtxt("sugar-map.txt")
        
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar((x, y), self, max_sugar)
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)


    def remove_agent(self, agent):
        '''
        Method that enables us to remove agents
        '''
        self.N_agents -= 1
        
        # Remove agent from grid
        self.grid.remove_agent(agent)
        
        # Remove agent from model
        self.agents.remove(agent)

    def step(self):
        '''
        Method that steps every agent. 
        
        Prevents applying step on new agents by creating a local list.
        '''
        for agent in list(self.agents):
            agent.step()
