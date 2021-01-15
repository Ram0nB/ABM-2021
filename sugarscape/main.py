import pandas as pd

from datetime import datetime
from datetime import date

from agents import Consumer, Sugar
from model import SugarModel


def main():
    global data
    N = 100
    size = 50
    steps = 10
    model = SugarModel(N, width=size, length=size)

    for i in range(steps):
        model.step() 

    # Retrieve dataframe from datacollector   
    df = model.datacollector.get_agent_vars_dataframe()
    
    # Retrieve current date and time for csv filename
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    # Save data to csv file
    # df.to_csv(f'data/{today} {current_time}.csv')
    print(f'saved data for {today} {current_time}')
    
if __name__ == "__main__":
    main()
    
    