"""
Zhen Lu 2017/10/31
A python script to generate cases for PaSR simulations of
partially premixed combution
"""

import numpy as np
import re
import os
import shutil
from subprocess import run
from counterflow_file import params2name

global Zst, Phif, Zf

def equiv2Z( Phi ):
    a = Phi*Zst/(1.-Zst)
    Z = a/(1.+a)
    return Z

def air_flow_rate( Z ):
    return (Zf - Z)/Z

# constants
CH4 = 16.043
O2 = 31.999
N2 = 28.013
Zst = 0.05518
Phif = 4.76
Zf = equiv2Z( Phif )

print('{:g}'.format(air_flow_rate(Zst)))


mixing_models = {'IEM':1,'MC':2,'EMST':3}
time_res = np.array([4.e-3,])
max_res_ratio = 50.
mix_res_ratio = np.array([0.02, 0.03, 0.05, 0.07, 0.1, 0.2, 0.3, 0.5])
equiv_ratio = [0.8, 1.0, 1.2, 1.5, 2.0]
Zf_variance = [0.01, 0.02, 0.05, 0.1]

with open('template/pasr.nml','r') as template:
    lines_nml = template.readlines();
with open('template/run_shaheen.sh','r') as template:
    lines_job = template.readlines();

# case name string is combined with case parameters, in the sequence
# mixing model, tres, tmix/tres, equivalence ratio, variance of Zf
params = {}
for mix_k, mix_v in mixing_models.items():
    params['MIX'] = mix_k
    for tres in time_res:
        params['tres'] = tres
        for tmix_ratio in mix_res_ratio:
            tmix = tmix_ratio*tres
            params['tmix'] = tmix_ratio
            for Phi in equiv_ratio:
                params['eqv'] = Phi
                air_rate = air_flow_rate( equiv2Z( Phi ) )
                for var in Zf_variance:
                    params['Zfvar'] = var
                    case = params2name(params)

if os.path.isdir(case):
    shutil.rmtree(case)
shutil.copytree('template',case)
os.chdir(case)

# pasr namelist
with open('pasr.nml','w') as nml:
    for line in lines_nml:
        line = re.sub('@MIXMODEL@',
                '{:g}'.format(mix_v),
                line)
        line = re.sub('@TRES@',
                '{:e}'.format(tres),
                line)
        line = re.sub('@TMIX@',
                '{:e}'.format(tmix),
                line)
        line = re.sub('@AIRRATE@',
                '{:g}'.format(air_rate),
                line)
        line = re.sub('@ZFMEAN@',
                '{:g}'.format(Zf),
                line)
        line = re.sub('@ZFVAR@',
                '{:g}'.format(var),
                line)
        nml.write(line)
# job script
with open('run_shaheen.sh','w') as job:
    for line in lines_job:
        line = re.sub('@JOBNAME@',
                case,
                line)
        job.write(line)

os.chdir('..')
