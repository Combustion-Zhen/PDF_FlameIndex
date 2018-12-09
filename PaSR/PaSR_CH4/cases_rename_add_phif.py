"""
Zhen Lu 2017/11/03
add dtmix to folder name
"""

import shutil
from counterflow_file import params2name

mixing_models = ['IEM','MC','EMST']
time_res = [4.e-3, 1.e-2]
mix_res_ratio = [0.02, 0.05, 0.1, 0.2, 0.5]
equiv_ratio = [1.0, 1.2]
Zf_variance = [0.01, 0.02, 0.05, 0.1]
dtmix = [0.01, 0.04]

phif = 4.76

params = {}

for mix in mixing_models:
    params['MIX'] = mix
    for tres in time_res:
        params['tres'] = tres
        for tmix_ratio in mix_res_ratio:
            params['tmix'] = tmix_ratio
            for eqv in equiv_ratio:
                params['eqv'] = eqv
                for var in Zf_variance:
                    params['Zfvar'] = var
                    for dt in dtmix:
                        params['dtmix'] = dt

                        name_old = params2name(params)

                        params['phif'] = phif
                        name_new = params2name(params)

                        shutil.move(name_old,name_new)

                        del params['phif']
