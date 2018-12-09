"""
Zhen Lu 2017/10/31
A python script to generate cases for PaSR simulations of
partially premixed combution
"""

import numpy as np
import re
import os
import shutil
import subprocess
from counterflow_file import params2name

global Zst

def equiv2Z( phi ):
    a = phi*Zst/(1.-Zst)
    Z = a/(1.+a)
    return Z

def air_flow_rate( Zf, Z ):
    return (Zf - Z)/Z

# constants
Zst = 0.05518

mixing_models = {'IEMHYB':4,
                 'EMSTHYB':6,
                 'IEM':7,
                 'EMST':9}

time_res = [1.e-2,]
mix_res_ratio = [0.02, 0.035, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
equiv_ratio_f = [4.76,]
equiv_ratio = [1.0,]
Zf_variance = [0.1,]
dtmix = [0.01,]

dtres = 0.01
isave = 100
restart = '.false.'
full_op = '.false.'
full_fi = '.false.'

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
            for phif in equiv_ratio_f:
                Zf = equiv2Z( phif )
                for phi in equiv_ratio:
                    params['eqv'] = phi
                    air_rate = air_flow_rate( Zf, equiv2Z( phi ) )
                    for var in Zf_variance:
                        params['Zfvar'] = var
                        for dt in dtmix:
                            params['dtmix'] = dt
                            params['phif'] = phif

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
                                    line = re.sub('@CDTRP@',
                                            '{:g}'.format(dtres),
                                            line)
                                    line = re.sub('@SAVESTEP@',
                                            '{:d}'.format(isave),
                                            line)
                                    line = re.sub('@CDTMIX@',
                                            '{:g}'.format(dt),
                                            line)
                                    line = re.sub('@RESTART@',
                                            restart,
                                            line)
                                    line = re.sub('@FULLOP@',
                                            full_op,
                                            line)
                                    line = re.sub('@FULLFI@',
                                            full_fi,
                                            line)
                                    nml.write(line)
                            # job script
                            with open('run_shaheen.sh','w') as job:
                                for line in lines_job:
                                    line = re.sub('@JOBNAME@',
                                            case,
                                            line)
                                    job.write(line)

                            #subprocess.run(['sbatch','run_shaheen.sh'])
                            subprocess.Popen('PaSR_PPF_MIX &> pasr.op',shell=True)

                            os.chdir('..')
