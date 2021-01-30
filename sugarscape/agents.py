
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
    """ An agent on the sugarscape"""

    def __init__(self, unique_id, model, vision = 3, sugar = 2, gen = 1, metabolism = 1, age = 0, reproduction_and_death = True, spawn_at_random = False):
        
        """
        Initizalize an agent
        """
        super().__init__(unique_id, model)
        self.sugar = sugar
        self.max_sugar = 7 
        self.max_age = np.random.normal(loc = 80, scale = 4) #mean of 81 (average life expectancy years), std of 4; currently set to steps in the model
        self.age = age
        self.gen = gen
        self.vision = vision
        self.metabolism = metabolism
        self.reproduction_and_death = reproduction_and_death
        self.spawn_at_random = spawn_at_random


    def step(self):
        
        """
        Agent ages one step, moves, reduces it sugar level according to metabolism, and consumes sugar.
        Optionally, an agent can also die and respawn in several different ways. 
        All parameters are determined in the initialization
        """
        self.age += 1
        self.move_agent()
        self.sugar -= self.metabolism

        # Eat sugar
        available_sugar = self.get_sugar(self.pos).amount
        self.sugar += available_sugar
#        self.total_sugar_in_field -= available_sugar
        # Set sugar in current cell to zero
        self.get_sugar(self.pos).eat_sugar() 
        
        
        
        if self.sugar == 0:
            self.model.remove_agent(self)
            
            self.gen += 1
            x = self.model.random.randrange(self.model.grid.width)
            y = self.model.random.randrange(self.model.grid.height)
            new_pos = (x,y)
                    
            self.model.add_agent(Consumer, new_pos, f"{self.unique_id.split('-')[0]}-{self.gen}", self.gen, self.model.vision, self.model.metabolism, self.model.starting_sugar)
                    
            
        if self.reproduction_and_death:
            if self.age > self.max_age: # Agent dies
                # Tax inheritance
                self.model.inheritance_tax_agent(self)
                
                if self.model.spawn_at_random:
                    self.gen += 1
                    x = self.model.random.randrange(self.model.grid.width)
                    y = self.model.random.randrange(self.model.grid.height)
                    new_pos = (x,y)
                    
                    self.model.add_agent(Consumer, new_pos, f"{self.unique_id.split('-')[0]}-{self.gen}", self.gen, self.model.vision, self.model.metabolism, self.model.starting_sugar)
                    self.model.remove_agent(self) #agent dies
                    
                    
                else:
                    #spawn new agent
                    self.gen += 1
                    if self.sugar != 0:
                        self.model.add_agent(Consumer, self.pos, f"{self.unique_id.split('-')[0]}-{self.gen}", self.gen, self.vision, self.metabolism, self.sugar)
                    else:
                        self.model.add_agent(Consumer, self.pos, f"{self.unique_id.split('-')[0]}-{self.gen}", self.gen, self.vision, self.metabolism, self.model.starting_sugar)
                   
                    self.model.remove_agent(self) #agent dies
                
        
    def neighboring_consumers(self, position_list):
        """
        Provide a list of positions with possible neighboring consumers
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
        Provide a touple with the position coordinates (x,y)
        Returns sugar agent in a specific cell 
        '''
        current_cell = self.model.grid.get_cell_list_contents([pos])

        for agent in current_cell:
            if type(agent) == Sugar:
                return agent


    def is_empty(self, pos):
        '''
        Provide a touple with the position coordinates (x,y)
        Checks if current cell is empty
        Returns True or False
        '''

        
        current_cell = self.model.grid.get_cell_list_contents([pos])

        # Check if cell contains agent (apart from sugar)
        return len(current_cell) < 2

    def get_dist(self, cell):
        '''
        Provide a touple with the position coordinates (x,y)
        Returns euclidian distance between current position and a cell
        '''
        distance = np.sqrt((cell[0] - self.pos[0])**2 + (cell[1] - self.pos[1])**2)
        return distance
    
    

    def move_agent(self):
        '''
        This function checks for empty cells around agent and moves to cell containing the highest amount of sugar
        '''

        neighborhood = [move for move in self.model.grid.get_neighborhood(self.pos, moore = True, include_center = False, radius = self.vision) if self.is_empty(move)]
        
        # Find cells with the highest amount of sugar in the agents neighborhood
        try:
            max_sugar = max([self.get_sugar(pos).amount for pos in neighborhood])
         
            possible_moves = [pos for pos in neighborhood if self.get_sugar(pos).amount == max_sugar]
            
            # Find shortest distance to a cell with max sugar 
            shortest_dist = min([self.get_dist(pos) for pos in possible_moves])
    
            # Create list with cells with the highest sugar the are closest to the agent
            nearest_possible_moves = [cell for cell in possible_moves if self.get_dist(cell) == shortest_dist]
            
            # Move to random cell from this list
            self.model.grid.move_agent(self, random.choice(nearest_possible_moves))
        
        # This had to be added, as the function gets an error if it has no possible space to move to (e.g. with instant growback all spots around agent are taken)
        except:
            print(self.unique_id, " couldn't move.") #agent does not move

            pass
        




class Sugar(Agent):
    def __init__(self, pos, model, max_sugar, instant_grow_back = False):
        """
        initialization of sugar agent
        """
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar
        self.instant_grow_back = instant_grow_back


    def step(self):
        """
        Grows back sugar at predefined rate or to total sugar
        """
        
        if not self.instant_grow_back:
            self.amount = min([self.max_sugar, self.amount + 1])
        else:
            self.amount = self.max_sugar
        
    def eat_sugar(self):
        """
        sugar is being consumed by agent
        reduces sugar to zero
        """
        self.amount = 0
