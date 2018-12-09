"""
An opposed-flow hydrogen/air counterflow flame
"""

import cantera as ct
import numpy as np
import sys
from counterflow_file import params2name

def counterflow_flame(mech='gri30.xml', transport='Multi',
        flag_soret = True, flag_radiation = False,
        fuel = {'CH4':1}, oxy = {'O2':1,'N2':3.76},
        strain_rate=100., width=0.01, p=1.,
        phi_f='inf', phi_o=0., tin_f=300., tin_o=300., solution=None):

################################################################################
# Create the gas object used to evaluate all thermodynamic, kinetic, and
# transport properties.
    gas = ct.Solution(mech)

    phi_f = float(phi_f)
    if phi_f <= 1.:
        sys.exit('Equivalence ratio of fuel side {:g}'.format(phi_f))
    if phi_o >= 1.:
        sys.exit('Equivalence ratio of oxidizer side {:g}'.format(phi_o))

    # construct case name
    flame_params = {}
    flame_params['p'] = p
    flame_params['a'] = strain_rate
    flame_params['phif'] = phi_f
    flame_params['phio'] = phi_o
    flame_params['tf'] = tin_f
    flame_params['to'] = tin_o

    case_name = params2name(flame_params)

    p *= ct.one_atm  # pressure
################################################################################

    #fuel = { 'H2':1., 'N2':1. } # fuel composition
    #oxy = {'O2':1., 'N2':3.76}  # air composition

    Z_element = ['C','H','O']
    for e in Z_element:
        if e not in gas.element_names:
            Z_element.remove(e)

    # get stoichiometric coefficients
    element_nu = {'C':2, 'O':-1, 'H':0.5}

    o_fuel = 0.
    for k, v in fuel.items():
        for e in gas.element_names:
            if e in element_nu.keys():
                o_fuel += v*gas.n_atoms(k,e)*element_nu[e]

    o_oxy = 0.
    for k, v in oxy.items():
        for e in gas.element_names:
            if e in element_nu.keys():
                o_oxy += v*gas.n_atoms(k,e)*element_nu[e]

    stoich_nu = -o_fuel/o_oxy

    # composition for two streams
    comp_f = {}
    comp_o = {}

    for k in fuel.keys():
        comp_f[k] = 0.
        comp_o[k] = 0.
    for k in oxy.keys():
        comp_f[k] = 0.
        comp_o[k] = 0.

    for k, v in fuel.items():
        comp_f[k] += v
        comp_o[k] += v*phi_o/stoich_nu

    for k, v in oxy.items():
        comp_o[k] += v
        comp_f[k] += v*stoich_nu/phi_f

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

    if solution is not None:
        try:
            f.restore(solution, loglevel=0)
        except Exception as e:
            print(e,'Start to solve from initialization')

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
        return -1

    if flag_radiation:
        f.radiation_enabled = True
        try:
            f.solve(loglevel=0, auto=True)
        except Exception as e:
            print('Error: not converge for case:',e)
            return -1

    if flag_soret:
        f.soret_enabled = True
        try:
            f.solve(loglevel=0, auto=True)
        except Exception as e:
            print('Error: not converge for case:',e)
            return -1

    f.save('{}.xml'.format(case_name))

################################################################################
# post-processing

    # Calculate Bilger's mixture fraction

    # fuel
    gas.TPX = tin_f, p, comp_f

    z_f = 0
    for e in Z_element:
        z_f += (element_nu[e]
                *gas.elemental_mass_fraction(e)
                /gas.atomic_weight(e))
    
    comp_fuel = np.hstack((gas.T,gas.Y))
    fuel_str = ' '.join([format(x, '12.6e') for x in comp_fuel])

    # oxidizer
    gas.TPX = tin_o, p, comp_o

    z_o = 0
    for e in Z_element:
        z_o += (element_nu[e]
                *gas.elemental_mass_fraction(e)
                /gas.atomic_weight(e))
    
    comp_oxy = np.hstack((gas.T,gas.Y))
    oxy_str = ' '.join([format(x, '12.6e') for x in comp_oxy])

    # stoichiometric mixture
    comp_st = {}

    for k in fuel.keys():
        comp_st[k] = 0.
    for k in oxy.keys():
        comp_st[k] = 0.

    for k, v in fuel.items():
        comp_st[k] += v
    for k, v in oxy.items():
        comp_st[k] += v*stoich_nu

    gas.TPX = tin_o, p, comp_st

    z_st = 0
    for e in Z_element:
        z_st += (element_nu[e]
                 *gas.elemental_mass_fraction(e)
                 /gas.atomic_weight(e))
    
    Zst = (z_st-z_o)/(z_f-z_o)

    z = np.zeros(f.T.shape)
    for e in Z_element:
        z += (element_nu[e]
              *f.elemental_mass_fraction(e)
              /gas.atomic_weight(e))

    Z = (z-z_o)/(z_f-z_o)

# thermal diffusivity
    alpha = f.thermal_conductivity/(f.cp_mass*f.density)

# kinetic viscosity
    nu = f.viscosity/f.density

# a mixture fraction based on fuel stream is pure fuel
    gas.TPX = tin_f, p, fuel

    z_f = 0
    for e in Z_element:
        z_f += (element_nu[e]
                *gas.elemental_mass_fraction(e)
                /gas.atomic_weight(e))

    gas.TPX = tin_o, p, oxy

    z_o = 0
    for e in Z_element:
        z_o += (element_nu[e]
                *gas.elemental_mass_fraction(e)
                /gas.atomic_weight(e))
    
    Z1st = (z_st-z_o)/(z_f-z_o)

    z = np.zeros(f.T.shape)
    for e in Z_element:
        z += (element_nu[e]
              *f.elemental_mass_fraction(e)
              /gas.atomic_weight(e))

    Z1 = (z-z_o)/(z_f-z_o)

# heat release rate
    Q = f.heat_release_rate

################################################################################
# output

    data = np.column_stack((f.grid,f.T,f.Y.transpose(),
        Z,Z1,Q,alpha,nu))
    data_names = (['grid','T']
            +gas.species_names
            +['Z','Z1','Q','alpha','nu'])

    np.savetxt('{}.dat'.format(case_name),
            data,
            header=('FUEL: {0}\nOXIDIZER: {1}\n'.format(fuel_str,oxy_str)
                +'Zst = {:g}; Z1st = {:g}\n'.format(Zst,Z1st)
                +' '.join(data_names)),
            comments='')

    if np.max(f.T) < np.max((tin_f,tin_o))+100:
        return 1
    else:
        return 0

if __name__ == '__main__':
    counterflow_flame()
