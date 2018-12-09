"""
Zhen Lu 2017/11/04

A driver to loop over adiabatic flame results,
calculating the scalar dissipation rate

function flame_chi requires numpy 1.13, conflict with cantera
"""

import numpy as np
from flame_file import *
from flame_chi import *
import matplotlib.pyplot as plt

def equiv2Z( phi, Zst ):
    a = phi*Zst/(1.-Zst)
    Z = a/(1.+a)
    return Z

# get flame parameters
param_list = paramlist('.xml')

F = 'CH4'
p = 1
T = 300
Zst = 0.05518

params = {}
params['F'] = F
params['p'] = p
params['T'] = T

eqvn = np.array(param_list['eqv'])
eqvl = eqvn[eqvn <= 1.]
eqvr = eqvn[eqvn >= 1.]

# plot
# use TeX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
plot_width    = 9.0
plot_height   = 9.0
margin_left   = 1.8
margin_right  = 0.3
margin_bottom = 1.2
margin_top    = 1.0
space_width   = 2.4
space_height  = 1.5
ftsize        = 12

fig, ax = plt.subplots(1,2,sharex=True,sharey=True)

flame_raw = {}

npts = 1

for eqv in eqvn:

    params['eqv'] = eqv
    label = r'$\Phi = $'+'{:g}'.format(eqv)
    case = params2name(params)

    C = flame_chi_n(case)

    if C.shape[0] > npts :
        npts = C.shape[0]
        grid = C[:,1]

    # store data
    flame_raw[eqv] = C

    if eqv <= 1.:
        ax[0].plot(C[:,1],C[:,2],label=label)
    else:
        ax[1].plot(C[:,1],C[:,2],label=label)

ax[0].set_xlim(0.,1)
ax[0].set_xlabel('$c$',fontsize=ftsize)
ax[1].set_xlabel('$c$',fontsize=ftsize)
ax[0].set_ylabel('$\chi_{c}$',fontsize=ftsize)

ax[0].legend(fontsize=ftsize, frameon=False)
ax[1].legend(fontsize=ftsize, frameon=False)

fig.savefig('normalized_chi.pdf')

if grid[0] > 0. :
    npts += 1
    grid = np.insert(grid,0,0)

flag = grid[1:] == grid[:-1]
flag = np.insert(flag,0,False)
npts -= np.sum(flag)

for i, v in reversed(list(enumerate(flag))):
    if v:
        grid = np.delete(grid,i)

flame_chi = np.zeros((npts,len(eqvn)))

with open('flame_C.dat','w') as f:
    f.write('{:d}\n'.format(npts))
    for x in grid:
        f.write('{:17.8e}\n'.format(x))

with open('flame_Z.dat','w') as f:
    f.write('{:d}\n'.format(len(eqvn)))
    for i, eqv in enumerate(eqvn):
        Z = equiv2Z( eqv, Zst )
        C = flame_raw[eqv]
        f.write('{:17.8e}{:17.8e}{:17.8e}\n'.format(Z,C[0,0],C[-1,0]))

        flame_chi[:,i] = np.interp( grid, C[:,1], C[:,2] )

np.savetxt('flame_chi.dat',flame_chi)
