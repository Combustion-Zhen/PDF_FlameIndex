"""
Zhen Lu 2017/11/11

plot counterflow profiles colored by CEMA results
"""

import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

#phif   = [1.3, 1.5, 1.7, 2.0, 2.3, 3.2, 4.8, 9.5, float('inf')]
phif   = [1.3, 1.7, 2.0, 2.3, 3.2, 4.8, float('inf')]
#phio = [0, 0.02, 0.05, 0.1, 0.2, 0.3]
phio = [0, 0.05, 0.1, 0.2, 0.3]
strain = [100, 150, 200, 250, 300]

var_names = ['T','C_o','C_4spe','C_2spe','Q']

dst = 'figs_phif_cema'

folder_params = {}
folder_params['phif'] = float('inf')
folder_params['phio'] = 0

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = 100
flame_params['phif'] = float('inf')
flame_params['phio'] = 0
flame_params['tf'] = 300
flame_params['to'] = 300

# plot
# use TEX for interpreter
plt.rc('text',usetex=True)
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 9.0
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

subplot_width = plot_width-margin_left-margin_right
subplot_height = subplot_width * 0.9

plot_height = subplot_height+margin_bottom+margin_top

figs = [None] * len(var_names)
axes = [None] * len(var_names)

for a in strain:
    flame_params['a'] = a

    # generate figure and axes
    for i, var in enumerate(var_names):
        figs[i],axes[i] = plt.subplots(figsize=cm2inch(plot_width,plot_height))

    # get data
    #for phi in phif:
    #    folder_params['phif'] = phi
    #    flame_params['phif'] = phi
    for phi in phio:
        folder_params['phio'] = phi
        flame_params['phio'] = phi

        folder = params2name(folder_params)
        flame = params2name(flame_params)

        label = r'$\varphi_r=$'+'{0:g}'.format(phi)

        file_name = '{}/{}.dat'.format(folder,flame)
        cema_name = '{}/{}.cema'.format(folder,flame)

        if not os.path.exists(file_name):
            continue
        data = np.genfromtxt(file_name,skip_header=3,names=True)

        # scalar dissipation rate
        gradZ = np.gradient(data['Z'],data['grid'])
        chi = 2.*data['nu']/0.8*gradZ*gradZ

        cema = np.genfromtxt(cema_name,usecols=(0,))
        lamb = cema-chi

        cema = np.sign(cema)*np.log10(1+np.absolute(cema))
        lamb = np.sign(lamb)*np.log10(1+np.absolute(lamb))

        for i, var in enumerate(var_names):
            cplt=axes[i].scatter(data['Z1'],data[var],s=4,c=lamb,vmin=-2,vmax=2,
                            marker='.',cmap='jet')

    for i, var in enumerate(var_names):
        #axes[i].set_xlim(0.05,0.15)
        axes[i].set_xlim(0.0,0.058)
        axes[i].set_xlabel('$Z$')
        axes[i].set_ylabel('${}$'.format(var))

        cbar = figs[i].colorbar(cplt)
        
        figs[i].subplots_adjust(
                left = margin_left/plot_width,
                bottom = margin_bottom/plot_height,
                right = 1.0-margin_right/plot_width,
                top = 1.0-margin_top/plot_height,
                wspace = space_width/plot_width,
                hspace = space_height/plot_height
                )

        #figs[i].savefig('{0}/phif_a{1:g}_{2}.pdf'.format(dst,a,var))
        figs[i].savefig('{0}/phio_a{1:g}_{2}.pdf'.format(dst,a,var))
    plt.close('all')
