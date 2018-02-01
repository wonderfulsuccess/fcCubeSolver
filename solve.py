import subprocess
from video import webcam
import numpy as np

state = webcam.scan()
cube_status = ''
cube_status += ''.join(state['Y'])
cube_status += ''.join(state['G'])
cube_status += ''.join(state['R'])
cube_status += ''.join(state['W'])
cube_status += ''.join(state['B'])
cube_status += ''.join(state['O'])

print(cube_status)

subprocess.call("node ./app.js "+str(cube_status), shell=True)