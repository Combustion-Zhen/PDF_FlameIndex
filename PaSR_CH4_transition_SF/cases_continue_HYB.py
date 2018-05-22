"""
Zhen Lu 2017/11/03
Continue the PaSR cases, modify some parameters
"""

import os
import copy
import shutil
import subprocess
import numpy as np
from counterflow_file import params2name

mixing_models = {'IEMHYB':4,
                 'EMSTHYB':6,
                 'IEM':7,
                 'EMST':9}
tau_log = np.linspace(-4,-2,11)
mix_res_ratio = [0.3,]
equiv_ratio = [1.0,]

params = {}

for mix_k, mix_v in mixing_models.items():
    params['MIX'] = mix_k
    for tres_log in tau_log:
        tres = np.power( 10., tres_log )
        params['tres'] = tres_log
        for tmix_ratio in mix_res_ratio:
            params['tmix'] = tmix_ratio
            for eqv in equiv_ratio:
                params['eqv'] = eqv

                case = params2name(params)

                if os.path.isdir(case):
                    print(case)
                    os.chdir(case)
                    
                    with open('pasr.nml','r') as f:
                        lines = f.readlines()

                    with open('pasr.nml','w') as f:
                        for line in lines:
                            if line.startswith('anres'):
                                line = 'anres=20\n'
                            if line.startswith('part_in'):
                                line = 'part_in=.true.\n'
                            if line.startswith('full_op'):
                                line = 'full_op=.true.\n'
                            if line.startswith('full_fi'):
                                line = 'full_fi=.true.\n'
                            f.write(line)

                    #run(['sbatch','run_shaheen.sh'])
                    subprocess.Popen('PaSR_PPF_MIX &> pasr.op',shell=True)

                    os.chdir('..')

