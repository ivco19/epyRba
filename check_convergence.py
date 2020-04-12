
import os

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

rver = pd.read_csv('exports/results_R_long.csv')
pver = pd.read_csv('exports/results_long.csv')

rver.drop(columns='Unnamed: 11', inplace=True)

pver.set_index('Día', inplace=True)
rver.set_index('Día', inplace=True)

err_rel = (rver - pver)/rver

values = err_rel.columns
nvals = len(values)

if not os.path.exists('exports/graphs'):
    os.makedirs('exports/graphs')
    
fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(10, 16))
for ax, col in zip(axes.flatten(), values):
    ax.plot(np.abs(err_rel[col]), 'x-', label=r'$|\Delta p/p|$')
    ax.set_xlabel('Dia')
    ax.set_ylabel('Rel Err {}'.format(col))
    ax.hlines(xmin=0, xmax=np.max(err_rel.index), y=10e-6, 
              linestyles='dashed', color='red', label='10e-6')
    ax.legend(loc='best')
plt.tight_layout()
plt.savefig('exports/graphs/error_relativo.png')
