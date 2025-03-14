import subprocess

# List of scripts to run
scripts = ['dijkstra.py', 'a_Star.py', 'bellman.py']

# Run each script
for i in range(15):
    print(f'Running {i} Iteration')
    for script in scripts:

        print('Running ' + script)
        subprocess.run(['python', script])


