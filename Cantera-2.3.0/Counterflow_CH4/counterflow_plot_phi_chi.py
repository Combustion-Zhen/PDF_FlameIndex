"""
Zhen Lu 2017/11/29

plot SDR in counterflow flames with different extent of premixing
"""

import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

phif = [1.3, 1.7, 2.3, 3.2, 4.8, float('inf')]

var_names = ['Z1','C_4spe']

a = 200

dst = 'figs_chi'

folder_params = {}
folder_params['phif'] = float('inf')
folder_params['phio'] = 0

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = a
flame_params['phif'] = float('inf')
flame_params['phio'] = 0
flame_params['tf'] = 300
flame_params['to'] = 300

# plot
# use TEX for interpreter
plt.rc('text',usetex=True)
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.8
margin_right  = 0.5
margin_bottom = 1.2
margin_top    = 1.0
space_width   = 0.3
space_height  = 1.0
ftsize        = 10

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

plt.rc('font',**font)

nrow = 1
ncol = 2

subplot_width = (plot_width-margin_left-margin_right-(ncol-1)*space_width)/2
subplot_height = subplot_width * 0.7

plot_height = (nrow*subplot_height
              +margin_bottom
              +margin_top
              +(nrow-1)*space_height)

# generate figure and axes
fig, ax = plt.subplots(nrow,ncol,sharey=True,
                       figsize=cm2inch(plot_width,plot_height))

for phi in phif:
    folder_params['phif'] = phi
    flame_params['phif'] = phi

    folder = params2name(folder_params)
    flame = params2name(flame_params)

    label = r'$\varphi_r=$'+'{0:g}'.format(phi)

    file_name = '{}/{}.dat'.format(folder,flame)

    if not os.path.exists(file_name):
        continue
    data = np.genfromtxt(file_name,skip_header=3,names=True)

    # scalar dissipation rate
    gradZ = np.gradient(data['Z'],data['grid'])
    chi = 2.*data['nu']/0.8*gradZ*gradZ

    ax[0].plot(data['Z'],chi,label=label)
    ax[0].set_xlim(0,0.2)
    ax[0].legend(
            frameon=False
            )

    gradC = np.gradient(data['C_4spe'],data['grid'])
    chi = 2.*data['nu']/0.8*gradC*gradC

    ax[1].plot(data['Z1'],chi,label=label)
    ax[1].set_xlim(0,0.2)
    ax[1].legend(
            frameon=False
            )

fig.savefig('{0}/phi_a{1:g}.pdf'.format(dst,a))
fig.savefig('{0}/phi_a{1:g}.eps'.format(dst,a))
plt.close('all')

