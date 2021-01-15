
from agents import Consumer, Sugar
from model import SugarModel

import csv

def main():
    # global data
    N = 100
    size = 50
    steps = 100
    vision = 3
    model = SugarModel(N, size, size, vision)

    for i in range(steps):
        model.step() 
    data = model.datacollector.get_agent_vars_dataframe()
    
    with open('data/data.csv', mode='w') as file:
        data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            data_writer.writerow(row)

    
if __name__ == "__main__":
    main()
    
    