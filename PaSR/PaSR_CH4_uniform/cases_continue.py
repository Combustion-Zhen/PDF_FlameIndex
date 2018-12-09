"""
Zhen Lu 2017/11/03
Continue the PaSR cases, modify some parameters
"""

import os
import copy
import shutil
from subprocess import run
from counterflow_file import params2name

mixing_models = {'IEMHYB':4,
                 'MCHYB':5,
                 'EMSTHYB':6,
                 'IEM':7,
                 'MC':8,
                 'EMST':9}

time_res = [1.e-2, 4.e-3]
mix_res_ratio = [0.05, 0.1, 0.2, 0.5]
equiv_ratio_f = [1.3, 1.5, 1.7, 2.0, 2.3, 3.2, 4.8]
equiv_ratio = [1.0, 1.2]
Zf_variance = [0,]
dtmix = [0.01,]

params = {}

for mix_k, mix_v in mixing_models.items():
    params['MIX'] = mix_k
    for tres in time_res:
        params['tres'] = tres
        for tmix_ratio in mix_res_ratio:
            params['tmix'] = tmix_ratio
            for eqv in equiv_ratio:
                params['eqv'] = eqv
                for var in Zf_variance:
                    params['Zfvar'] = var
                    for dt in dtmix:
                        params['dtmix'] = dt
                        for phi in equiv_ratio_f:
                            params['phif']=phi

                            case = params2name(params)

                            if os.path.isdir(case):
                                print(case)
                                os.chdir(case)
                                
                                with open('pasr.nml','r') as f:
                                    lines = f.readlines()

                                with open('pasr.nml','w') as f:
                                    for line in lines:
                                        if line.startswith('part_in'):
                                            line = 'part_in=.true.\n'
                                        f.write(line)

                                run(['sbatch','run_shaheen.sh'])

                                os.chdir('..')
