import numpy as np
import argparse
from filename import params2name
import sys
sys.path.append('/home/luz0a/Documents/PDF_FlameIndex/FreelyPropagatingFlame')
from freelyPropagatingFlame import FreelyPropagatingFlame

def FreeFlameEquivalenceDriver(
        mech = 'gri30.xml', transport = 'UnityLewis',
        fuel_name = 'CH4', p = 1., T = 300.):

    eqvList = [0.4, 0.6, 0.8, 1.0, 1.2, 1.8, 2.4]

    for eqv in eqvList:
        FreelyPropagatingFlame(mech = mech,
                             transport = transport,
                             fuel_name = fuel_name,
                             p = p,
                             T = T,
                             eqv = eqv)

if __name__ == '__main__':
    FreeFlameEquivalenceDriver()
