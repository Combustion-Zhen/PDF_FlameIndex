"""
Zhen Lu 2017/10/27

A driver to loop over the strain rate of counterflow flames
"""

import numpy as np
import sys
from counterflow_flame import counterflow_flame
from counterflow_file import params2name

strain_init = 100.
strain_max = 1000.
strain_diff_min = 0.1

base = 10.
factor = 0.2

# parameters
flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1.
flame_params['a'] = strain_init
flame_params['phif'] = 'inf'
flame_params['phio'] = 0.
flame_params['tf'] = 300.
flame_params['to'] = 300.

case_name = params2name(flame_params)

strain = strain_init

info = counterflow_flame(strain_rate = strain,
        phi_f = flame_params['phif'],
        phi_o = flame_params['phio'],
        solution = '{}.xml'.format(case_name) )

if info != 0:
    sys.exit('Initialization fail')

while True :

    if info == 0 :
        print('strain rate = {:g} success'.format(strain))
        flame_params['a'] = strain
        case_name = params2name(flame_params)
    elif info == -1 :
        print('strain rate = {:g} fail'.format(strain))
        factor /= 1.5
    elif info == 1 :
        print('strain rate = {:g} extinct'.format(strain))
        factor /= 1.5

    strain = flame_params['a'] * np.power( base, factor )
    print('New strain rate = {:g}'.format(strain))
    strain_diff = strain - flame_params['a']

    if strain > strain_max or strain_diff < strain_diff_min:
        break

    info = counterflow_flame(strain_rate = strain,
            phi_f = flame_params['phif'],
            phi_o = flame_params['phio'],
            solution = '{}.xml'.format(case_name) )
