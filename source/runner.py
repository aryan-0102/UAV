import subprocess
import time
# List of scripts to run
scripts = ['order_spread.py', 'dijkstra.py', 'a_Star.py', 'bellman.py', 'abc.py', 'comapre.py']


for script in scripts:

    print('Running ' + script)
    subprocess.run(['python', script])


