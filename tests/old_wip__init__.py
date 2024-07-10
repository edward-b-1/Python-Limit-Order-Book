import sys
import os

d = os.path.abspath('.')

with open('tmpf.txt', 'w') as f:
    f.write(f'test...\n')
    f.write(f'{d}\n')
    f.flush()

extra_dir = f'{d}/Python'

with open('tmpf.txt', 'a') as f:
    f.write(f'adding extra dir to PYTHONPATH\n')
    f.write(f'{extra_dir}\n')
    f.flush()

sys.path.append(extra_dir)

with open('tmpf.txt', 'a') as f:
    PYTHONPATH = os.environ['PYTHONPATH']
    f.write(f'PYTHONPATH={PYTHONPATH}\n')
    f.flush()