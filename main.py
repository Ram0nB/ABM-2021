# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 09:58:43 2021

@author: chris
"""

from mesa import Agent, Model
from mesa.space import MultiGrid, SingleGrid
from mesa.time import RandomActivation


class PersonalAgent(Agent):
    """
    individuals in the model
    """
    def __init__(self, unique_id, model, wealth):
        super().__init__(unique_id, model)
        self.wealth = wealth
        
        
    def step():
        pass
    
    
class Money(Agent):
    """
    environmental sugar
    """
    def __init__(self, unique_id, model, money):
        super().__init__(unique_id, model)
        self.money = money
    
    
class Landscape(Model):
    """
    is the main model
    """
    
    def __init__(self, N, width, height):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, True)


    def step():
        pass
    
    

def main():
    
    OurModel = Landscape(100, 20,20)
    for i in range(10):
        OurModel.step()

if __name__ == "__main__":
    main()