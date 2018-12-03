import numpy as np
import os
import sys
sys.path.append('/home/luz0a/Documents/PDF_FlameIndex/CounterflowFlame')
from filename import params2name
from counterflow_flame import counterflowPartiallyPremixedFlame

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

strain = strain_init
solution = None

while True :

    info = counterflowPartiallyPremixedFlame(
            strain_rate = flame_params['a'],
            phi_f = flame_params['phif'],
            phi_o = flame_params['phio'],
            solution = solution )

    case_name = params2name(flame_params)
    file_name = '{}.xml'.format(case_name)

    if info == 0 :
        print('strain rate = {:g} success'.format(flame_params['a']))
        solution = file_name
        strain = flame_params['a']
    elif info == -1 :
        print('strain rate = {:g} fail'.format(flame_params['a']))
        factor /= 1.5
    elif info == 1 :
        print('strain rate = {:g} extinct'.format(flame_params['a']))
        os.remove(file_name)
        factor /= 1.5

    flame_params['a'] = strain * np.power( base, factor )
    strain_diff = flame_params['a'] - strain

    if strain > strain_max or strain_diff < strain_diff_min:
        break
