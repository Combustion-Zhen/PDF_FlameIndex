"""
Zhen Lu 2017/07/15 <albert.lz07@gmail.com>

A script to calculate the ratio of mass flow rate between oxidizer and fuel 
for the PaSR calculation.

Set a mixing extent factor x,
fuel stream is made of
    (1-x/2) FUEL + nu x/2 AIR
oxydizer stream is name fo
    nu (1-x/2) AIR + x/2 FUEL

The ratio of mass flow rates is calculated as

        nu(1-x/2)*M_air + phi*x/2*M_fuel
r_m = -----------------------------------
        phi*(1-x/2)*M_fuel+nu*x/2*M_air

"""

import numpy as np

# target equivalence ratio
phi = 1
# stoichiometric coefficient
nu = 0.5
# Mass of one mole fuel H2:N2 1:1
m_fuel = 2+28
# Mass of stoichiometric oxidizer
m_air = 32 + 3.76*28

for x in np.arange(0.1,1.0,0.1):
    f_f = phi*(1-x/2)
    f_o = nu*x/2
    o_f = phi*x/2
    o_o = nu*(1-x/2)
    r_m = (o_o*m_air+o_f*m_fuel)/(f_f*m_fuel+f_o*m_air)

    print(x,r_m,f_f,f_o,o_f,o_o)
