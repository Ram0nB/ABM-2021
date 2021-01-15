
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

import numpy as np
import random

"""
To be implemented
- different metabolism
- different sights
- reproduction
- inheritance methods
- taxes

"""


class Consumer(Agent):
    """ An agent on the sugarscape"""

    def __init__(self, unique_id, model, vision = 3, sugar = 2, gen = 1):

        super().__init__(unique_id, model)
        self.sugar = sugar
        self.max_sugar = 7 
        self.max_age = np.random.normal(loc = 81, scale = 4) #mean of 81 (average life expectancy years), std of 4; currently set to steps in the model
        self.age = 0
        self.gen = gen
        self.vision = vision


    def step(self):
        
        self.sugar -= 1
        self.age += 1
        self.move_agent()
        
        #eat sugar
        wealth_available = self.get_sugar(self.pos).amount
        self.sugar += wealth_available
        self.get_sugar(self.pos).eat_sugar() #reduce the sugar to zero
        
        
        if self.sugar == 0:
            self.model.remove_agent(self)
        if self.age > self.max_age: #agent dies
            #leaves wealth to surrounding agents
            neighborhood = self.model.grid.get_neighborhood(self.pos, moore = True, include_center = False, radius = 10) #get neighborhood
            consumers_in_neighborhood = self.neighboring_consumers(neighborhood) #get agents in neighborhood
            
            #distributes wealth evenly between others
            if consumers_in_neighborhood:
                wealth_fraction = self.sugar/len(consumers_in_neighborhood)
                for inheritant in consumers_in_neighborhood:
                    inheritant.sugar += wealth_fraction
                
            
            #spawn new agent
            self.gen += 1
            self.model.add_agent(Consumer, self.pos, f"{self.unique_id.split('-')[0]}-{self.gen}", self.gen)
            

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
                    
        return agent_list
            
            
            

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
            for move in self.model.grid.get_neighborhood(
                self.pos, moore = True, include_center = False, radius = self.vision
                )
            if self.is_empty(move)
        ]
        
        
        # Move to random cell with highest amount of sugar
        highest_amount = max([self.get_sugar(pos).amount for pos in neighborhood])
        possible_moves = [pos for pos in neighborhood if self.get_sugar(pos).amount == highest_amount]
        print(possible_moves)
        
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