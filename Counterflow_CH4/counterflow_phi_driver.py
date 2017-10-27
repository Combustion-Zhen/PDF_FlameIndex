"""
Zhen Lu 2017/10/25

Driver to loop over phif
"""

import numpy as np
from counterflow_flame import counterflow_flame, params2name

# run cases
strain = [100., 150., 200., 250., 270., 280., 290., 300.]
phif = [1.3, 1.5, 1.7, 2.3, 3.2, 4.8, 9.5, float('inf')]
phio = [0.02, 0.05, 0.1, 0.2, 0.3]

# parameters
flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1.
flame_params['a'] = 100.
flame_params['phif'] = 'inf'
flame_params['phio'] = 0.
flame_params['tf'] = 300.
flame_params['to'] = 300.

case_name = None

for a in strain:

    for phi in phif:
        flame_params['phio'] = 0.
        flame_params['phif'] = phi
        case_name = params2name(flame_params)
        counterflow_flame(strain_rate = a,
                phi_f = phi, phi_o = 0.,
                solution = '{}.xml'.format(case_name))

    for phi in phio:
        flame_params['phio'] = phi
        flame_params['phif'] = 'inf'
        case_name = params2name(flame_params)
        counterflow_flame(strain_rate = a,
                phi_f = 'inf', phi_o = phi,
                solution = '{}.xml'.format(case_name))

    flame_params['a'] = a
