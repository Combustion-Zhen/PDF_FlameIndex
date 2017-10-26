"""
An opposed-flow methane/air counterflow flame
"""

import cantera as ct
import numpy as np

def counterflow_flame(mech='gri30.xml', transport='Multi', flag_soret = True,
        fuel_name='CH4', strain_rate=100., width=0.01, p=1.,
        phi_f=10., phi_o=0., tin_f=300., tin_o=300.):

################################################################################
# Create the gas object used to evaluate all thermodynamic, kinetic, and
# transport properties.
    gas = ct.Solution('gri30.xml', 'gri30_mix')
    p *= ct.one_atm  # pressure

    case_name = '{0}_p{1:g}_a{2:g}_phif{3:g}_phio{4:g}_tf{5:g}_to{6:g}' \
            .format(fuel_name,p/ct.one_atm,strain_rate,phi_f,phi_o,tin_f,tin_o)

## parameters of the counterflow flame
## a = (U_f+U+o)/width
#strain_rate = 100 # 1/s
#
#width = 0.01 # Distance between inlets is 2 cm
#
## single fuel
#fuel_name = 'CH4'
#
#phi_f = 1.7 # equivalence ratio of the fuel side stream
#phi_o = 0.  # equivalence ratio of the oxidizer side stream
#
#tin_f = 300.0  # fuel inlet temperature
#tin_o = 300.0  # oxidizer inlet temperature
#
################################################################################

    oxy = {'O2':1., 'N2':3.76}  # air composition

    fuel_index = gas.species_index(fuel_name)

    stoich_nu = gas.n_atoms(fuel_index,'C')+gas.n_atoms(fuel_index,'H')/4.

    comp_f = {}
    comp_f[fuel_name] = 1
    if phi_f < 10.0 :
        for k, v in oxy.items():
            comp_f[k] = v*stoich_nu/phi_f

    comp_o = oxy
    comp_o[fuel_name] = phi_o

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
    f.transport_model = transport

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
    try:
        f.solve(loglevel=0, auto=True)
    except Exception as e:
        print('Error: not converge for case:',e)

    if flag_soret:
        f.soret_enabled = True
        try:
            f.solve(loglevel=0, auto=True)
        except Exception as e:
            print('Error: not converge for case:',e)

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
    for k, v in oxy.items():
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

    gas.TPX = tin_o, p, oxy
    YC_o = gas.elemental_mass_fraction('C')
    YH_o = gas.elemental_mass_fraction('H')
    YO_o = gas.elemental_mass_fraction('O')

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

if __name__ == '__main__':
    counterflow_flame()
