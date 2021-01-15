
from agents import Consumer, Sugar
from model import SugarModel


def main():
    global data
    N = 100
    size = 50
    steps = 300
    vision = 3
    model = SugarModel(N, size, size, vision)

    for i in range(steps):
        model.step() 
    data = model.datacollector.get_agent_vars_dataframe()

    
if __name__ == "__main__":
    main()
    
    