"""
Zhen Lu 2017/11/06

plot the FI of constructed subgrid with respect to different sampling
Double columns plot for three mixing models
""" 
import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

def equiv2Z( Phi, Zst ):
    a = Phi*Zst/(1.-Zst)
    Z = a/(1.+a)
    return Z

var = 0.05
#a = 100
#a = 150
#loc_legend = (0., 0.51)

a = 200
loc_legend = (0., 0.51)

Zst = 0.0551863

variance = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
eqv_ratio = [0.8,0.9,1.0,1.1,1.2,1.3,1.4]

phif   = [1.3, 1.7, 2.3, 3.2, 4.8]
strain = [100, 150, 200, 250]

dst = 'figs_sample_line'

models = ['IEM','MC','EMST']

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
flame_params['eqv'] = None
flame_params['var'] = var

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 19.0
margin_left   = 1.5
margin_right  = 0.1
margin_bottom = 1.2
margin_top    = 0.1
space_width   = 0.
space_height  = 1.0
ftsize        = 12

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = len(models)
num_rows = 1

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.9

plot_height = (subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

# generate figure and axes
fig, ax = plt.subplots(num_rows,num_cols,sharex=True,sharey=True,
                       figsize=cm2inch(plot_width,plot_height))

for axes in ax:
    axes.plot([0,1],[0.5,0.5],'k--',linewidth=1)

# get data
for phi in phif:
    folder_params['phif'] = phi
    flame_params['phif'] = phi

    folder = params2name(folder_params)

    label = r'$\varphi_r=$'+'{0:g}'.format(phi)

    for j, model in enumerate(models):
        data = np.zeros((len(eqv_ratio),2))
        for k, eqv in enumerate(eqv_ratio):
            flame_params['eqv'] = eqv

            flame = params2name(flame_params)
            file_name = '{}/{}.{}'.format(folder,flame,model)

            if not os.path.exists(file_name):
                continue
            flame_index = np.genfromtxt(file_name,usecols=(2,))

            data[k,0] = equiv2Z(eqv,Zst)
            data[k,1] = np.mean(flame_index)

            flag = data[:,0] > 0

        ax[j].plot(data[flag,0],data[flag,1],label=label,linewidth=1)
    
ax[0].set_ylabel(r'$\tilde{\mathrm{FI}}$')

ax[1].text(0.045,0.52,r'$\tilde{\mathrm{FI}}=0.5$')

for j, axes in enumerate(ax):
    axes.set_xlim(0.042,0.078)
    axes.set_xlabel('$Z$')
    axes.text(0.045,0.2,
            ''.join(['{}\n'.format(models[j]),
                     r'$a\;\;=$',
                     '{:g}'.format(a),
                     r'$\;\mathrm{s}^{-1}$',
                     '\n',
                     r'$\eta_Z=$',
                     '{:g}'.format(var)]))

ax[0].legend(fontsize=ftsize-2,
             loc=loc_legend,
             handlelength=1.2,
             handletextpad=0.3,
             frameon=False
             )

fig.subplots_adjust(
    left = margin_left/plot_width,
    bottom = margin_bottom/plot_height,
    right = 1.0-margin_right/plot_width,
    top = 1.0-margin_top/plot_height,
    wspace = space_width/plot_width,
    hspace = space_height/plot_height
    )

fig.savefig('{0}/FI_a{1:g}_var{2:g}.pdf'.format(dst,a,var))
fig.savefig('{0}/FI_a{1:g}_var{2:g}.eps'.format(dst,a,var))
# close figures to avoid warnings
plt.close('all')
