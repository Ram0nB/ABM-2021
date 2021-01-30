import pandas as pd

from datetime import datetime
from datetime import date

from agents import Consumer, Sugar
from model import SugarModel
import numpy as np

def main(parameters):
    global df_agent_vars, df_model_vars

    # used params
    N, vision, total_init_sugar, useamsmap, usedeath, useinstantregrowth, tax_rate, expname = parameters

    # fixed params
    steps = 250
    size = 50
    inheritance_tax_brackets = []
    inheritance_tax_percentages = []
    starting_wealth = 5

    model = SugarModel(N, 
    width=size,
    height=size, 
    total_sugar_equal = True,
    total_sugar = total_init_sugar, 
    vision = vision,
    reproduction_and_death = usedeath, 
    spawn_at_random = False, 
    instant_grow_back = useinstantregrowth, 
    starting_sugar = starting_wealth, 
    inheritance_tax = tax_rate,
    amsterdam_map = useamsmap)
    
    for i in range(steps):
        model.step()
        print(f"Step: {i}")

    # Retrieve dataframe from datacollector   
    df_agent_vars = model.datacollector.get_agent_vars_dataframe()
#    df_model_vars = model.datacollector.get_model_vars_dataframe()
    
    # Add variables for csv file
    df_agent_vars["Exp name"] = expname
    df_agent_vars["Vision"] = vision
    df_agent_vars["Tax Rate"] = tax_rate
    df_agent_vars["Ams map"] = useamsmap
    df_agent_vars["Death"] = usedeath
    df_agent_vars["Inst regrowth"] = useinstantregrowth

    
    
    # Retrieve current date and time for csv filename
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    now = datetime.now()
    current_time = now.strftime("%H.%M")

    # Save data to csv file
    df_agent_vars.to_csv(f'data/{expname}_{today}_{current_time}_{np.random.randint(10000, 100000)}.csv')
#    df_model_vars.to_csv(f'data/{today} {current_time} Model Vars.csv')

    print(f'saved data for {today} {current_time}')
    return df_agent_vars


def run_main(parameters):
    
    try:
        main(parameters)
    except:
        run_main(parameters)



if __name__ == "__main__":

    """
    20-30 runs (maybe even 50 runs); also measure spread
    Use CI instead of STD 
    """
    

    for tax in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]:
        for runs in range(50):
            
            N = 250
            vision = 2
            total_init_sugar = 2
            useamsmap = False
            usedeath = True
            useinstantregrowth = False
            tax_rate = tax
        
            parameters = N, vision, total_init_sugar, useamsmap, usedeath, useinstantregrowth, tax_rate
            
            
            run_main(parameters)



