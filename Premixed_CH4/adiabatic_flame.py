"""
A freely-propagating, premixed hydrogen flat flame with multicomponent
transport properties.
"""

import cantera as ct
import numpy as np
from flame_file import params2name

def adiabatic_flame(mech = 'gri30.xml', transport = 'Multi',
        fuel_name = 'CH4', p = 1., T = 300., eqv = 1.,
        width = 0.03, solution=None):

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

    if solution is not None:
        try:
            f.restore( solution, loglevel = loglevel )
        except Exception as e:
            print( e, 'Start to solve from initialization' )
            f.set_initial_guess()

    f.set_refine_criteria(ratio=3, slope=0.06, curve=0.1, prune=0.01)
    #f.soret_enabled = False
    #f.radiation_enabled = False

    # Solve with mixture-averaged transport model
    f.transport_model = 'Mix'
    try:
        f.solve( loglevel = loglevel, auto = True )
    except Exception as e:
        print('Error: not converge for case:',e)
        return -1

    f.transport_model = transport
    try:
        f.solve( loglevel = loglevel)
    except Exception as e:
        print('Error: not converge for case:',e)
        return -1

    # return for unburnt flame
    if np.max(f.T) < T+100:
        return 1

    f.save('{}.xml'.format(case))

    # write the velocity, temperature, density, and mole fractions to a CSV file
    f.write_csv('{}.csv'.format(case), species='Y', quiet=False)

    np.savetxt('{}_diff.dat'.format(case),f.mix_diff_coeffs_mass)

if __name__ == '__main__':
    adiabatic_flame()
