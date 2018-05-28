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

tau_log = np.linspace(-4,-2,21)
tau_log = np.insert( tau_log, 4, -3.65)

params = {}
params['MIX'] = None
params['tres'] = None
params['tmix'] = 0.2
params['eqv'] = 1.0

# obtain data
dat_name = 'pasrm.op'

fi = np.zeros([len(tau_log),len(models)])
omega = np.zeros([len(tau_log),len(models)])

for i, t in enumerate(tau_log):
    params['tres'] = t
    for j, model in enumerate(models):
        params['MIX'] = model

        case = params2name(params)
        file_name = '/'.join([case,dat_name])

        data = np.genfromtxt(file_name,usecols=(3,4))

        fi[i,j] = np.mean(data[:,0])
        omega[i,j] = np.mean(data[:-1750,1])

# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.4
margin_right  = 0.1
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
plt.rc('text.latex', preamble=[r'\usepackage{amsmath}',r'\usepackage{bm}'])
# use serif font
plt.rc('font',**font)

num_cols = 2
num_rows = 1

colors = ['tab:orange','tab:blue','tab:green','tab:red']

mft = ['o','s']
mfc = ['w',None]

dst = '.'

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.9

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

# plot against tmix
fig, ax = plt.subplots(num_rows,num_cols,sharex=True,
                       figsize=cm2inch(plot_width,plot_height))

ax[0].plot(
        [0.00001, 0.1],[0, 0],
        'k--',lw=1.0)

ax[1].plot(
        [0.00001, 0.1],[1, 1],
        'k--',lw=1.0)

tres = np.power(10, tau_log)
for j, model in enumerate(modeln):
    ax[0].plot(
            tres,2*fi[:,j]-1,
            c=colors[j],ls='',
            marker=mft[j//2],ms=4,mew=0.5,
            label=model)
    print(model)
    print(2*fi[:,j]-1)
    if j%2 == 1:
        ax[1].plot(tres,omega[:,j]*tres*params['tmix'],
                c=colors[j],ls='',
                marker=mft[j//2],ms=4,mew=0.5,
                label=model)

# axis limits and ticks
ax[0].set_xscale('log')
ax[0].set_xlim([0.00008,0.0125])
#ax[0].set_xticks([2e-2,1e-1,5e-1])
#ax[0].get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

ax[0].set_ylim([-0.7,0.7])
ax[1].set_ylim([0.95,1.75])
#ax[0].set_yticks([-1,-0.5,0,0.5,1])

# legend
ax[0].legend(frameon=False,
             loc=4
            )
ax[1].legend(frameon=False,
             loc=6,
            )

# labels
ax[0].set_xlabel(r'$\tau_{\mathrm{res}}\;(\mathrm{s})$')
ax[1].set_xlabel(r'$\tau_{\mathrm{res}}\;(\mathrm{s})$')
ax[0].set_ylabel(r'$\langle\tilde{\mathrm{FI}}\rangle$')
ax[1].set_ylabel(r'$\langle\tilde{\omega}_{\bm\phi}\rangle/\tilde{\omega}_{\bm\phi}^\mathrm{N}$')

# notes
ax[0].text(0.0001,0.55,'(a)')
ax[1].text(0.0001,1.25/1.4*0.8+0.95,'(b)')

ax[0].text(0.0006,(1.6-0.95)/0.8*1.4-0.7,
           r'$\dfrac{\tau_{\mathrm{mix}}}{\tau_{\mathrm{res}}} = 0.2$',
          )
ax[1].text(0.0006,1.6,
           r'$\dfrac{\tau_{\mathrm{mix}}}{\tau_{\mathrm{res}}} = 0.2$',
          )

fig.subplots_adjust(left = margin_left/plot_width,
                    bottom = margin_bottom/plot_height,
                    right = 1.0-margin_right/plot_width,
                    top = 1.0-margin_top/plot_height,
                    wspace = space_width/plot_width,
                    hspace = space_height/plot_height
                    )

fig.savefig('{}/fig_FIOMEGA.pdf'.format(dst))
fig.savefig('{}/fig_FIOMEGA.eps'.format(dst))

