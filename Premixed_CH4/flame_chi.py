"""
Zhen Lu 2017/11/04

calculate the scalar dissipation of progress variable defined as
sum of species mass fractions, in the present implementation,
the species counted are CO2, CO, H2O, and H2 by default

input:
    case:       following the rule with params2name
    spe_list:   a list of species names that are used for C

output:
    C:          a three column array, 0: z (m) 1: C 2: chi_C

numpy 1.13 is required, conflict with cantera
"""

import numpy as np

# not normalized, returns z, C, chi
def flame_chi( case, spe_list=None ):
    
    # default value for spe_list
    # CO2 CO H2O H2
    if spe_list is None:
        spe_list = ['CO2','CO','H2O','H2']

    flame = np.genfromtxt('{}.csv'.format(case),delimiter=',',names=True)
    diff = np.genfromtxt('{}_diff.dat'.format(case))

    spe_names = flame.dtype.names[5:]

    C = np.zeros((len(flame),3))
    D = np.zeros(flame.shape)

    C[:,0] = flame['z_m']
    for spe in spe_list:
        C[:,1] += flame[spe]
        D += diff[spe_names.index(spe),:]*flame[spe]

    D /= C[:,1]
    grad = np.gradient(C[:,1],C[:,0])

    C[:,2] = 2*D*(grad**2)
    
    return C

# chi based on normalized value
# returns C, C_n, chi_n
def flame_chi_n( case, spe_list=None ):

    # default value for spe_list
    # CO2 CO H2O H2
    if spe_list is None:
        spe_list = ['CO2','CO','H2O','H2']

    flame = np.genfromtxt('{}.csv'.format(case),delimiter=',',names=True)
    diff = np.genfromtxt('{}_diff.dat'.format(case))
    
    spe_names = flame.dtype.names[5:]

    C = np.zeros((len(flame),3))
    D = np.zeros(flame.shape)

    for spe in spe_list:
        C[:,0] += flame[spe]
        D += diff[spe_names.index(spe),:]*flame[spe]

    D /= C[:,0]

    # normalize progress variable
    C[:,1] = (C[:,0]-C[0,0])/(C[-1,0]-C[0,0])

    grad = np.gradient(C[:,1],flame['z_m'])

    C[:,2] = 2*D*(grad**2)

    return C
