import pandas as pd

from datetime import datetime
from datetime import date

from agents import Consumer, Sugar
from model import SugarModel


def main():
    global df_agent_vars, df_model_vars
    N = 20
    size = 99
    vision = 1
    tax_brackets = [0,0]
    tax_percentages = [0,0]
    inheritance_tax_brackets = [0, 10, 30, 50, 100]
    inheritance_tax_percentages = [0, 0.3, 0.3, 0.35, 0.6]
    starting_wealth = 5


    steps = 300
    model = SugarModel(N, width=size, height=size, vision= vision, reproduction_and_death = False, instant_grow_back = True, starting_sugar = starting_wealth, tax_brackets = tax_brackets, tax_percentages = tax_percentages, inheritance_tax_brackets = inheritance_tax_brackets, inheritance_tax_percentages = inheritance_tax_percentages, amsterdam_map = True)

    for i in range(steps):
        model.step() 

    # Retrieve dataframe from datacollector   
    df_agent_vars = model.datacollector.get_agent_vars_dataframe()
    df_model_vars = model.datacollector.get_model_vars_dataframe()
    
    #add variables
    df_agent_vars["Vision"] = vision
    df_agent_vars["N_Agents"] = N
    df_agent_vars["Size"] = size
    df_agent_vars["tax brackets"] = f"{tax_brackets}"
    df_agent_vars["tax percentages"] = f"{tax_percentages}"
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
    df_model_vars.to_csv(f'data/{today} {current_time} Model Vars.csv')
    print(f'saved data for {today} {current_time}')
    
if __name__ == "__main__":
    main()
    
    