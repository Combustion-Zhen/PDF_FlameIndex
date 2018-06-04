"""
Zhen Lu 2018/04/23
plot the averaged flame index and mixing rate of PaSR results
"""
import os
import copy
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

models = ['IEM','IEMHYB','EMST','EMSTHYB']
modeln = ['IEM','IEM-FI','EMST','EMST-FI']

tau_log = np.linspace(-4,-2,21)
tau_log = np.insert( tau_log, 4, -3.65)

params = {}
params['MIX'] = None
params['tres'] = None
params['tmix'] = 0.2
params['eqv'] = 1.0

# obtain data
dat_name = 'pasrm.op'

T = np.zeros([len(tau_log),len(models)])

for i, t in enumerate(tau_log):
    params['tres'] = t
    for j, model in enumerate(models):
        params['MIX'] = model

        case = params2name(params)
        file_name = '/'.join([case,dat_name])

        data = np.genfromtxt(file_name,usecols=(-4,))

        T[i,j] = np.mean(data)

# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 6.7
margin_left   = 1.4
margin_right  = 0.1
margin_bottom = 1.0
margin_top    = 0.1
space_width   = 3.5
space_height  = 0.5
ftsize        = 9

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
plt.rc('text.latex',preamble=[r'\usepackage{amsmath}'])
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
fig, ax = plt.subplots(num_rows,num_cols,
                       figsize=cm2inch(plot_width,plot_height))

for j, model in enumerate(modeln):
    ax.plot(
            np.power(10,tau_log),T[:,j],
            c=colors[j],ls='',
            marker=mft[j//2],ms=4,mew=0.5,
            label=model)

# axis limits and ticks
ax.set_xscale('log')

ax.set_xlim([0.00008, 0.0125])
ax.set_ylim([300, 2100])

# legend
ax.legend(frameon=False)

# labels
ax.set_xlabel(r'$\tau_{\mathrm{res}}\;(\mathrm{s})$')
ax.set_ylabel(r'$\langle\tilde{T}\rangle\;(\mathrm{K})$')

# notes
ax.text(
        0.0001,1750,
        r'$\dfrac{\tau_{\mathrm{mix}}}{\tau_{\mathrm{res}}} = 0.2$',
       )

fig.subplots_adjust(left = margin_left/plot_width,
                    bottom = margin_bottom/plot_height,
                    right = 1.0-margin_right/plot_width,
                    top = 1.0-margin_top/plot_height,
                    wspace = space_width/plot_width,
                    hspace = space_height/plot_height
                    )

fig.savefig('{}/fig_T.pdf'.format(dst))
fig.savefig('{}/fig_T.eps'.format(dst))

