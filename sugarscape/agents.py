
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

import numpy as np
import random

"""
To be implemented
- taxes
    -inheritance
    -regular taxes

"""




class Consumer(Agent):
    """ 
    An agent on the sugarscape
    """
    def __init__(self, unique_id, model, vision = 3, sugar = 2, gen = 1, metabolism = 1):

        super().__init__(unique_id, model)
        self.sugar = sugar
        self.max_sugar = 7 
        self.max_age = np.random.normal(loc = 81, scale = 4) #mean of 81 (average life expectancy years), std of 4; currently set to steps in the model
        self.age = 0
        self.gen = gen
        self.vision = vision
        self.metabolism = metabolism


    def step(self):
        
        self.sugar -= self.metabolism
        self.age += 1
        self.move_agent()
        
        # Eat sugar
        wealth_available = self.get_sugar(self.pos).amount
        self.sugar += wealth_available
        self.get_sugar(self.pos).eat_sugar() #reduce the sugar to zero
        
        self.model.tax_agent(self)
        
        
        if self.sugar == 0:
            self.model.remove_agent(self)
        if self.age > self.max_age: #agent dies
            #leaves wealth to surrounding agents
            neighborhood = self.model.grid.get_neighborhood(self.pos, moore = True, include_center = False, radius = 10) #get neighborhood
            consumers_in_neighborhood = self.neighboring_consumers(neighborhood) #get agents in neighborhood
            
            #tax inheritance
            self.model.inheritance_tax_agent(self)
            #distributes wealth evenly between others
            if consumers_in_neighborhood:
                wealth_fraction = self.sugar/len(consumers_in_neighborhood)
                for inheritant in consumers_in_neighborhood:
                    inheritant.sugar += wealth_fraction
                
            
            #spawn new agent
            self.gen += 1
            self.model.add_agent(Consumer, self.pos, f"{self.unique_id.split('-')[0]}-{self.gen}", self.gen, self.vision, self.metabolism)
            

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

    def get_dist(self, cell):
        '''
        Returns euclidian distance between current position and a cell
        '''
        distance = np.sqrt((cell[0] - self.pos[0])**2 + (cell[1] - self.pos[1])**2)
        return distance

    def move_agent(self):
        '''
        This function checks for empty cells around agent and moves to cell containing the highest amount of sugar
        '''
        # Retrieve cells within the agents vision
        neighborhood = [
            move
            for move in self.model.grid.get_neighborhood(
                self.pos, moore = True, include_center = False, radius = self.vision
                )
            if self.is_empty(move)
        ]
        
        # Find cells with the highest amount of sugar in the agents neighborhood
        max_sugar = max([self.get_sugar(pos).amount for pos in neighborhood])
        possible_moves = [pos for pos in neighborhood if self.get_sugar(pos).amount == max_sugar]
        
        # Find shortest distance to a cell with max sugar 
        shortest_dist = min([self.get_dist(pos) for pos in possible_moves])

        # Create list with cells with the highest sugar the are closest to the agent
        nearest_possible_moves = [cell for cell in possible_moves if self.get_dist(cell) == shortest_dist]
        
        # Move to random cell from this list
        self.model.grid.move_agent(self, random.choice(nearest_possible_moves))



class Sugar(Agent):
    def __init__(self, pos, model, max_sugar):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar

    def step(self):
        self.amount = min([self.max_sugar, self.amount + 1])
        
    def eat_sugar(self):
        self.amount = 0