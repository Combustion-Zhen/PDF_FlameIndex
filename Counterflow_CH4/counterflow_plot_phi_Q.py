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

phif = [1.3, 1.7, 2.3, 3.2, 4.8, float('inf')]
phio = [0, 0.05, 0.1, 0.2, 0.3]

ls = ['-','-.','--','-','-.','--']
lw = [2,2,2,1,1,1]

var = 'Q'

a = 200

Zp = 0.06
Zst = 0.0551863
loc_legend = 0.58

dst = 'figs_phi'

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
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.1
margin_right  = 0.1
margin_bottom = 0.8
margin_top    = 0.1
space_width   = 1.3
space_height  = 1.0
ftsize        = 7

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
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
fig,ax = plt.subplots(
        nrow,ncol,sharey=True,
        figsize=cm2inch(plot_width,plot_height))

# get data
folder_params['phif'] = float('inf')
flame_params['phif'] = float('inf')
for i, phi in enumerate(phio):
    folder_params['phio'] = phi
    flame_params['phio'] = phi

    folder = params2name(folder_params)
    flame = params2name(flame_params)

    label = r'$\varphi_l=$'+'{0:g}'.format(phi)

    file_name = '{}/{}.dat'.format(folder,flame)

    if not os.path.exists(file_name):
        continue
    data = np.genfromtxt(file_name,skip_header=3,names=True)
    ax[0].plot(data['Z1'],data[var],label=label,ls=ls[i],lw=lw[i])

folder_params['phio'] = 0
flame_params['phio'] = 0
for i, phi in enumerate(phif):
    folder_params['phif'] = phi
    flame_params['phif'] = phi

    folder = params2name(folder_params)
    flame = params2name(flame_params)

    label = r'$\varphi_r=$'+'{0:g}'.format(phi)

    file_name = '{}/{}.dat'.format(folder,flame)

    if not os.path.exists(file_name):
        continue
    data = np.genfromtxt(file_name,skip_header=3,names=True)
    ax[1].plot(data['Z1'],data[var],label=label,ls=ls[i],lw=lw[i])

ax[0].set_xlim(0.0,0.05)
ax[0].set_xlabel('$Z$')
ax[1].set_xlim(0.05,0.1)
ax[1].set_xlabel('$Z$')

ax[0].set_ylim(0.0,2.3e9)
ax[0].set_ylabel('heat release rate (10$^9$ W/m$^3$)')
#ax[0].set_yticks([0., 0.05, 0.10, 0.15, 0.20, 0.25])

ax[1].tick_params(axis='y',length=0)

ax[0].text(0.045,2e9,'(a)',fontweight='bold')
ax[1].text(0.052,2e9,'(b)',fontweight='bold')

ax[0].text(
        0.002,0.4e9,
        ''.join([r'$\mathrm{CH}_4/\mathrm{Air}$',
                 '\n',
                 '$a\;\:=\;$',
                 '{:g}'.format(a),
                 r'$\;\mathrm{s}^{-1}$',
                 '\n',
                 r'$p\;\;=1\;\mathrm{atm}$',
                 '\n',
                 r'$T_r=300\;\mathrm{K}$',
                 '\n',
                 r'$T_l\,=300\;\mathrm{K}$'
                 ]),
        linespacing=1.5
        )

ax[0].legend(
        handlelength=3,
        handletextpad=0.5,
        frameon=False
        )
ax[1].legend(
        handlelength=3,
        handletextpad=0.5,
        frameon=False
        )

#a_str = r'$a=$'+'{:g}'.format(a)+r'$\;\mathrm{s}^{-1}$'
#axes.text(0.085,cmax*0.92,
#          a_str
#          )
#

fig.subplots_adjust(
    left = margin_left/plot_width,
    bottom = margin_bottom/plot_height,
    right = 1.0-margin_right/plot_width,
    top = 1.0-margin_top/plot_height,
    wspace = space_width/plot_width,
    hspace = space_height/plot_height
    )

fig.savefig('{0}/phi_a{1:g}_{2}.pdf'.format(dst,a,var))
fig.savefig('{0}/phi_a{1:g}_{2}.eps'.format(dst,a,var))

