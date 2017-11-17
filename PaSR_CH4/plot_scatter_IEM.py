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
from counterflow_file import *

models = np.array(['IEM','IEMHYB'])

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
dat_name = 'particle_fi.dat'
full_name = 'fifull.op'

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 6.7
margin_left   = 1.0
margin_right  = 0.1
margin_bottom = 0.8
margin_top    = 0.5
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
    file_name = '/'.join([model,case,dat_name])
    if os.path.exists(file_name):
        FI = np.genfromtxt(file_name)
    else:
        print(file_name)
        FI = np.zeros((1000,3))

    cplt = ax[i].scatter(
            FI[:,1],FI[:,2],c=FI[:,0],
            s=3,
            vmin=0,vmax=1,
            marker='.',
            cmap='coolwarm')

    ax[i].set_ylim(0,0.31)
    ax[i].set_ylabel('$c$')

ax[0].text(0.12,0.27,'(a) IEM')
ax[1].text(0.12,0.27,'(b) IEMHYB')
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

cax = fig.add_axes([3/plot_width,
                    (plot_height-0.4)/plot_height,
                    3/plot_width,
                    0.12/plot_height])
clb = fig.colorbar(cplt,cax=cax,orientation='horizontal')
cax.tick_params(axis='x',pad=0.1,length=2,labelsize='small')
cax.xaxis.set_ticks_position('top')

fig.text(2.3/plot_width,(plot_height-0.3)/plot_height,'FI')

#cax = fig.add_axes(
#        [(plot_width-margin_right+0.2)/plot_width,
#          margin_bottom/plot_height,
#          0.2/plot_width,
#          (2*subplot_height+space_height)/plot_height])
#clb = fig.colorbar(cplt,cax=cax)
#cax.set_ylabel('$\mathrm{FI}$')

fig.savefig('{}/PaSR_FI_scatter_IEM.eps'.format(dst))
plt.close('all')
