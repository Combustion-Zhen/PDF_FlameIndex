"""
Zhen Lu 2018/04/23
plot the averaged flame index and mixing rate of PaSR results
"""
import os
import copy
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from counterflow_file import *

models = ['IEM','IEMHYB','EMST','EMSTHYB']
modeln = ['IEM','IEM-FI','EMST','EMST-FI']

mix_res_ratio = [0.02, 0.035, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]

params = {}
params['MIX'] = None
params['tres'] = 1.e-2
params['tmix'] = None
params['eqv'] = 1.0
params['Zfvar'] = 0.1
params['dtmix'] = 0.01
params['phif'] = 4.76

# obtain data
dat_name = 'pasrm.op'

T = np.zeros([len(mix_res_ratio),len(models)])

for i, tmix_ratio in enumerate(mix_res_ratio):
    params['tmix'] = tmix_ratio
    for j, model in enumerate(models):
        params['MIX'] = model

        case = params2name(params)
        file_name = '/'.join([case,dat_name])

        data = np.genfromtxt(file_name,usecols=(-4,))

        T[i,j] = np.mean(data)

# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 6.7
margin_left   = 1.3
margin_right  = 0.2
margin_bottom = 1.0
margin_top    = 0.1
space_width   = 3.5
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
num_rows = 1

colors = ['tab:orange','tab:blue','tab:green','tab:red']

mft = ['o','s']
mfc = ['w',None]

dst = '.'

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.8

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

# plot against tmix
fig, ax = plt.subplots(num_rows,num_cols,sharex=True,
                       figsize=cm2inch(plot_width,plot_height))

for j, model in enumerate(modeln):
    ax.plot(
            mix_res_ratio,T[:,j],
            c=colors[j],ls='',
            marker=mft[j//2],ms=4,mew=0.5,
            label=model)

# axis limits and ticks
ax.set_xscale('log')
ax.set_xticks([2.e-2,1e-1,5e-1])
ax.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

#ax.set_ylim([300, 2100])


# legend
ax.legend(frameon=False)

# labels
ax.set_xlabel(r'$\tau_{\mathrm{mix}}/\tau_{\mathrm{res}}$')
ax.set_ylabel(r'$\langle T \rangle\;(\mathrm{K})$')

# notes
ax.text(
        0.022,1200,
        ''.join([
            r'$\tau_{\mathrm{res}}\,=\,$',
            '{:g}'.format(params['tres']),
            '$\mathrm{s}$',
            '\n',
            r'$\varphi\quad\;\!=\,$',
            '{:g}'.format(params['eqv']),
            '\n',
            r'$\eta_{Z,r}\!\!\:=\,$',
            '{:g}'.format(params['Zfvar'])]))

fig.subplots_adjust(left = margin_left/plot_width,
                    bottom = margin_bottom/plot_height,
                    right = 1.0-margin_right/plot_width,
                    top = 1.0-margin_top/plot_height,
                    wspace = space_width/plot_width,
                    hspace = space_height/plot_height
                    )

plot_params = copy.deepcopy(params)
del plot_params['MIX']
del plot_params['tres']
del plot_params['dtmix']
del plot_params['tmix']
del plot_params['phif']
del plot_params['Zfvar']
plot_name = params2name(plot_params)

fig.savefig('{}/fig_T_{}.pdf'.format(dst,plot_name))

