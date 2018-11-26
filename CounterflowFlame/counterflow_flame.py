import cantera as ct
import numpy as np
import sys
from filename import params2name

def counterflowPartiallyPremixedFlame(
        mech='gri30.xml', transport='Multi',
        flag_soret = True, flag_radiation = False,
        fuel_name='CH4', strain_rate=100., width=0.01, p=1.,
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
    flame_params['F'] = fuel_name
    flame_params['p'] = p
    flame_params['a'] = strain_rate
    flame_params['phif'] = phi_f
    flame_params['phio'] = phi_o
    flame_params['tf'] = tin_f
    flame_params['to'] = tin_o

    case_name = params2name(flame_params)

    p *= ct.one_atm  # pressure

################################################################################

    oxy = {'O2':1., 'N2':3.76}  # air composition

    fuel_index = gas.species_index(fuel_name)

    stoich_nu = gas.n_atoms(fuel_index,'C')+gas.n_atoms(fuel_index,'H')/4.

    comp_f = {}
    comp_o = {}
    comp_f[fuel_name] = 1
    for k, v in oxy.items():
        comp_o[k] = v
        comp_f[k] = v*stoich_nu/phi_f

    comp_o[fuel_name] = phi_o/stoich_nu

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

    if np.max(f.T) < np.max((tin_f,tin_o))+100:
        return 1
    else:
        return 0

if __name__ == '__main__':
    counterflowPartiallyPremixedFlame()
