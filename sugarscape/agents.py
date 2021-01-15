
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

import numpy as np
import random

class Consumer(Agent):
    """ An agent on the sugarscape"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.sugar = 2
        self.max_sugar = 7 
        self.max_age = np.random.normal(loc = 81, scale = 4) #mean of 81 (average life expectancy years), std of 4; currently set to steps in the model
        


    def step(self):
        
        self.sugar -= 1
        self.move_agent()
        
        #eat sugar
        wealth_available = self.get_sugar(self.pos).amount
        self.sugar += wealth_available
        self.get_sugar(self.pos).eat_sugar() #reduce the sugar to zero
        
        
        if self.sugar == 0:
            self.model.remove_agent(self)
        if self.model.schedule.time > self.max_age: #agent dies
            #leaves wealth to surrounding agents
            neighborhood = self.model.grid.get_neighborhood(self.pos, moore = True, include_center = False, radius = 10) #get neighborhood
            consumers_in_neighborhood = self.neighboring_consumers(neighborhood) #get agents in neighborhood
            
            if consumers_in_neighborhood:
                wealth_fraction = int(self.sugar/len(consumers_in_neighborhood))
                for inheritant in consumers_in_neighborhood:
                    inheritant.sugar += wealth_fraction
                
                
            
            
            
            self.model.remove_agent(self) #agent dies
            
        
    def neighboring_consumers(self, position_list):
        """
        Returns list of consumer agents in neighboorhood
        """
        agent_list = []
        #loop over all neighbors
        for position in position_list:
            agents_in_cell = self.model.grid.get_cell_list_contents(position)
            #loop over all agents in the cell to find if agent is present
            for agent in agents_in_cell:
                if type(agent).__name__ == "Consumer":
                    agent_list.append(agent)
            
            
            

    def get_sugar(self, pos):
        '''
        Returns sugar agent in a specific cell 
        '''

        current_cell = self.model.grid.get_cell_list_contents([pos])

        for agent in current_cell:
            if type(agent) == Sugar:
                return agent


    def is_empty(self, pos):
        '''
        Checks if current cell is empty
        '''
        current_cell = self.model.grid.get_cell_list_contents([pos])

        # Check if cell contains agent (apart from sugar)
        return len(current_cell) < 2

    def move_agent(self):
        '''
        This function checks for empty cells around agent and moves to cell containing the highest amount of sugar
        '''
        # Retrieve possible moves         
        neighborhood = [
            move
            # TODO: radius (vision) is currently hardcoded --> change this later
            for move in self.model.grid.get_neighborhood(
                self.pos, moore = True, include_center = False, radius = 1
                )
            if self.is_empty(move)
        ]
        
        
        # Move to random cell with highest amount of sugar
        highest_amount = max([self.get_sugar(pos).amount for pos in neighborhood])
        possible_moves = [pos for pos in neighborhood if self.get_sugar(pos).amount == highest_amount]
        # TODO: change this to the nearest location with max sugar, in stead of random location with max sugar
        self.model.grid.move_agent(self, random.choice(possible_moves))



class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar

    def step(self):
        self.amount = min([self.max_sugar, self.amount + 1])
        
    def eat_sugar(self):
        self.amount = 0