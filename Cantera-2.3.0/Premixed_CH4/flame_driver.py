"""
Zhen Lu 2017/11/04

A driver script to calculate adiabatic flame with different equivalence ratio
"""

import numpy as np
from adiabatic_flame import adiabatic_flame
from flame_file import *

F = 'CH4'
p = 1
T = 300

phi_lean = np.arange(0.9,0.3,-0.05)
phi_rich = np.arange(1.1,2.5,0.1)

# calculate the flame with equivalence ratio 1 first
adiabatic_flame( fuel_name=F, p=p, T=T, eqv=1 )

# lean mixture
for phi in phi_lean:
    print('Solving equivalence ratio {:g}'.format(phi))
    info = adiabatic_flame( fuel_name=F, p=p, T=T, eqv=phi )
    if info != 0:
        break

# rich mixture
for phi in phi_rich:
    print('Solving equivalence ratio {:g}'.format(phi))
    info = adiabatic_flame( fuel_name=F, p=p, T=T, eqv=phi )
    if info != 0:
        break
