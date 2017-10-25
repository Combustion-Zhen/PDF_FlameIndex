"""
An opposed-flow methane/air counterflow flame


"""

import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# parameters of the counterflow flame
# a = (U_f+U+o)/width
strain_rate = 100 # 1/s

width = 0.01 # Distance between inlets is 2 cm

# Create the gas object used to evaluate all thermodynamic, kinetic, and
# transport properties.
gas = ct.Solution('gri30.xml', 'gri30_mix')
p = ct.one_atm  # pressure

# single fuel
fuel_name = 'CH4'

phi_r = 1.3 # equivalence ratio of the fuel side stream

tin_f = 300.0  # fuel inlet temperature
tin_o = 300.0  # oxidizer inlet temperature

case_name = '{0}_p{1:g}_a{2:g}_phir{3:g}_tf{4:g}_to{5:g}'.format(fuel_name,
        p/ct.one_atm,strain_rate,phi_r,tin_f,tin_o)

################################################################################

comp_o = {'O2':1., 'N2':3.76}  # air composition

fuel_index = gas.species_index(fuel_name)

stoich_nu = gas.n_atoms(fuel_index,'C')+gas.n_atoms(fuel_index,'H')/4.

comp_f = {}
comp_f[fuel_name] = 1
if phi_r < 10.0 :
    for k, v in comp_o.items():
        comp_f[k] = v*stoich_nu/phi_r

# fuel and oxidizer streams have the same velocity
u = strain_rate*width/2.

# get mass flow rate
gas.TPX = tin_f, p, comp_o
dens_o = gas.density
mdot_o = u*dens_o

gas.TPX = tin_o, p, comp_f
dens_f = gas.density
mdot_f = u*dens_f  # kg/m^2/s

# Create an object representing the counterflow flame configuration,
# which consists of a fuel inlet on the left, the flow in the middle,
# and the oxidizer inlet on the right.
f = ct.CounterflowDiffusionFlame(gas, width=width)
f.transport_model = 'Multi'

# Set the state of the two inlets
f.fuel_inlet.mdot = mdot_f
f.fuel_inlet.X = comp_f
f.fuel_inlet.T = tin_f

f.oxidizer_inlet.mdot = mdot_o
f.oxidizer_inlet.X = comp_o
f.oxidizer_inlet.T = tin_o

# Set the boundary emissivities
f.set_boundary_emissivities(0.0, 0.0)
# Turn radiation off
f.radiation_enabled = False

f.set_refine_criteria(ratio=2, slope=0.1, curve=0.1, prune=0.01)

# Solve the problem
f.solve(loglevel=0, auto=True)
f.soret_enabled = True
f.solve(loglevel=0, auto=True)

f.save('{}.xml'.format(case_name))

################################################################################

# Calculate Bilger's mixture fraction
gas.TPX = tin_f, p, comp_f
YC_f = gas.elemental_mass_fraction('C')
YH_f = gas.elemental_mass_fraction('H')
YO_f = gas.elemental_mass_fraction('O')

gas.TPX = tin_o, p, comp_o
YC_o = gas.elemental_mass_fraction('C')
YH_o = gas.elemental_mass_fraction('H')
YO_o = gas.elemental_mass_fraction('O')

YC = f.elemental_mass_fraction('C')
YH = f.elemental_mass_fraction('H')
YO = f.elemental_mass_fraction('O')

Z = (2.*(YC-YC_o)/gas.atomic_weight('C')
        +(YH-YH_o)/2./gas.atomic_weight('H')
        -(YO-YO_o)/gas.atomic_weight('O')) / \
        (2.*(YC_f-YC_o)/gas.atomic_weight('C')
        +(YH_f-YH_o)/2./gas.atomic_weight('H')
        -(YO_f-YO_o)/gas.atomic_weight('O'))

# thermal diffusivity
alpha = f.thermal_conductivity/(f.cp_mass*f.density)

# kinetic viscosity
nu = f.viscosity/f.density

# a mixture fraction based on fuel stream is pure CH4
gas.TPX = tin_f, p, {fuel_name:1}
YC_f = gas.elemental_mass_fraction('C')
YH_f = gas.elemental_mass_fraction('H')
YO_f = gas.elemental_mass_fraction('O')

Z1 = (2.*(YC-YC_o)/gas.atomic_weight('C')
         +(YH-YH_o)/2./gas.atomic_weight('H')
         -(YO-YO_o)/gas.atomic_weight('O')) / \
         (2.*(YC_f-YC_o)/gas.atomic_weight('C')
         +(YH_f-YH_o)/2./gas.atomic_weight('H')
         -(YO_f-YO_o)/gas.atomic_weight('O'))

data = np.column_stack((f.grid,f.T,f.Y.transpose(),Z,Z1,alpha,nu))
data_names = ['grid','T']+gas.species_names+['Z','Z1','alpha','nu']

np.savetxt('{}.dat'.format(case_name),
        data,
        header=' '.join(data_names),
        comments='')
