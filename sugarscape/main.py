import pandas as pd

from datetime import datetime
from datetime import date

from agents import Consumer, Sugar
from model import SugarModel

def main(parameters):
    global df_agent_vars, df_model_vars

    N, size, vision, inheritance_tax_brackets, inheritance_tax_percentages, starting_wealth, steps = parameters

    steps = 100

    model = SugarModel(N, 
    width=size,
    height=size, 
    vision= vision, 
    reproduction_and_death = True, 
    spawn_at_random = True, 
    instant_grow_back = True, 
    starting_sugar = starting_wealth, 
    tax_brackets = tax_brackets, 
    tax_percentages = tax_percentages, 
    inheritance_tax_brackets = inheritance_tax_brackets, 
    inheritance_tax_percentages = inheritance_tax_percentages, 
    amsterdam_map = False)


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

    print(f'saved data for {today} {current_time}')
    return df_agent_vars


if __name__ == "__main__":

    """
    20-30 runs (maybe even 50 runs); also measure spread
    Use CI instead of STD 
    """
    
    N = 223
    size = 50
    vision = 5
    inheritance_tax_brackets = [0, 10, 30, 50, 100]
    inheritance_tax_percentages = [0, 0.3, 0.3, 0.35, 0.6]
    starting_wealth = 5
    steps = 100
    

    parameters = N, size, vision,inheritance_tax_brackets, inheritance_tax_percentages, starting_wealth, steps
    # print(parameters)
    main(parameters)
