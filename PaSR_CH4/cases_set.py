"""
Zhen Lu 2017/10/21
A python script to generate cases for PaSR simulations of soot
"""

import numpy as np
import re
import os
from subprocess import run

mixing_models = ('IEM','MC','EMST')
time_res = np.array([2.e-3,])
max_res_ratio = 50.
mix_res_ratio = np.power(10., np.arange(-2,0,0.25))
num_particles = {1600:5,}
mom_methods = {'MOMIC':(1,6),'CQMOM':(4,6)}
#mom_methods = {'SEMI':(0,2),'MOMIC':(1,6),'HMOM':(2,7),'DQMOM':(3,4),'CQMOM':(4,6)}
soot_mix = {'off':'.true.','on':'.false.'}
stoich_fuel_rate = 0.066719
equiv_ratio = [0.5, 0.8, 1.0, 1.5, 2.0]

with open('input_template','r') as template:
    lines = template.readlines();
with open('run_shaheen_template.sh','r') as template:
    lines_job = template.readlines();

# case name string is combined with case parameters, in the sequence
# MOM method, Mixing model, Equivalence ratio, Residence time,
# Mixing time, Number of particles, Soot mixing flag
case_param = [None]*7
for mom, mom_v  in mom_methods.items():
    case_param[0] = mom
    for mix in mixing_models:
        case_param[1] = mix
        for phi in equiv_ratio:
            fuel_rate = phi*stoich_fuel_rate
            case_param[2] = 'phi{:.1f}'.format(phi)
            for tres in time_res:
                tmax = max_res_ratio*tres
                case_param[3] = 'tres{:.3e}'.format(tres)
                for tmix_ratio in mix_res_ratio:
                    tmix = tmix_ratio*tres
                    case_param[4] = 'tmix{:.3e}'.format(tmix)
                    for np, nd in num_particles.items():
                        case_param[5] = 'np{:g}'.format(np)
                        for soot_k, soot_v in soot_mix.items():
                            case_param[6] = 'soot-{}'.format(soot_k)
                            case = '_'.join(case_param)
                            # make case directory
                            os.makedirs(case,exist_ok=True)
                            # set input file
                            with open('input','w') as input:
                                for line in lines:
                                    line = re.sub('@MOMINDEX@',
                                            '{:g}'.format(mom_v[0]),
                                            line)
                                    line = re.sub('@MOMNUM@',
                                            '{:g}'.format(mom_v[1]),
                                            line)
                                    line = re.sub('@MIXMODEL@',
                                            mix,
                                            line)
                                    line = re.sub('@TRES@',
                                            '{:.3e}'.format(tres),
                                            line)
                                    line = re.sub('@TMAX@',
                                            '{:.3e}'.format(tmax),
                                            line)
                                    line = re.sub('@TMIX@',
                                            '{:.3e}'.format(tmix),
                                            line)
                                    line = re.sub('@NP@',
                                            '{:g}'.format(np),
                                            line)
                                    line = re.sub('@NOSOOTMIX@',
                                            soot_v,
                                            line)
                                    line = re.sub('@FUELRATE@',
                                            '{:.8f}'.format(fuel_rate),
                                            line)
                                    input.write(line)
                            # set job script
                            with open('run_shaheen.sh','w') as job:
                                for line in lines_job:
                                    line = re.sub('@JOBNAME@',
                                            case,
                                            line)
                                    line = re.sub('@NUMNODE@',
                                            '{:g}'.format(nd),
                                            line)
                                    job.write(line)
                            # mv to case folder
                            os.rename('input',
                                    '{}/input'.format(case))
                            os.rename('run_shaheen.sh',
                                    '{}/run_shaheen.sh'.format(case))
                            # change directory
                            os.chdir(case)
                            run(['sbatch','run_shaheen.sh'])
                            os.chdir('..')
