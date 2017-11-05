"""
Zhen Lu 2017/11/05
reset the EMST HYBRID cases

1. stop jobid
2. restart
"""

import glob
import os
from subprocess import run

for case in glob.glob('MIX-EMSTHYB_tres-0.01_*'):
    os.chdir(case)

    for outfile in glob.glob('job*.out'):
        jobid = outfile[3:-4]
        # kill possible running cases
        run(['scancel',jobid])

    with open('pasr.nml','r') as f:
        lines = f.readlines()

    # initialize the case
    with open('pasr.nml','w') as f:
        for line in lines:
            if line[:7]=='part_in':
                line = 'part_in=.false.\n'
            f.write(line)

    run(['sbatch','run_shaheen.sh'])

    os.chdir('..')
