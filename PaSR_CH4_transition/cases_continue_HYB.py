"""
Zhen Lu 2017/11/03
Continue the PaSR cases, modify some parameters
"""

import os
import copy
import shutil
import subprocess
from counterflow_file import params2name

mixing_models = {'IEMHYB':4,
                 'EMSTHYB':6,
                 'IEM':7,
                 'MC':8,
                 'EMST':9}

time_res = [1.e-2,]
mix_res_ratio = [0.02, 0.035, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
equiv_ratio_f = [4.76,]
equiv_ratio = [1.2,]
Zf_variance = [0.1,]
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
                                        if line.startswith('anres'):
                                            line = 'anres=50\n'
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

