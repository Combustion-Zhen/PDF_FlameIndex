
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from counterflow_file import *

Z_st = 0.055

models = ['IEM','IEMHYB','EMST','EMSTHYB']
modeln = ['IEM','IEM-FI','EMST','EMST-FI']

params = {}
params['MIX'] = None
params['tres'] = 1.e-2
params['tmix'] = 0.2
params['eqv'] = 1.0
params['Zfvar'] = 0.1
params['dtmix'] = 0.01
params['phif'] = 4.76

data_params = {}
data_params['MIX'] = params['MIX']
data_params['tmix'] = params['tmix']
data_params['var'] = 'F'
data_params['statics'] = 'avg'

# obtain data
file_name = 'cond-FC_eqv-{:g}.csv'.format(params['eqv'])
data = pd.read_csv(file_name)

Z_f = np.genfromtxt('template/flame_Z.dat',skip_header=1,usecols=(0,))
Z_mid = (Z_f[1:]+Z_f[:-1])/2

# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.3
margin_right  = 0.2
margin_bottom = 0.8
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

num_cols = 2
num_rows = 1

colors = ['tab:orange','tab:blue','tab:green','tab:red']
lines = [':','-','-.','--']

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
fig, ax = plt.subplots(num_rows,num_cols,
                       figsize=cm2inch(plot_width,plot_height))

for i, model in enumerate(models):
    params['MIX'] = model
    data_params['MIX'] = model
    
    ax[0].plot(
        data['Z'], 2*data[params2name(data_params)].values-1,
        c = colors[i], ls = lines[i], lw = 1.,
        label=modeln[i])

    if i%2 == 1:
        case_name = params2name(params)
        file_name = '/'.join([case_name,'mixrate.op'])

        omega = np.genfromtxt(file_name)
        omega_avg = np.average(omega[:,1:-1], axis = 0)

        ax[1].plot(
                Z_mid,omega_avg*params['tres']*params['tmix'],
                c = colors[i], ls = lines[i], lw = 1.,
                label=modeln[i])

# legend
ax[0].legend(frameon=False)

# limits
ax[0].set_xlim([0, 0.5])
ax[0].set_ylim([-1, 1])
ax[0].set_yticks([-1, -0.5, 0, 0.5, 1])
ax[1].set_xlim([0.03, 0.121])

# notes
ax[1].text(
        0.035,4.5,
        ''.join([
            r'$\tau_{\mathrm{res}}\,=\,$',
            '{:g}'.format(params['tres']),
            '$\;\mathrm{s}$',
            '\n',
            r'$\tau_{\mathrm{mix}}\!=\,$',
            '{:g}'.format(params['tres']*params['tmix']*1000),
            '$\;\mathrm{ms}$',
            '\n',
            r'$\varphi\quad\;\!=\,$',
            '{:g}'.format(params['eqv']),
            '\n',
            r'$\eta_{Z,r}\!\!\:=\,$',
            '{:g}'.format(params['Zfvar'])]))

# labels
ax[0].set_xlabel(r'$Z$')
ax[1].set_xlabel(r'$Z$')
ax[0].set_ylabel(r'$\langle\mathrm{FI}\vert Z\rangle$')
ax[1].set_ylabel(r'$\langle\widetilde{\omega_{\phi}\vert Z}\rangle\cdot\tau_{\mathrm{mix}}$')

# figure layout
fig.subplots_adjust(left = margin_left/plot_width,
                    bottom = margin_bottom/plot_height,
                    right = 1.0-margin_right/plot_width,
                    top = 1.0-margin_top/plot_height,
                    wspace = space_width/plot_width,
                    hspace = space_height/plot_height
                    )

fig.savefig('{0}/fig_condFIOMEGA_tmix-{1:g}_eqv-{2:g}.pdf'.format(dst,params['tmix'],params['eqv']))

