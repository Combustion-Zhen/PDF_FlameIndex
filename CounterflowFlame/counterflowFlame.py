import cantera as ct
import numpy as np
import sys
import argparse
from filename import params2name

def CounterflowPartiallyPremixedFlame(
        mech='gri30.xml', transport='UnityLewis',
        flag_soret = False, flag_radiation = False,
        fuel_name='CH4', strain_rate=285., width=0.01, p=1.,
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

################################################################################

    p *= ct.one_atm  # pressure

    # Create an object representing the counterflow flame configuration,
    # which consists of a fuel inlet on the left, the flow in the middle,
    # and the oxidizer inlet on the right.
    f = ct.CounterflowDiffusionFlame(gas, width=width)
    f.transport_model = transport
    f.P = p

    if solution is not None:
        f.restore(solution, loglevel=0)

        solution_width = f.grid[-1] - f.grid[0]
        width_factor = width / solution_width

        solution_strain = (f.u[0] - f.u[-1])/solution_width
        strain_factor = strain_rate / solution_strain

        normalized_grid = f.grid / solution_width

        u_factor = strain_factor * width_factor

        # update solution initialization following Fiala & Sattelmayer
        f.flame.grid = normalized_grid * width
        f.set_profile('u', normalized_grid, f.u*u_factor)
        f.set_profile('V', normalized_grid, f.V*strain_factor)
        f.set_profile('lambda', normalized_grid, f.L*np.square(strain_factor))

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

    gas.TPX = tin_f, p, comp_o
    dens_o = gas.density

    gas.TPX = tin_o, p, comp_f
    dens_f = gas.density

    # fuel and oxidizer streams have the same velocity
    u = strain_rate*width/2.

    # get mass flow rate
    mdot_o = u*dens_o
    mdot_f = u*dens_f  # kg/m^2/s

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
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-m', '--mechanism',
        default = 'gri30.xml',
        type = str,
        help = 'reaction mechanism')

    parser.add_argument(
        '-t', '--transport',
        default = 'UnityLewis',
        type = str,
        help = 'transport model')

    parser.add_argument(
        '--soret',
        default = False,
        type = bool,
        help = 'Soret effect')

    parser.add_argument(
        '--radiation',
        default = False,
        type = bool,
        help = 'radiation')

    parser.add_argument(
        '-f', '--fuel',
        default = 'CH4',
        type = str,
        help = 'fuel name')

    parser.add_argument(
        '-a', '--strain',
        default = 100.,
        type = float,
        help = 'mean strain rate (1/s)')

    parser.add_argument(
        '-w', '--width',
        default = 0.01,
        type = float,
        help = 'flame domain (m)')

    parser.add_argument(
        '-p', '--pressure',
        default = 1.,
        type = float,
        help = 'pressure (atm)')

    parser.add_argument(
        '--phif',
        default = float('inf'),
        type = float,
        help = 'equivalence ratio of the rich stream')

    parser.add_argument(
        '--phio',
        default = 0.,
        type = float,
        help = 'equivalence ratio of the lean stream')

    parser.add_argument(
        '--Tf',
        default = 300.,
        type = float,
        help = 'temperature of the rich stream')

    parser.add_argument(
        '--To',
        default = 300.,
        type = float,
        help = 'temperature of the lean stream')

    parser.add_argument(
        '-s', '--solution',
        default = None,
        type = str,
        help = 'restart solution')

    args = parser.parse_args()

    CounterflowPartiallyPremixedFlame(
        mech = args.mechanism,
        transport = args.transport,
        flag_soret = args.soret, 
        flag_radiation = args.radiation,
        fuel_name = args.fuel, 
        strain_rate = args.strain, 
        width = args.width, 
        p = args.pressure,
        phi_f = args.phif, 
        phi_o = args.phio, 
        tin_f = args.Tf, 
        tin_o = args.To, 
        solution = args.solution)
