"""
Zhen Lu 2017/10/23
Do ensemble average of eligible cases
"""

import numpy as np
import json
import os

def value_convert(x):
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x

step_start = 1000

param_names = ['MOM','MIX','phi','tres','tmix','np','soot-']
data = {}

# get case list
with open('list_step1500.op','r') as f, open('average.json','w') as output:
    for case in f:
        case = case.replace('\n','')
        os.chdir(case)

        # get parameters
        params = case.split(sep='_')
        for i, param in enumerate(param_names):
            if i <2 :
                data[param] = params[i]
            else:
                value = params[i][len(param):]
                data[param] = value_convert(value)

        # variables
        with open('means.dat','r') as f:
            # depends on the format of the output
            var_names = []
            var_names_raw = f.readline().split()[2:]
            for name in var_names_raw:
                name = name[1:-1]
                var_names.append(name)

        # read data and ensemble average
        vars = np.genfromtxt('means.dat',skip_header=2,names=var_names)

        # Time do not need average
        #names have been modified for numpy
        #print(vars.dtype.names)
        for var in vars.dtype.names:
            data[var] = np.mean(vars[var][step_start:])

        os.chdir('..')

        output.write('{}\n'.format(json.dumps(data)))
