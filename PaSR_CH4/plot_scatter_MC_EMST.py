"""
Zhen Lu 2017/11/13

scatter plot of a certain case
"""

import os
import copy
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from subprocess import run
from counterflow_file import *

models = np.array(['MC','EMST'])

time_res = [1.e-2,]
#mix_res_ratio = [0.02, 0.05, 0.1, 0.2, 0.5]
mix_res_ratio = [0.1,]
equiv_ratio_f = [4.76,]
#equiv_ratio = [1.0, 1.2, 1.4]
equiv_ratio = [1.2,]
#Zf_variance = [0.01, 0.02, 0.05, 0.1, 0.15]
Zf_variance = [0.1,]
dtmix = [0.01,]

params = {}
params['MIX'] = None
params['tres'] = 1.e-2
params['tmix'] = 0.2
params['eqv'] = 1.2
params['Zfvar'] = 0.1
params['dtmix'] = 0.01
params['phif'] = 4.76

dst = 'figs_scatter'
dat_name = 'particle_info.op'

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 6.7
margin_left   = 1.0
margin_right  = 0.1
margin_bottom = 0.8
margin_top    = 0.1
space_width   = 0.5
space_height  = 0.5
ftsize        = 7

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = 1
num_rows = 2

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.4

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

# loop over all parameters
fig, ax = plt.subplots(
        num_rows,num_cols,
        sharex=True,sharey=True,
        figsize=cm2inch(plot_width,plot_height))

for i in range(2):
    model = models[i]
    params['MIX'] = model
    case = params2name(params)
    folder_name = '/'.join([model,case])
    file_name = '/'.join([model,case,dat_name])

    os.chdir(folder_name)
    run(['particles_post'])
    os.chdir('../..')
    p = np.genfromtxt(file_name)

    cplt = ax[i].scatter(
            p[:,0],p[:,1],
            marker='.',
            s=2
            )

    ax[i].set_ylim(0,0.31)
    ax[i].set_ylabel('$c$')

ax[0].text(0.12,0.27,'(a) MC')
ax[1].text(0.12,0.27,'(b) EMST')
ax[0].set_xlim(0,0.37)
ax[0].set_ylim(0,0.32)
ax[0].set_xticks([0,0.1,0.2,0.3])
ax[0].set_yticks([0,0.1,0.2,0.3])

ax[-1].set_xlabel('$Z$')
ax[0].tick_params(axis='x',length=0)

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/plot_width,
        hspace = space_height/plot_height
        )

ax[0].text(
        0.25,0.14,
        ''.join([
            r'$\tau_{\mathrm{res}}\,=0.01\;\mathrm{s}$',
            '\n',
            r'$\tau_{\mathrm{mix}}\!=2\;\mathrm{ms}$',
            '\n',
            r'$\varphi\quad\;\!=1.2$',
            '\n',
            r'$\langle\varphi_r\rangle\!=4.76$',
            '\n',
            r'$\eta_{Z,r}\!\!\:=0.1$'
            ]))

fig.savefig('{}/PaSR_cZ_scatter.eps'.format(dst))
plt.close('all')
