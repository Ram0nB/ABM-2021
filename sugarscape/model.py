from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation, BaseScheduler
from mesa.datacollection import DataCollector

import numpy as np
import random
import pandas as pd

from agents import Consumer, Sugar

"""
To be implemented

"""

class SugarModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height, vision=3):
        self.N_agents = N
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.schedule_sugar = BaseScheduler(self)
        self.agents = []

        # Create agents
        for i in range(self.N_agents):
            a = Consumer(f"{i}", self, vision)

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
            self.schedule_sugar.add(sugar)
            
        self.datacollector = DataCollector(
                agent_reporters = {"Wealth":"sugar", "Position":"pos"}
                )
        #Data Collection 
        # This is required for the datacollector to work
        self.running = True
        self.datacollector.collect(self)


    def remove_agent(self, agent):
        '''
        Method that enables us to remove agents
        '''
        self.N_agents -= 1
        
        # Remove agent from grid
        self.grid.remove_agent(agent)
        
        # Remove agent from model
        self.agents.remove(agent)
        self.schedule.remove(agent)
        
    def add_agent(self, agent_type, pos, new_id, generation, vision, metabolism):
        """
        Method that enables us to create agents
        """
        #bring alternations into the reproduction 
        metabolism = metabolism + random.randint(-1,1)
        vision = vision + random.randint(-1,1)
        if metabolism <= 0:
            metabolism = 1
        if vision <= 0:
            vision = 1
        #create new agent
        agent = agent_type(new_id, self, gen = generation, vision = vision, metabolism = metabolism)
        self.N_agents += 1
        self.agents.append(agent)
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent) 
        


    def step(self):
        '''
        Method that steps every agent.
        
        '''
        
        self.datacollector.collect(self)
        self.schedule.step()
        self.schedule_sugar.step()
