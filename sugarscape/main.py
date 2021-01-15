
from agents import Consumer, Sugar
from model import SugarModel


def main():
    global data
    N = 10
    size = 50
    steps = 100
    model = SugarModel(N, size, size)
    for i in range(steps):
        model.step() 
    data = model.datacollector.get_agent_vars_dataframe()

    
if __name__ == "__main__":
    main()
    
    