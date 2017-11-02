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
mean = 0.0551863

for file_name in glob.glob('*.sample'):
    flame = file_name[:file_name.find('.sample')]
    print(flame)
    params = name2params(flame)

    particles = np.genfromtxt(file_name)
    chi = np.average(particles[:,-1])

    # edit input
    with open('input','w') as f:
        f.write('{0}\n{1}\n'.format(file_name,params['F']))
        f.write('{0:12.5f}{1:12.5f}{2:12.5f}\n'.format(mean,params['var'],chi))

    for i, model in enumerate( models ):
        # edit the pasr.nml
        with open('mix.nml','r') as f:
            nml = f.read()
        nml_n = '{0}{1}{2}'.format(nml[:nml.find('mxmode')+7],
                                   i+1,
                                   nml[nml.find('mxmode')+8:])
        with open('mix.nml','w') as f:
            f.write(nml_n)

        # run the mixing
        run(["Mixing"])
