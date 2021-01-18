from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement

from model import SugarModel
from agents import Sugar, Consumer
from colour import Color



import numpy as np

def agent_portrayal(agent):
    '''
    Method that tells the Modular Server how to draw the agents in the CanvasGrid
    '''

    # fill the cell grids with a higher amount of sugar than value 0
    if type(agent) == Sugar and agent.amount > 0.0:

        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "w": 0.8,
                    "h": 0.8}

        # # TODO: Check whether we want to make the colors dynamic based on the max sugar we provide per cell. 
        # # TODO: Otherwise, the code below that is commented out can be removed.
        # # retrieve gradient based on max amount of sugar
        # white = Color("white")
        # colors = list(white.range_to(Color("red"), 4))

        # # Color cells with different sugar levels through color coding
        # portrayal["Color"] = colors[int(agent.amount)]

        if type(agent) == Sugar and agent.amount == 3.0:
            portrayal["Color"] = "#ff0000"
        elif type(agent) == Sugar and agent.amount == 2.0:
            portrayal["Color"] = "#ff4c4c"
        elif type(agent) == Sugar and agent.amount == 1.0:
            portrayal["Color"] = "#ffb7b7"
        elif type(agent) == Sugar and agent.amount == 4.0:
            portrayal["Color"] = "#ab0000"

        return portrayal

    # Set up visualizing characteristics for consumer agents
    elif type(agent) == Consumer:
        portrayal = {"Shape": "circle",
                    "Color": "grey",
                    "Filled": "true",
                    "Layer": 1,
                    "r": 0.4}

        return portrayal

class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        
        agents_hist = []
        # render the sugar levels of the consumer agents to send to the js vizualization file
        for agent in model.schedule.agents:
            if type(agent) == Consumer:
                agents_hist.append(agent.sugar)
        # return sugar levels in order to be able to send to the js file
        hist = np.histogram(agents_hist, bins=self.bins)[0]
        return [int(x) for x in hist]

# Create a visualized grid of 50 by 50 cells, and display it as 800 by 800 pixels
grid = CanvasGrid(agent_portrayal, 99, 99, 800, 800)
# Create a Histogram with x-axis value range 0-100
histogram = HistogramModule(list(range(100)), 300, 800)

# Initiate local server for visualizing data
server = ModularServer(SugarModel,
                        [grid, histogram],
                        "SugarModel",
                        {"N":100, "width":99, "height":99})

server.port = 8521
server.launch()