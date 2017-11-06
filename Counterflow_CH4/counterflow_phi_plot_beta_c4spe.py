"""
Zhen Lu 2017/10/27
plot counterflow flames with different inlet equivalence ratio
only plot for one case
"""

import os
import numpy as np
import glob
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

phif   = [1.3, 1.7, 2.3, 3.2, 4.8]

var = 'C_4spe'
beta = 5

#a = 250
#cmax = 0.27

a = 200
cmax = 0.272

Zp = 0.06
Zst = 0.0551863
loc_legend = 0.58

dst = 'figs_phif'

folder_params = {}
folder_params['phif'] = None
folder_params['phio'] = 0

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = a
flame_params['phif'] = None
flame_params['phio'] = 0
flame_params['tf'] = 300
flame_params['to'] = 300

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 9.0
margin_left   = 1.5
margin_right  = 0.5
margin_bottom = 1.2
margin_top    = 0.1
space_width   = 0.3
space_height  = 1.0
ftsize        = 12

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

subplot_width = plot_width-margin_left-margin_right
subplot_height = subplot_width * 0.9

plot_height = subplot_height+margin_bottom+margin_top

# generate figure and axes
fig,axes = plt.subplots(figsize=cm2inch(plot_width,plot_height))

# beta
axes.plot([0,Zp,2*Zp],[0,Zp*beta,0],
          'k--',linewidth=1)
axes.text(0.015,0.1,
          r'$\beta$',
          fontsize=ftsize-2
          )
axes.text(0.1,0.1,
          r'$-\beta$',
          fontsize=ftsize-2
          )
# Zst
axes.plot([Zst,Zst],[0,Zp*beta],
          'k-.',linewidth=1)
axes.text(Zst-0.01,0.1,
          '$Z_{st}$',
          fontsize=ftsize-2
          )

# get data
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

    axes.plot(data['Z1'],data[var],label=label,linewidth=1)

axes.set_xlim(0.0,0.12)
axes.set_xticks([0.0, 0.03, 0.06, 0.09, 0.12])
axes.set_xlabel('$Z$')
axes.set_ylim(0.0,cmax)
axes.set_yticks([0.0, 0.05, 0.1, 0.15, 0.2, 0.25])
axes.set_ylabel('$c$')

a_str = r'$a=$'+'{:g}'.format(a)+r'$\;\mathrm{s}^{-1}$'
axes.text(0.085,cmax*0.92,
          a_str
          )

axes.legend(fontsize=ftsize-2,
            handlelength=1.2,
            handletextpad=0.3,
            loc=(0,0.59),
            frameon=False
            )

#axes.tick_params(direction='in')

fig.subplots_adjust(
    left = margin_left/plot_width,
    bottom = margin_bottom/plot_height,
    right = 1.0-margin_right/plot_width,
    top = 1.0-margin_top/plot_height,
    wspace = space_width/plot_width,
    hspace = space_height/plot_height
    )

fig.savefig('{0}/phif_a{1:g}_{2}.pdf'.format(dst,a,var))
