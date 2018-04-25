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

models = np.array(['IEM','EMST','IEMHYB','EMSTHYB'])
modeln = np.array(['IEM','EMST','IEM-FI','EMST-FI'])

time_res = [1.e-2,]
mix_res_ratio = [0.02, 0.035, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
equiv_ratio_f = [4.76,]
equiv_ratio = [1.2,]
Zf_variance = [0.1,]
dtmix = [0.01,]

params = {}
params['MIX'] = None
params['tres'] = 1.e-2
params['tmix'] = None
params['eqv'] = 1.2
params['Zfvar'] = 0.1
params['dtmix'] = 0.01
params['phif'] = 4.76

# obtain data
dat_name = 'pasrm.op'

fi = np.zeros([len(mix_res_ratio),models.size])
omega = np.zeros([len(mix_res_ratio),models.size])

for i, tmix_ratio in enumerate(mix_res_ratio):
    params['tmix'] = tmix_ratio
    for j, model in enumerate(models):
        params['MIX'] = model

        case = params2name(params)
        file_name = '/'.join([case,dat_name])

        data = np.genfromtxt(file_name,usecols=(3,4))

        fi[i,j] = np.mean(data[:,0])
        omega[i,j] = np.mean(data[:,1])

# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.5
margin_right  = 0.22
margin_bottom = 0.85
margin_top    = 0.1
space_width   = 2.5
space_height  = 0.5
ftsize        = 7

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = 2
num_rows = 1

colors = np.array(['tab:orange','tab:green','tab:blue','tab:red'])

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
    ax[0].plot(
            mix_res_ratio,2*fi[:,j]-1,
            c=colors[j],ls='',
            marker=mft[j%2],ms=4,mew=0.5,
            label=model)
    if j > 1:
        ax[1].plot(mix_res_ratio,omega[:,j]*np.array(mix_res_ratio)/100.,
                c=colors[j],ls='',
                marker=mft[j%2],ms=4,mew=0.5,
                label=model)

ax[0].set_xscale('log')
ax[0].set_xlim([0.015,0.6])
ax[0].set_xticks([2e-2,1e-1,5e-1])
ax[0].get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())

ax[0].set_ylim([-1,1])
ax[0].set_yticks([-1,-0.5,0,0.5,1])
ax[1].set_ylim([1,1.15])
ax[1].set_yticks(np.arange(1,1.15,0.02))

ax[0].legend(ncol=2,frameon=False)

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
del plot_params['phif']
del plot_params['Zfvar']
plot_name = params2name(plot_params)

fig.savefig('{}/fig_FIOMEGA_{}.pdf'.format(dst,plot_name))

