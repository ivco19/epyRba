import numpy as np
import pandas as pd 
rver = pd.read_csv('exports/export_2020-04-08T13_47_38.380044.csv')
pver = pd.read_csv('exports/results_long.csv')

relats = [] 
for acolumn in pver.columns: 
    relats.append(np.abs(rver[acolumn]-pver[acolumn])/np.abs(rver[acolumn])) 
                                                                                                                          
for arela in relats: 
    print(np.max(arela)/1e-5, np.min(arela)/1e-5, np.mean(arela)/1e-5, np.std(arela)/1e-5) 

     