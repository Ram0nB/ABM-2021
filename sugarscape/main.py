
from agents import Consumer, Sugar
from model import SugarModel


def main():
    global data
    N = 100
    size = 50
<<<<<<< HEAD
    steps = 300
    model = SugarModel(N, size, size)
=======
    steps = 100
    vision = 3
    model = SugarModel(N, size, size, vision)
>>>>>>> 33d6244f8c0d0be93cff98fbd5865d1fd1ecf81b
    for i in range(steps):
        model.step() 
    data = model.datacollector.get_agent_vars_dataframe()

    
if __name__ == "__main__":
    main()
    
    