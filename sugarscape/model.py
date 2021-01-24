from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation, BaseScheduler
from mesa.datacollection import DataCollector

import numpy as np
import random
import pandas as pd

from agents import Consumer, Sugar
from colour import Color


def get_tax_revenue(model):
    return model.tax_revenue


def get_inheritance_tax_revenue(model):
    return model.inheritance_tax_revenue

class SugarModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height, total_sugar_equal=False, total_sugar=1, vision=3, starting_sugar = 2, metabolism = 1, reproduction_and_death = True, spawn_at_random = False, instant_grow_back = False, inheritance_tax_brackets = [0, 1, 3, 5, 7], inheritance_tax_percentages = [0, 0.1, 0.2, 0.35, 0.6], amsterdam_map = False):
        
        self.N_agents = N
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.schedule_sugar = BaseScheduler(self)
        
        self.total_sugar_start = total_sugar
        self.vision = vision
        self.metabolism = metabolism
        self.starting_sugar = starting_sugar
        self.amsterdam_map = amsterdam_map
        self.agents = []
        self.inheritance_tax_revenue = 0
        self.inheritance_tax_brackets = inheritance_tax_brackets
        self.inheritance_tax_percentages = inheritance_tax_percentages
        self.reproduction_and_death = reproduction_and_death
        self.instant_grow_back = instant_grow_back
        self.colour_gradient = self.set_up_colour_gradient()
        self.spawn_at_random = spawn_at_random

        # Create agents
        for i in range(self.N_agents):
            age = int(random.random() * 60)
            a = Consumer(f"{i}", self, self.vision, self.starting_sugar, age = age, reproduction_and_death = self.reproduction_and_death, spawn_at_random = self.spawn_at_random)

            self.schedule.add(a)
            self.agents.append(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            

            self.grid.place_agent(a, (x, y))
        
        # Create sugar map
        if self.amsterdam_map:
            sugar_distribution = np.genfromtxt("AmsMaps/SugerMapAms_Grid-99-Max-50.txt")    
        else:
            sugar_distribution = np.genfromtxt("sugar-map.txt")
        
        # determine fraction of total sugar has to be divided to make total sugar level equal
        if total_sugar_equal is True:
            total_sugar = sugar_distribution.sum()
            if self.amsterdam_map is True:
                other_total_sugar = np.genfromtxt("sugar-map.txt").sum() * self.total_sugar_start
            else:
                other_total_sugar = np.genfromtxt("suger-map_ams99x99max50.txt").sum() * self.total_sugar_start
            fraction_total_sugar = total_sugar / other_total_sugar
        
        self.sugar_agents = []
        for _, x, y in self.grid.coord_iter():
            # set up max sugar levels depending on Booleand for sugar levels equal for both maps
            if total_sugar_equal is True:
                max_sugar = sugar_distribution[x, y] / fraction_total_sugar
            else:
                max_sugar = sugar_distribution[x, y]
            sugar = Sugar((x, y), self, max_sugar * total_sugar, self.instant_grow_back)
            self.sugar_agents.append(sugar)
            self.grid.place_agent(sugar, (x, y))
            self.schedule_sugar.add(sugar)

        # Data Collection     
        self.datacollector = DataCollector(
                agent_reporters = {"Wealth":"sugar", "Position":"pos"}, 
                model_reporters = {"Inheritance Tax Revenue": get_inheritance_tax_revenue, 'Total Sugar Level': self.schedule.model.get_total_sugar}
                )
        
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
        
    def add_agent(self, agent_type, pos, new_id, generation, vision, metabolism, sugar):
        """
        Method that enables us to create agents
        """
        
        
        # Create new agent
        
        agent = agent_type(new_id, self, gen = generation, vision = vision, metabolism = metabolism, sugar = sugar)
     
        self.N_agents += 1
       
        self.agents.append(agent)
       
        self.grid.place_agent(agent, pos)
        
        self.schedule.add(agent) 
   
        
   
    def inheritance_tax_agent(self, agent):
        """
        Taxes wealth left when dead
        Works identical to tax_agent; however, with different tax brackets
        """
        
        #find tax bracket
        
        for bracket in range(len(self.inheritance_tax_brackets) - 1):
            if (self.inheritance_tax_brackets[bracket] <= agent.sugar) & (self.inheritance_tax_brackets[bracket + 1] >= agent.sugar): #execute taxation
                self.inheritance_tax_revenue += agent.sugar * self.inheritance_tax_percentages[bracket]
                agent.sugar = agent.sugar * (1 - self.inheritance_tax_percentages[bracket])
                break
            
        if (len(self.inheritance_tax_brackets) - 1) == bracket: #checks if the agent is above the last tax bracket
            self.inheritance_tax_revenue += agent.sugar * self.inheritance_tax_percentages[-1]
            agent.sugar = agent.sugar * (1 - self.inheritance_tax_percentages[-1])

    def step(self):
        '''
        Method that steps every agent.
        '''
        self.inheritance_tax_revenue = float(0)        
        self.datacollector.collect(self)
        self.schedule.step()
        self.schedule_sugar.step()

        # Distribute taxes to agents
        list_agents = [agent for agent in self.schedule.agents]
        print("Current Agents: ", len(list_agents))
        for agent in list_agents:
            agent.sugar += self.inheritance_tax_revenue * (1/self.N_agents)
            
    def get_total_sugar(self):

        total_sug = 0
        for sugar_agent in self.sugar_agents:
            total_sug += sugar_agent.amount
        
        return total_sug
    
    def set_up_colour_gradient(self):
        '''
        Method that sets up a color gradient depending on the amount of different sugar levels
        '''
        # Create sugar map from text file
        # sugar_distribution = np.genfromtxt("sugar-map.txt")
        sugar_distribution = np.genfromtxt("AmsMaps/SugerMapAms_Grid-99-Max-50.txt")
        max_sugar = int(np.max(sugar_distribution))
        
        # determine possible sugar levels from map
        sugar_levels = []
        for i in range(max_sugar + 1):
          sugar_levels.append(float(i))

        # create a color gradient ranging from white to red
        white = Color("white")
        colors = list(white.range_to(Color("red"),max_sugar + 1))
        colour_gradient = dict()

        colors[0] = "#ffffff"
        colors[-1] = "#ff0000"
        for i in range(len(colors)):
            colour_gradient[sugar_levels[i]] = str(colors[i])

        return colour_gradient

    def agent_portrayal(self, agent):
        '''
        Method that tells the Modular Server how to draw the agents in the CanvasGrid
        '''
        self.agent = agent
        # fill the cell grids with a higher amount of sugar than value 0
        if type(self.agent) == Sugar:
            portrayal = {"Shape": "rect",
                        "Filled": "true",
                        "Color": self.colour_gradient.get(agent.amount),
                        "Layer": 0,
                        "w": 0.8,
                        "h": 0.8}

            return portrayal

        # Set up visualizing characteristics for consumer agents
        elif type(self.agent) == Consumer:
            portrayal = {"Shape": "circle",
                        "Color": "grey",
                        "Filled": "true",
                        "Layer": 1,
                        "r": 0.4}

            return portrayal
        
