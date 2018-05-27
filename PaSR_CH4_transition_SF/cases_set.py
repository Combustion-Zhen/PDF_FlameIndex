"""
Zhen Lu 2018/05/20
A python script to generate cases for PaSR simulations of
the Sandia flame, three streams provided
"""

import numpy as np
import re
import os
import shutil
import subprocess
from counterflow_file import params2name

global Zst
# constants
Zst = 0.05518
m_pilot = 1.
m_fuel = 4.88
equiv_ratio_pilot = 0.77
equiv_ratio_fuel = 3.17

L = 30*7.2/1000

def equiv2Z( phi ):
    a = phi*Zst/(1.-Zst)
    Z = a/(1.+a)
    return Z

def air_flow_rate( Zf, Z ):
    return (Zf - Z)/Z

mixing_models = {'IEMHYB':4,
                 'EMSTHYB':6,
                 'IEM':7,
                 'EMST':9}

#tau_log = np.linspace(-3.9,-2.1,10)
tau_log = np.array([-3.65,])
mix_res_ratio = [0.2,]
equiv_ratio = [1.0,]

dtmix = 0.01
dtres = 0.01
isave = 100
restart = '.false.'
full_op = '.false.'
full_fi = '.false.'
bin_op = '.false.'

with open('template/pasr.nml','r') as template:
    lines_nml = template.readlines();
with open('template/run_shaheen.sh','r') as template:
    lines_job = template.readlines();

# case name string is combined with case parameters, in the sequence
# mixing model, tres, tmix/tres, equivalence ratio, variance of Zf
params = {}
for mix_k, mix_v in mixing_models.items():
    params['MIX'] = mix_k
    for tres_log in tau_log:
        tres = np.power( 10., tres_log )
        params['tres'] = tres_log
        for tmix_ratio in mix_res_ratio:
            tmix = tmix_ratio*tres
            params['tmix'] = tmix_ratio
            for phi in equiv_ratio:
                params['eqv'] = phi

                Z_fuel = equiv2Z( equiv_ratio_fuel )
                Z_pilot = equiv2Z( equiv_ratio_pilot )

                Z_fp = (Z_fuel*m_fuel+Z_pilot*m_pilot)/(m_fuel+m_pilot)

                m_air = air_flow_rate(Z_fp,equiv2Z(phi))*(m_fuel+m_pilot)

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
                                '{:g}'.format(m_air),
                                line)
                        line = re.sub('@ZFMEAN@',
                                '{:g}'.format(Z_fuel),
                                line)
                        line = re.sub('@CDTRP@',
                                '{:g}'.format(dtres),
                                line)
                        line = re.sub('@SAVESTEP@',
                                '{:d}'.format(isave),
                                line)
                        line = re.sub('@CDTMIX@',
                                '{:g}'.format(dtmix),
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
                        line = re.sub('@BINOP@',
                                bin_op,
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
                shutil.copy('streams_init.in','streams.in')
                subprocess.run('PaSR_particles_init')
                shutil.copy('streams_SF.in','streams.in')
                subprocess.Popen('PaSR_PPF_MIX')

                os.chdir('..')
