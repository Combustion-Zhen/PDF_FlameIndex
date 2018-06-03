"""
Zhen Lu 2017/10/25

Driver to loop over phif
"""

import numpy as np
from counterflow_flame import counterflow_flame
from counterflow_file import params2name

# run cases
strain = [200.,]
phif = [1.3, 1.5, 1.7, 2.3, 3.2, 4.8, 9.5]
phio = [0.2, 0.4, 0.6]

# parameters
flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1.
flame_params['a'] = None
flame_params['phif'] = None
flame_params['phio'] = None
flame_params['tf'] = 300.
flame_params['to'] = 300.

case_name = None

for a in strain:
    flame_params['a'] = a
    for f in phif:
        flame_params['phif'] = f
        for o in phio:
            flame_params['phio'] = o

            case_name = params2name(flame_params)
            counterflow_flame(strain_rate = a,
                              phi_f = f,
                              phi_o = o
                             )

