import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('abc_distances1000.csv')

df2 = pd.read_csv('dijkstra.csv')
abc = df['Distance(meters)']/1000

dikstra = df2['ShortestDistance']


plt.plot(abc, linestyle='-',label='ABC')
plt.plot(dikstra, linestyle='-',label='DIJKSTRA')
plt.legend()
plt.grid(True)
plt.show()

print('Total Distance :')
print('Dijkstra : ',dikstra.sum())
print('Artificial bee Colony : ',abc.sum())
print('Mean Distance')
print('Dijkstra : ',dikstra.mean())
print('Artificial bee Colony : ',abc.mean())