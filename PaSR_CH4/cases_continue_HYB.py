"""
Zhen Lu 2017/11/03
Continue the PaSR cases, modify some parameters
"""

import os
import copy
import shutil
from subprocess import run
from counterflow_file import params2name

#mixing_models = {'IEM':7,'MC':8,'EMST':9}
#time_res = [4.e-3, 1.e-2]
#mix_res_ratio = [0.02, 0.05, 0.1, 0.2, 0.5]
#equiv_ratio = [1.0, 1.2]
#Zf_variance = [0.01, 0.02, 0.05, 0.1]
#dtmix = [0.01, 0.04]

mixing_models = {'IEMHYB':4,'MCHYB':5,'EMSTHYB':6}
time_res = [1.e-2,]
mix_res_ratio = [0.02, 0.05, 0.1, 0.2, 0.5]
equiv_ratio = [1.0, 1.2, 1.4]
Zf_variance = [0.02, 0.05, 0.1]
dtmix = [0.01,]
phif=[4.76,]

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
                        for phi in phif:
                            params['phif']=phi
                        

                            case = params2name(params)

                            if os.path.isdir(case):
                                print(case)
                                shutil.copy('template/flame_C.dat',case)
                                shutil.copy('template/flame_Z.dat',case)
                                shutil.copy('template/flame_chi.dat',case)
                                os.chdir(case)
                                
                                with open('pasr.nml','r') as f:
                                    lines = f.readlines()

                                with open('pasr.nml','w') as f:
                                    for line in lines:
                                        if line[:7]=='part_in':
                                            line = 'part_in=.true.\n'
                                        if line[:6]=='mxmode':
                                            line = 'mxmode={:d}\n'.format(mix_v)
                                        f.write(line)

                                run(['sbatch','run_shaheen.sh'])

                                os.chdir('..')

Zf_variance = [0.02, 0.04]
phif=[2,]

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
                        for phi in phif:
                            params['phif']=phi
                        

                            case = params2name(params)

                            if os.path.isdir(case):
                                print(case)
                                shutil.copy('template/flame_C.dat',case)
                                shutil.copy('template/flame_Z.dat',case)
                                shutil.copy('template/flame_chi.dat',case)
                                os.chdir(case)
                                
                                with open('pasr.nml','r') as f:
                                    lines = f.readlines()

                                with open('pasr.nml','w') as f:
                                    for line in lines:
                                        if line[:7]=='part_in':
                                            line = 'part_in=.true.\n'
                                        if line[:6]=='mxmode':
                                            line = 'mxmode={:d}\n'.format(mix_v)
                                        f.write(line)

                                run(['sbatch','run_shaheen.sh'])

                                os.chdir('..')
