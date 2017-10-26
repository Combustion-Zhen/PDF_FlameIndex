"""
Zhen Lu 2017/10/25

Driver to loop over phif
"""

import numpy as np
from counterflow_flame import counterflow_flame

# run cases
strain = 100.
phif = [1.3, 1.5, 1.7, 2.0, 2.3, 2.7, 3.2, 2.8, 4.8, 7.0, 9.5, float('inf')]
phio = np.arange(0.1,0.6,0.1)

for phi in phif:
    counterflow_flame(strain_rate=strain,phi_f=phi)

for phi in phio:
    counterflow_flame(strain_rate=strain,phi_o=phi)
