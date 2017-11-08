"""
Zhen Lu 2017/10/29 <albert.lz07@gmail.com>

Do mixing for the sampled counterflow flame solution
cycle in three mixing models
"""

import glob
import numpy as np
from subprocess import run
from counterflow_file import *

models = ['IEM','MC','EMST']

for file_name in glob.glob('*.sample'):
#for file_name in glob.glob('*_a-300_*.sample'):
    flame = file_name[:file_name.find('.sample')]
    print(flame)
    params = name2params(flame)

    # edit input
    with open('input','w') as f:
        f.write('{0}\n{1}\n'.format(file_name,params['F']))

    for i, model in enumerate( models ):
        # edit the pasr.nml
        print('{}'.format(model))
        with open('mix.nml','r') as f:
            nml = f.readlines()
        with open('mix.nml','w') as f:
            for line in nml:
                if line.startswith('mxmode'):
                    line='mxmode={:d}\n'.format(i+7)
                f.write(line)
        # run the mixing
        run(["Mixing"])
