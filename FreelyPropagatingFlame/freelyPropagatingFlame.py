import cantera as ct
import numpy as np
import argparse
from filename import params2name

def FreelyPropagatingFlame(
        mech = 'gri30.xml', transport = 'UnityLewis',
        fuel_name = 'CH4', p = 1., T = 300., eqv = 1., width = 0.03):

    # supress log output
    loglevel = 0

    # gas object, ideal gas
    gas = ct.Solution(mech)
    if eqv < 0.:
        raise ValueError('Negative equivalence ratio')

    params = {}
    params['F'] = fuel_name
    params['p'] = p
    params['T'] = T
    params['eqv'] = eqv

    case = params2name(params)

    p *= ct.one_atm  # pressure [Pa]

    # construct mixture by volume
    air = {'O2':1.,'N2':3.76}
    fuel_index = gas.species_index(fuel_name)
    stoich_nu = gas.n_atoms(fuel_index,'C')+gas.n_atoms(fuel_index,'H')/4.

    mixture = air
    mixture[fuel_name] = eqv/stoich_nu

    gas.TPX = T, p, mixture

    # flame object
    f = ct.FreeFlame( gas, width = width )

    f.set_initial_guess()

    f.set_refine_criteria(ratio=3, slope=0.06, curve=0.1, prune=0.01)
    f.soret_enabled = False
    f.radiation_enabled = False

    f.transport_model = transport
    try:
        f.solve( loglevel = loglevel )
    except Exception as e:
        print('Error: not converge for case:',e)
        return -1

    # return for unburnt flame
    if np.max(f.T) < T+100:
        return 1

    f.save('{}.xml'.format(case))

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
        '-f', '--fuel',
        default = 'CH4',
        type = str,
        help = 'fuel name')

    parser.add_argument(
        '-p', '--pressure',
        default = 1.,
        type = float,
        help = 'pressure (atm)')

    parser.add_argument(
        '-T', '--temperature',
        default = 300.,
        type = float,
        help = 'temperature of the unburnt stream')

    parser.add_argument(
        '--phi',
        default = 1.,
        type = float,
        help = 'equivalence ratio of the stream')

    parser.add_argument(
        '-w', '--width',
        default = 0.03,
        type = float,
        help = 'flame domain (m)')

    args = parser.parse_args()

    FreelyPropagatingFlame(
        mech = args.mechanism,
        transport = args.transport,
        fuel_name = args.fuel, 
        p = args.pressure,
        T = args.temperature,
        eqv = args.phi, 
        width = args.width)
