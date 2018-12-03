import numpy as np
import os
import sys
sys.path.append('/home/luz0a/Documents/PDF_FlameIndex/CounterflowFlame')
from filename import params2name
from counterflow_flame import counterflowPartiallyPremixedFlame

strain_list = np.array([50, 100, 200, 400])

# parameters
flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1.
flame_params['a'] = 100.
flame_params['phif'] = 'inf'
flame_params['phio'] = 0.
flame_params['tf'] = 300.
flame_params['to'] = 300.

solution = None

for a in strain_list:

    flame_params['a'] = a
    case_name = params2name(flame_params)
    file_name = '{}.xml'.format(case_name)

    info = counterflowPartiallyPremixedFlame(
            strain_rate = flame_params['a'],
            phi_f = flame_params['phif'],
            phi_o = flame_params['phio'],
            solution = solution )

    if info == 0 :
        print('strain rate = {:g} success'.format(flame_params['a']))
        solution = file_name
    elif info == -1 :
        print('strain rate = {:g} fail'.format(flame_params['a']))
        break
    elif info == 1 :
        print('strain rate = {:g} extinct'.format(flame_params['a']))
        os.remove(file_name)
        break
