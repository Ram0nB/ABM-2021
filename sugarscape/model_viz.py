from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import VisualizationElement

from model import SugarModel
from agents import Sugar, Consumer
from colour import Color



import numpy as np
from colour import Color

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


N = 10
size = 99
model = SugarModel(N, width=size, height=size)

# Create a visualized grid of 50 by 50 cells, and display it as 800 by 800 pixels
grid = CanvasGrid(agent_portrayal, 50, 50, 700, 700)
# Create a Histogram with x-axis value range 0-100
histogram = HistogramModule(list(range(100)), 300, 800)

# Initiate local server for visualizing data
server = ModularServer(SugarModel,
                        [grid, histogram],
                        "SugarModel",
                        {"N":100, "width":size, "height":size})

server.port = 8521
server.launch()
