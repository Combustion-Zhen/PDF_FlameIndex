"""
Zhen Lu 2017/10/25

Driver to loop over phif
"""

import numpy as np
from counterflow_flame import counterflow_flame

# run cases
strain = 100.
phif = [1.3, 1.5, 1.7, 2.3, 3.2, 4.8, 9.5, float('inf')]
phio = [0.02, 0.05, 0.1, 0.2, 0.3]
#phio = [0.02, 0.05]

for phi in phif:
    counterflow_flame(strain_rate=strain,phi_f=phi)

for phi in phio:
    counterflow_flame(strain_rate=strain,phi_o=phi)
