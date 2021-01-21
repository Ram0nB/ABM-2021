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
    def __init__(self, N, width, height, vision=3, starting_sugar = 2, metabolism = 1, reproduction_and_death = True, spawn_at_random = False, instant_grow_back = False, tax_brackets = [0,0], tax_percentages = [0,0], inheritance_tax_brackets = [0, 1, 3, 5, 7], inheritance_tax_percentages = [0, 0.1, 0.2, 0.35, 0.6], amsterdam_map = False):
        
        self.N_agents = N
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.schedule_sugar = BaseScheduler(self)
        
        self.vision = vision
        self.metabolism = metabolism
        self.starting_sugar = starting_sugar
        self.amsterdam_map = amsterdam_map
        self.agents = []
        self.tax_revenue = 0
        self.inheritance_tax_revenue = 0
        self.tax_brackets = tax_brackets
        self.tax_percentages = tax_percentages
        self.inheritance_tax_brackets = inheritance_tax_brackets
        self.inheritance_tax_percentages = inheritance_tax_percentages
        self.reproduction_and_death = reproduction_and_death
        self.instant_grow_back = instant_grow_back
        self.colour_gradient = self.set_up_colour_gradient()
        self.spawn_at_random = spawn_at_random
        
        


        # Create agents
        for i in range(self.N_agents):
            a = Consumer(f"{i}", self, self.vision, self.starting_sugar, reproduction_and_death = self.reproduction_and_death, spawn_at_random = self.spawn_at_random)

            self.schedule.add(a)
            self.agents.append(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            print(x,y)

            self.grid.place_agent(a, (x, y))
        
        # Create sugar map
        if self.amsterdam_map:
            sugar_distribution = np.genfromtxt("suger-map_ams99x99max50.txt")    
        else:
            sugar_distribution = np.genfromtxt("sugar-map.txt")
            
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar((x, y), self, max_sugar, self.instant_grow_back)
            self.grid.place_agent(sugar, (x, y))
            self.schedule_sugar.add(sugar)

        # Data Collection     
        self.datacollector = DataCollector(
                agent_reporters = {"Wealth":"sugar", "Position":"pos"}, 
                model_reporters = {"Tax Revenue":get_tax_revenue, "Inheritance Tax Revenue": get_inheritance_tax_revenue}
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
        
        if not self.spawn_at_random:
            # Bring alternations into the reproduction 
            metabolism = metabolism + random.randint(-1,1)
            vision = vision + random.randint(-1,1)
    
            if metabolism <= 0:
                metabolism = 1
            if vision <= 0:
                vision = 1
        
        # Create new agent
        agent = agent_type(new_id, self, gen = generation, vision = vision, metabolism = metabolism, sugar = sugar)
        self.N_agents += 1
        self.agents.append(agent)
        self.grid.place_agent(agent, pos)
        self.schedule.add(agent) 

        
    
    def tax_agent(self, agent):
        """
        Taxes Agent according to it's wealth
        tax_brackets is a list with the value in which tax bracket the agent falls
        tax_percentages is the according percentage per bracket
        tax brackets are left open on max
        """
                    
        # Find tax bracket
        for bracket in range(len(self.tax_brackets) - 1):
            if (self.tax_brackets[bracket] <= agent.sugar) & (self.tax_brackets[bracket + 1] >= agent.sugar): #execute taxation
                self.tax_revenue += agent.sugar * self.tax_percentages[bracket]
                agent.sugar = agent.sugar * (1 - self.tax_percentages[bracket])
                break
            
        if (len(self.tax_brackets) - 1) == bracket: #checks if the agent is above the last tax bracket
            self.tax_revenue += agent.sugar * self.tax_percentages[-1]
            agent.sugar = agent.sugar * (1 - self.tax_percentages[-1])
                
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
            
        if (len(self.tax_brackets) - 1) == bracket: #checks if the agent is above the last tax bracket
            self.inheritance_tax_revenue += agent.sugar * self.inheritance_tax_percentages[-1]
            agent.sugar = agent.sugar * (1 - self.inheritance_tax_percentages[-1])

    def step(self):
        '''
        Method that steps every agent.
        
        '''
        self.tax_revenue = float(0)
        self.inheritance_tax_revenue = float(0)
        
        self.datacollector.collect(self)
        self.schedule.step()
        self.schedule_sugar.step()

        #distribute taxes to agents
        list_agents = [agent for agent in self.schedule.agents]
        for agent in list_agents:
            agent.sugar += self.tax_revenue * (1/self.N_agents)
            agent.sugar += self.inheritance_tax_revenue * (1/self.N_agents)
            
            
    def set_up_colour_gradient(self):
        '''
        Method that sets up a color gradient depending on the amount of different sugar levels
        '''
        # Create sugar map from text file
        # sugar_distribution = np.genfromtxt("sugar-map.txt")
        sugar_distribution = np.genfromtxt("suger-map_ams99x99max50.txt")
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
        
