"""
Zhen Lu 2017/11/13

plot conditional omega
"""
import os
import copy
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

model = 'IEMHYB'

tres = 0.01
#mix_res_ratio = [0.02, 0.05, 0.1, 0.2, 0.5]
tmixr = 0.2
phif = 4.76
#phi = [1.0, 1.2, 1.4]
eqv = 1.2
#Zf_variance = [0.01, 0.02, 0.05, 0.1, 0.15]
Zf_variance = [0.05, 0.1, 0.15]
line_style = ['-.','-','--']
dtmix = 0.01

params = {}
params['MIX'] = model
params['tres'] = tres
params['tmix'] = tmixr
params['eqv'] = eqv
params['Zfvar'] = None
params['dtmix'] = dtmix
params['phif'] = phif

dst = 'figs_omega'
dat_name = 'mixrate.op'
ave_name = 'pasrm.op'

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 6.7
margin_left   = 1.2
margin_right  = 0.1
margin_bottom = 0.8
margin_top    = 0.1
space_width   = 0.
space_height  = 0.
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

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.8

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

Zall = np.genfromtxt('flame_Z.dat',skip_header=1,usecols=(0,))
Z = (Zall[1:]+Zall[:-1])/2

fig, ax = plt.subplots(
        figsize = cm2inch(plot_width,plot_height))

omtau = 1/(tres*tmixr)
ax.plot([0,0.2],[omtau,omtau],'k:',linewidth=1)

for i, var in enumerate(Zf_variance):
    params['Zfvar'] = var

    case = params2name(params)
    file_name = '/'.join([model,case,dat_name])

    rate = np.genfromtxt(file_name)

    file_name = '/'.join([model,case,ave_name])
    omt = np.genfromtxt(file_name,usecols=(4,))

    if len(rate.shape) == 1:
        continue

    # calculate the ensemble averate
    omega = np.mean(rate[-50:,1:-1],axis=0)
    omstd = np.std(rate[-50:,1:-1],axis=0)
    omave = np.mean(omt[-50:])

    label = ''.join(
            [r'$\eta_{Z,r}=$',
             '{:g}'.format(var),
             '\n',
             r'$\langle\omega\rangle\;\,=$',
             '{:.4g}'.format(omave),
             r'$\;\mathrm{s}^{-1}$'
             ])

    ax.plot(Z,omega,line_style[i],linewidth=1,label=label)
    #ax.fill_between(Z,omega+omstd,omega-omstd,alpha=0.1)

ax.text(
        0.09,1150,
        ''.join([
            r'$\tau_{\mathrm{res}}\,=0.01\;\mathrm{s}$',
            '\n',
            r'$\tau_{\mathrm{mix}}\!=2\;\mathrm{ms}$',
            '\n',
            r'$\varphi\quad\;\!=1.2$'
            ]))

ax.legend(
        frameon=False,
        labelspacing=1
        )
ax.set_xlim(0.02,0.13)
ax.set_xlabel(r'$Z$')
ax.set_ylabel(r'$\langle\widetilde{\omega\vert Z}\rangle$')
ax.set_yscale('log')

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/plot_width,
        hspace = space_height/plot_height
        )

fig.savefig('{}/omega_IEM.eps'.format(dst))
