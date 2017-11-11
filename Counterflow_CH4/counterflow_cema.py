"""
Zhen Lu 2017/11/11

CEMA on the counterflow flame results
"""

import os
import numpy as np
from subprocess import run
from counterflow_file import *

# read the species names from chem.inp, guarantee the sequence
comp_names = []
spe_end = False
with open('chem.inp','r') as f:
    for line in f:
        if line[:7] == 'SPECIES':
            while True:
                newline = f.readline()[:-1].split()
                if newline[0] == 'END':
                    break
                else:
                    comp_names.extend(newline)
            break
comp_names.append('T')

phif = [1.3, 1.5, 1.7, 2.0, 2.3, 3.2, 4.8, 9.5, float('inf')]
phio = [0.02, 0.05, 0.1, 0.2, 0.3]
strain = [100, 150, 200, 250, 300]

folder_params = {}
folder_params['phif'] = None
folder_params['phio'] = None

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = None
flame_params['phif'] = None
flame_params['phio'] = None
flame_params['tf'] = 300
flame_params['to'] = 300

# loop over phif
#folder_params['phio'] = 0
#flame_params['phio'] = 0
#for phi in phif:
#    folder_params['phif'] = phi
#    flame_params['phif'] = phi

# loop over phio
folder_params['phif'] = float('inf')
flame_params['phif'] = float('inf')
for phi in phio:
    folder_params['phio'] = phi
    flame_params['phio'] = phi

    folder = params2name(folder_params)
    os.chdir(folder)

    for a in strain:
        flame_params['a'] = a
        case = params2name(flame_params)

        file_name = '{}.dat'.format(case)

        with open(file_name,'r') as f:
            f.readline()
            f.readline()
            f.readline()

            name_str = f.readline()[:-1].split()

        data = np.genfromtxt(file_name,skip_header=3,names=True)
        data_names = data.dtype.names

        dt = {'names':comp_names,
              'formats':[np.float64]*len(comp_names)}
        data_cema = np.zeros(len(data['Z']),dtype=dt)

        for name in comp_names:
            data_cema[name] = data[data_names[name_str.index(name)]]

        np.savetxt('cema.inp',data_cema)

        run(['CEMA_driver'])

        os.rename('cema.op','{}.cema'.format(case))

    os.chdir('..')

