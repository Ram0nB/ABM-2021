import pandas as pd

from datetime import datetime
from datetime import date

from agents import Consumer, Sugar
from model import SugarModel

def main(parameters):
    global df_agent_vars, df_model_vars

    # used params
    N, vision, total_init_sugar, useamsmap, usedeath, useinstantregrowth, tax_rate = parameters

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
    spawn_at_random = True, 
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
    df_agent_vars["Vision"] = vision
    df_agent_vars["N_Agents"] = N
    df_agent_vars["Size"] = size
    df_agent_vars["inheritance taxbrackets"] = f"{inheritance_tax_brackets}"
    df_agent_vars["inheritance tax percentages"] = f"{inheritance_tax_percentages}"
    df_agent_vars["Starting Wealth"] = starting_wealth
    
    
    # Retrieve current date and time for csv filename
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    now = datetime.now()
    current_time = now.strftime("%H.%M")

    # Save data to csv file
    df_agent_vars.to_csv(f'data/{today} {current_time} Agent Vars.csv')
#    df_model_vars.to_csv(f'data/{today} {current_time} Model Vars.csv')

    print(f'saved data for {today} {current_time}')
    return df_agent_vars


if __name__ == "__main__":

    """
    20-30 runs (maybe even 50 runs); also measure spread
    Use CI instead of STD 
    """
    

    N = 250
    vision = 1
    total_init_sugar = 1
    useamsmap = True
    usedeath = True
    useinstantregrowth = False
    tax_rate = 0.1

    parameters = N, vision, total_init_sugar, useamsmap, usedeath, useinstantregrowth, tax_rate

    main(parameters)
