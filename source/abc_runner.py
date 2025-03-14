import subprocess
import time

script = 'abc_all.py'
# Run each script
for i in range(15):

    print(f'\n ========= Running {i+1} loop ===========')
    subprocess.run(['python', script])