# ABM-2021
Agent-based Modelling Project

To run the model:
1. go to the folder sugarscape
2. open main.py
3. run the script (you can specify the specific parameters first if you'd like)
  - the output of the model will be saved as a csv file in the folder sugarscape/data
  - the output is a dataframe with the steps taken and the agents sugar levels and position
  - other parameters are saved in the columns as well
  
To visualize the model:
1. go to the folder sugarscape
2. open model_viz.py
3. run the script (you can specify the specific parameters first if you'd like)
  - a browser will be opened with the visualization

To run the sensitivity analysis:
1. run sugarscape/sensitivity_analysis.ipynb

To run the experiments:
1. run sugarscape/run_experiments.ipynb

To analyze the data:
1. run sugarscape/data_analysis.ipynb

To create Amsterdam map from CBS data:
run WealthaDATA/parseCBSdata.ipynb

Packages:
Mesa 0.8.8, model created with Mesa
Scipy.stats 1.5.2, check two-way ANOVA assumptions1
Bootstrapped 0.0.2, perform bootstrap method
Seaborn 0.11.0, create plots
IneqPy 0.0.2, calculate Gini-coefficient
Pandas 1.1.0, experiment data is saved in pandas’ dataframes
Numpy 1.19.0
SALib 1.3.12, sensitivity analysis
Rijksdriehoek 0.0.1, Converts WGS’84 to Rijksdriehoek coordinates
Simpledbf 1.2.6, Convert Amsterdam data from CBS
Scikit-image 0.17.2, Resize Amsterdam map
