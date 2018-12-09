"""
Zhen Lu 2017/07/12 <albert.lz07@gmail.com>

A script to calculate the dilution mole number to make the Z_st constant

Fuel side component: Fuel, Air, Dilute
Oxydizer side component: Fuel, Air

Reference case for non premixed flame:
    Fuel side: H2:N2 = 1:1
    Air side: Air (O2:N2 = 1:3.76)

Mole number of fuel is fixed as 1
"""

# target equivalence ratio
phi = 1
# mole of air with 1 mole of fuel
mole_air = 0.1
# fuel
m_fuel = 2
# dilute
mole_dilute_ref = 1
m_dilute = 28
# oxy
m_oxy = 32+3.76*28
# stoichiometric for fuel
mole_oxy_st = 0.5

Z_st = (m_fuel+mole_dilute_ref*m_dilute) \
      /(m_fuel+mole_dilute_ref*m_dilute+mole_oxy_st*m_oxy)

mole_dilute = ((Z_st-1)*m_fuel+(Z_st*mole_oxy_st-mole_air)*m_oxy) \
             /((1-Z_st)*m_dilute)

print(mole_dilute)
