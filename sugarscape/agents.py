
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

    def __init__(self, unique_id, model, vision = 3, sugar = 2, gen = 1, metabolism = 1, age = 0, reproduction_and_death = True, spawn_at_random = True):

        super().__init__(unique_id, model)
        self.sugar = sugar
        self.max_sugar = 7 
        self.max_age = np.random.normal(loc = 81, scale = 4) #mean of 81 (average life expectancy years), std of 4; currently set to steps in the model
        self.age = age
        self.gen = gen
        self.vision = vision
        self.metabolism = metabolism
        self.reproduction_and_death = reproduction_and_death
        self.spawn_at_random = spawn_at_random


    def step(self):
        self.age += 1
        self.move_agent()
        self.sugar -= self.metabolism

        # Eat sugar
        available_sugar = self.get_sugar(self.pos).amount
        self.sugar += available_sugar
        # Set sugar in current cell to zero
        self.get_sugar(self.pos).eat_sugar() 
        
        
        
        if self.sugar == 0:
            self.model.remove_agent(self)
            
        if self.reproduction_and_death:
            if self.age > self.max_age: #agent dies
         
                #tax inheritance
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
                    self.model.add_agent(Consumer, self.pos, f"{self.unique_id.split('-')[0]}-{self.gen}", self.gen, self.vision, self.metabolism, self.sugar)
                    
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

        neighborhood = [move for move in self.get_neighbors_w_empty_fields(self.vision) if self.is_empty(move)]
        
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
        
        #this had to be added, as the function gets an error if it has no possible space to move to (e.g. with instant growback all spots around agent are taken)
        except:
            pass
        
        
    def get_neighbors_w_empty_fields(self, vision):
            
        #create list with surrounding cells
        list_of_neighbors = self.model.grid.get_neighborhood(self.pos, moore = True, include_center = False, radius = self.vision)
#        
#
        empty_fields = []
        index_list = []
        for cell in list_of_neighbors:
            try:
                if self.model.grid.get_cell_list_contents(cell)[0].max_sugar == 0:
                    empty_fields.append(cell)
                    index_list.append(list_of_neighbors.index(cell))
            except: #if cell is outside the grid delete it from the possibiolities
                index_list.append(list_of_neighbors.index(cell))
                pass
                
        for index in sorted(index_list, reverse=True):
            del list_of_neighbors[index]

       
        #take another step in the direction for said field
        for cell in empty_fields:
            step_size = 1
            counter = 0
            cell_og = cell
            while True & (counter != 100): #take steps till the end
                try:
                    differences = self.get_direction_of_position(cell)
                    if differences[0] >= 0:
                        cell[0] += step_size
                        if self.model.grid.get_cell_list_contents(cell)[0].max_sugar == 0:
                            step_size += 1
                        if self.model.grid.get_cell_list_contents(cell)[0].max_sugar != 0:
                            list_of_neighbors.append(cell)
                            break
                        
                    if differences[0] < 0:
                        cell[0] -= step_size
                        if self.model.grid.get_cell_list_contents(cell)[0].max_sugar == 0:
                            step_size += 1
                        if self.model.grid.get_cell_list_contents(cell)[0].max_sugar != 0:
                            list_of_neighbors.append(cell)
                            break
                        
                    if differences[1] >= 0:
                        cell[1] += step_size
                        if self.model.grid.get_cell_list_contents(cell)[0].max_sugar == 0:
                            step_size += 1
                        if self.model.grid.get_cell_list_contents(cell)[0].max_sugar != 0:
                            list_of_neighbors.append(cell)
                            break
                        
                    if differences[1] < 0:
                        cell[1] -= step_size
                        if self.model.grid.get_cell_list_contents(cell)[0].max_sugar == 0:
                            step_size += 1
                        if self.model.grid.get_cell_list_contents(cell)[0].max_sugar != 0:
                            list_of_neighbors.append(cell)
                            break
                    counter += 1
                    print("It got stuck at ", cell_og, " and final ", cell)
                except: #if the try does not work, the cell content is outside the grid, so it just breaks without adding cell
                    break
                
                
        return list_of_neighbors
            
                        
                        
                        
        
        
    def get_direction_of_position(self, cell):
        
        x_diff = self.pos[0] - cell[0]
        y_diff = self.pos[1] - cell[1]
        
        return (x_diff, y_diff)
    
            



class Sugar(Agent):
    def __init__(self, pos, model, max_sugar, instant_grow_back = False):
        super().__init__(pos, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar
        self.instant_grow_back = instant_grow_back

    def step(self):
        if not self.instant_grow_back:
            self.amount = min([self.max_sugar, self.amount + 1])
        else:
            self.amount = self.max_sugar
        
    def eat_sugar(self):
        self.amount = 0