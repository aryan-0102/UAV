#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('abc_distances1000.csv')
df3 = pd.read_csv('bellman.csv')
df2 = pd.read_csv('dijkstra.csv')
df1 = pd.read_csv('a_star.csv')


abc = df['Distance(meters)']
dikstra = df2['ShortestDistance']
bellman = df3['ShortestDistance']
star = df1['ShortestDistance']

plt.plot(abc, linestyle='-',label='ABC')
plt.plot(dikstra, linestyle='-',label='DIJKSTRA')
plt.plot(star, linestyle='-',label='STAR')
plt.legend()
plt.grid(True)
plt.rcParams['figure.dpi'] = 300

plt.show()
column = ['Name','Total_Distance','Mean','Median']
data = pd.DataFrame(columns=column)


data.loc[len(data)] = ["Dijkstra", dikstra.sum(), dikstra.mean(), dikstra.median()]
data.loc[len(data)] = ['BellmanFord', bellman.sum(), bellman.mean(), bellman.median()]
data.loc[len(data)] = ['ABC',abc.sum(), abc.mean(), abc.median()]
data.loc[len(data)] = ['A-Star',star.sum(),star.mean(),star.median()]

print(data)

