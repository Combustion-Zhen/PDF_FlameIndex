"""
An opposed-flow methane/air counterflow flame


"""

import cantera as ct
import numpy as np

################################################################################
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
# post-processing

# Calculate Bilger's mixture fraction

# fuel
gas.TPX = tin_f, p, comp_f
YC_f = gas.elemental_mass_fraction('C')
YH_f = gas.elemental_mass_fraction('H')
YO_f = gas.elemental_mass_fraction('O')

comp_fuel = np.hstack((gas.T,gas.Y))
fuel_str = ' '.join([format(x, '12.6e') for x in comp_fuel])

# oxidizer
gas.TPX = tin_o, p, comp_o
YC_o = gas.elemental_mass_fraction('C')
YH_o = gas.elemental_mass_fraction('H')
YO_o = gas.elemental_mass_fraction('O')

comp_oxy = np.hstack((gas.T,gas.Y))
oxy_str = ' '.join([format(x, '12.6e') for x in comp_oxy])

# stoichiometric mixture
comp_st = {}
comp_st[fuel_name] = 1
for k, v in comp_o.items():
    comp_st[k] = v*stoich_nu

gas.TPX = tin_o, p, comp_st
YC_st = gas.elemental_mass_fraction('C')
YH_st = gas.elemental_mass_fraction('H')
YO_st = gas.elemental_mass_fraction('O')

Zst = (2.*(YC_st-YC_o)/gas.atomic_weight('C')
        +(YH_st-YH_o)/2./gas.atomic_weight('H')
        -(YO_st-YO_o)/gas.atomic_weight('O')) / \
        (2.*(YC_f-YC_o)/gas.atomic_weight('C')
        +(YH_f-YH_o)/2./gas.atomic_weight('H')
        -(YO_f-YO_o)/gas.atomic_weight('O'))

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

Z1st = (2.*(YC_st-YC_o)/gas.atomic_weight('C')
        +(YH_st-YH_o)/2./gas.atomic_weight('H')
        -(YO_st-YO_o)/gas.atomic_weight('O')) / \
        (2.*(YC_f-YC_o)/gas.atomic_weight('C')
        +(YH_f-YH_o)/2./gas.atomic_weight('H')
        -(YO_f-YO_o)/gas.atomic_weight('O'))

Z1 = (2.*(YC-YC_o)/gas.atomic_weight('C')
         +(YH-YH_o)/2./gas.atomic_weight('H')
         -(YO-YO_o)/gas.atomic_weight('O')) / \
         (2.*(YC_f-YC_o)/gas.atomic_weight('C')
         +(YH_f-YH_o)/2./gas.atomic_weight('H')
         -(YO_f-YO_o)/gas.atomic_weight('O'))

# progress variable
# C_o: mass fractio of O in products CO2, CO, H2O
# C_4spe: mass fraction of CO2, CO, H2O, H2
# C_2spe: mass fraction of CO2 and CO

index_H2O = gas.species_index('H2O')
index_CO2 = gas.species_index('CO2')
index_CO = gas.species_index('CO')
index_H2 = gas.species_index('H2')

MW_H2O = gas.molecular_weights[index_H2O]
MW_CO2 = gas.molecular_weights[index_CO2]
MW_CO = gas.molecular_weights[index_CO]
MW_H2 = gas.molecular_weights[index_H2]

C_o = gas.atomic_weight('O')*(f.Y[index_H2O]/MW_H2O
        +2.*f.Y[index_CO2]/MW_CO2
        +f.Y[index_CO]/MW_CO)

C_4spe = f.Y[index_CO2]+f.Y[index_CO]+f.Y[index_H2O]+f.Y[index_H2]

C_2spe = f.Y[index_CO2]+f.Y[index_CO]

# heat release rate
Q = f.heat_release_rate

################################################################################
# output

data = np.column_stack((f.grid,f.T,f.Y.transpose(),
    Z,Z1,C_o,C_4spe,C_2spe,Q,alpha,nu))
data_names = (['grid','T']
        +gas.species_names
        +['Z','Z1','C_o','C_4spe','C_2spe','Q','alpha','nu'])

np.savetxt('{}.dat'.format(case_name),
        data,
        header=('FUEL: {0}\nOXIDIZER: {1}\n'.format(fuel_str,oxy_str)
            +'Zst = {:g}; Z1st = {:g}\n'.format(Zst,Z1st)
            +' '.join(data_names)),
        comments='')
