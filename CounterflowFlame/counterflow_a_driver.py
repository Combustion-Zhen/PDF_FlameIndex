import numpy as np
import os
import argparse
import sys
sys.path.append('/home/luz0a/Documents/PDF_FlameIndex/CounterflowFlame')
from filename import params2name
from counterflow_flame import counterflowPartiallyPremixedFlame

def counterflowFlameStrainDriver(
        mech='gri30.xml', transport='UnityLewis',
        flag_soret = False, flag_radiation = False,
        fuel_name='CH4', width=0.01, p=1.,
        phi_f='inf', phi_o=0., tin_f=300., tin_o=300.):

    strain_list = np.array([50, 100, 200, 400])

    folder_params = {}
    folder_params['phif'] = phi_f
    folder_params['phio'] = phi_o

    folder_name = params2name(folder_params)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    os.chdir(folder_name)

    # parameters
    flame_params = {}
    flame_params['F'] = fuel_name
    flame_params['p'] = p
    flame_params['a'] = None
    flame_params['phif'] = phi_f
    flame_params['phio'] = phi_o
    flame_params['tf'] = tin_f
    flame_params['to'] = tin_o

    solution = None

    for a in strain_list:

        flame_params['a'] = a
        case_name = params2name(flame_params)
        file_name = '{}.xml'.format(case_name)

        info = counterflowPartiallyPremixedFlame(
                mech = mech,
                transport = transport,
                flag_soret = flag_soret,
                flag_radiation = flag_radiation,
                fuel_name = flame_params['F'],
                strain_rate = flame_params['a'],
                width = width,
                p = flame_params['p'],
                phi_f = flame_params['phif'],
                phi_o = flame_params['phio'],
                tin_f = flame_params['tf'],
                tin_o = flame_params['to'],
                solution = solution )

        if info == 0 :
            print('strain rate = {:g} success'.format(flame_params['a']))
            solution = file_name
        elif info == -1 :
            print('strain rate = {:g} fail'.format(flame_params['a']))
            break
        elif info == 1 :
            print('strain rate = {:g} extinct'.format(flame_params['a']))
            os.remove(file_name)
            break

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

    args = parser.parse_args()

    counterflowFlameStrainDriver(
        mech = args.mechanism,
        transport = args.transport,
        flag_soret = args.soret, 
        flag_radiation = args.radiation,
        fuel_name = args.fuel, 
        width = args.width, 
        p = args.pressure,
        phi_f = args.phif, 
        phi_o = args.phio, 
        tin_f = args.Tf, 
        tin_o = args.To)
