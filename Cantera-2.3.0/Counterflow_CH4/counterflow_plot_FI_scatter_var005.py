"""
Zhen Lu 2017/11/08

scatter plot of constructed subgrid

select a set of cases
"""
import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

models = ['IEM','MC','EMST']

strain = [100, 200, 300]
#variance = [0.05, 0.05, 0.05]
variance = 0.05
phif = [1.3, 2.3, 4.8]

Zst = 0.0551863

xlim0 = 0.046
xlim1 = 0.072
xfac = 0.02

dst = 'figs_sample_scatter'

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = None
flame_params['phif'] = None
flame_params['phio'] = 0
flame_params['tf'] = 300
flame_params['to'] = 300
flame_params['eqv'] = 1.2
flame_params['var'] = None

folder_params= {}
folder_params['phif'] = None
folder_params['phio'] = 0

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.0
margin_right  = 0.1
margin_bottom = 0.8
margin_top    = 0.6
space_width   = 0.
space_height  = 2.
ftsize        = 7

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = len(models)
num_rows = len(strain)

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.15

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

fig, ax = plt.subplots(num_rows,num_cols,
                       sharex='row',sharey=True,
                       figsize=cm2inch(plot_width,plot_height))

axsb = [0.832, 0.54, 0.248]

for i in range(num_rows):

    flame_params['a'] = strain[i]
    flame_params['phif'] = phif[i]
    flame_params['var'] = variance

    folder_params['phif'] = phif[i]

    folder = params2name(folder_params)
    flame = params2name(flame_params)

    for j in range(num_cols):

        ax[i,j].plot([0, 1],[0.5, 0.5],'k--',linewidth=1)
        ax[i,j].plot([Zst, Zst],[0, 1],'k-.',linewidth=1)

        file_name = '{}/{}.{}'.format(folder,flame,models[j])

        FI = np.genfromtxt(file_name)

        # 1000 pts at largest
        ntotal = FI.shape[0]
        if ntotal > 1000:
            # get PDF of FI for EMST
            hist, bin_edges = np.histogram(
                    FI[:,-1],
                    bins=30,
                    range=(0,1),
                    density=True
                    )

            rect = 0.695, axsb[i], 0.09, 0.08
            axs = fig.add_axes(rect)
            axs.set_xlim(0,1)
            axs.set_xticks([0,0.5,1])
            axs.set_xticklabels(['-1','0','1'])
            axs.set_yticks([])
            axs.tick_params(length=0,pad=0.2,labelsize=6)
            axs.spines["right"].set_color('none')
            axs.spines["top"].set_color('none')
            axs.set_facecolor('none')

            axs.plot((bin_edges[:-1]+bin_edges[1:])/2,hist,'k-',lw=1)

            idx = np.random.randint(0,ntotal,200)
            FI = FI[idx,:]

        cplt = ax[i,j].scatter(FI[:,0],FI[:,2],c=FI[:,1],
                               vmin=0,vmax=0.28,
                               marker='.',cmap='coolwarm')
        ax[i,j].set_ylim(0,1)
    ax[i,0].set_ylabel(r'$\mathrm{FI}$')
    ax[i,0].set_yticks([0,0.5,1])
    ax[i,0].set_yticklabels(['-1','0','1'])

for j in range(num_cols):
    ax[-1,j].set_xlabel('$Z$')
    ax[0,j].set_title(models[j])

xlim_lb = xlim0
xlim_ub = xlim1
ax[0,0].set_xlim(xlim_lb,xlim_ub)
ax[0,0].text(xlim_lb+xfac*(xlim_ub-xlim_lb),0.55,
             ''.join(['$a=$',
                      '{:g}'.format(strain[0]),
                      r'$\;\mathrm{s}^{-1}$',
                      '\n',
                      r'$\eta_Z=$',
                      '{:g}'.format(variance),
                      '\n',
                      r'$\varphi_r=$',
                      '{:g}'.format(phif[0])
                      ])
             )

xlim_ub = 0.11
xlim_lb = Zst-(Zst-xlim0)/(xlim1-Zst)*(xlim_ub-Zst)
ax[1,0].set_xlim(xlim_lb,xlim_ub)
ax[1,0].text(xlim_lb+xfac*(xlim_ub-xlim_lb),0.55,
             ''.join(['$a=$',
                      '{:g}'.format(strain[1]),
                      r'$\;\mathrm{s}^{-1}$',
                      '\n',
                      r'$\eta_Z=$',
                      '{:g}'.format(variance),
                      '\n',
                      r'$\varphi_r=$',
                      '{:g}'.format(phif[1])
                      ])
             )


xlim_ub = 0.14
xlim_lb = Zst-(Zst-xlim0)/(xlim1-Zst)*(xlim_ub-Zst)
ax[2,0].set_xlim(xlim_lb,xlim_ub)
ax[2,0].text(xlim_lb+xfac*(xlim_ub-xlim_lb),0.55,
             ''.join(['$a=$',
                      '{:g}'.format(strain[2]),
                      r'$\;\mathrm{s}^{-1}$',
                      '\n',
                      r'$\eta_Z=$',
                      '{:g}'.format(variance),
                      '\n',
                      r'$\varphi_r=$',
                      '{:g}'.format(phif[2])
                      ])
             )
ax[2,0].set_xticks([0.03, 0.06, 0.09, 0.12])


fig.subplots_adjust(
    left = margin_left/plot_width,
    bottom = margin_bottom/plot_height,
    right = 1.0-margin_right/plot_width,
    top = 1.0-margin_top/plot_height,
    wspace = space_width/plot_width,
    hspace = space_height/plot_height
    )

cax = fig.add_axes([0.5/plot_width,
                    (plot_height-0.4)/plot_height,
                    2.2/plot_width,
                    0.12/plot_height])
clb = fig.colorbar(cplt,cax=cax,orientation='horizontal')
clb.set_ticks([0.05,0.15,0.25])
cax.tick_params(axis='x',pad=0.1,length=2,labelsize='small')
cax.xaxis.set_ticks_position('top')
fig.text(0.2/plot_width,(plot_height-0.3)/plot_height,'$c$')

fig.savefig('{}/FI_scatter_var005.pdf'.format(dst))
fig.savefig('{}/FI_scatter_var005.eps'.format(dst))
plt.close('all')
