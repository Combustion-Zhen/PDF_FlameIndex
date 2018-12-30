
# coding: utf-8

# In[1]:


import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import figureSize
from filename import params2name
import cantera as ct
import canteraFlame


# In[2]:


models = ['IEM','MC','EMST']

phif = [2.4, 4.8, float('inf')]

Zst = 0.0551863

dst = 'figs_sample_scatter'


# In[3]:


flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = 200
flame_params['phif'] = None
flame_params['phio'] = 0
flame_params['tf'] = 300
flame_params['to'] = 300
flame_params['ave'] = 0.065
flame_params['var'] = 0.05

folder_params= {}
folder_params['phif'] = None
folder_params['phio'] = 0


# In[4]:


# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 19.0
margin_left   = 1.2
margin_right  = 0.1
margin_bottom = 1.2
margin_top    = 0.8
space_width   = 0.4
space_height  = 0.8
# for the special column of c-Z plot
space_s_w     = 1.0

ftsize        = 11

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
plt.rc('text.latex', preamble=[r'\usepackage{amsmath}',r'\usepackage{bm}'])
# use serif font
plt.rc('font',**font)


num_cols = len(models)
num_rows = len(phif)

subplot_width = (plot_width
                 -space_s_w
                 -margin_left
                 -margin_right
                 -(num_cols-1)*space_width
                )/(num_cols+1)
subplot_height = subplot_width * 0.7

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)


# In[5]:


fig, ax = plt.subplots(num_rows,num_cols,
                       sharex='row',sharey=True,
                       figsize=figureSize.cm2inch(plot_width,plot_height))

for i, phi in enumerate(phif):
    flame_params['phif'] = phi
    folder_params['phif'] = phi

    folder = params2name(folder_params)
    flame = params2name(flame_params)

    for j, model in enumerate(models):

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

            rect = [0.9,
                    (margin_bottom+(2-i)*(space_height+subplot_height)+0.35)/plot_height,
                    0.09,
                    0.08]
            axs = fig.add_axes(rect)
            axs.set_xlim(0,1)
            axs.set_xticks([0,0.5,1])
            axs.set_xticklabels(['-1','0','1'])
            axs.set_yticks([])
            axs.tick_params(length=0,pad=0.2,labelsize=11)
            axs.spines["right"].set_color('none')
            axs.spines["top"].set_color('none')
            axs.set_facecolor('none')

            axs.plot((bin_edges[:-1]+bin_edges[1:])/2,hist,'k-',lw=1)

            FI = FI[:501,:]

        cplt = ax[i,j].scatter(FI[:,0],FI[:,-1],c=FI[:,1],
                               vmin=0,vmax=0.28,
                               marker='.',cmap='coolwarm')
        ax[i,j].set_ylim(0,1)
    ax[i,0].set_ylabel(r'$\mathrm{FI}$')
    ax[i,0].yaxis.set_label_coords(-0.12,0.5)
    ax[i,0].set_yticks([0,0.5,1])
    ax[i,0].set_yticklabels(['-1','0','1'])
    ax[i,0].set_xlim([0, 0.21])
    
for j in range(num_cols):
    ax[-1,j].set_xlabel('$Z$')
    ax[0,j].set_title(models[j])

fig.subplots_adjust(
    left = (margin_left+space_s_w+subplot_width)/plot_width,
    bottom = margin_bottom/plot_height,
    right = 1.0-margin_right/plot_width,
    top = 1.0-margin_top/plot_height,
    wspace = space_width/subplot_width,
    hspace = space_height/subplot_height
    )

cax = fig.add_axes([3.5/plot_width,
                    (plot_height-0.6)/plot_height,
                    2.2/plot_width,
                    0.15/plot_height])
clb = fig.colorbar(cplt,cax=cax,orientation='horizontal')
clb.set_ticks([0.05,0.15,0.25])
cax.tick_params(axis='x',pad=0.1,length=2,labelsize=9)
cax.xaxis.set_ticks_position('top')
fig.text(3.2/plot_width,(plot_height-0.5)/plot_height,'$c$')

del flame_params['ave']
del flame_params['var']

speciesProgressVariable = ['CO2', 'CO', 'H2O', 'H2']

p = flame_params['p']*ct.one_atm

fuel = ct.Solution('gri30.xml')
fuel.TPX = flame_params['tf'], p, {flame_params['F']:1}

oxidizer = ct.Solution('gri30.xml')
oxidizer.TPX = flame_params['to'], p, {'O2':1,'N2':3.76}

Zst = canteraFlame.StoichiometricMixtureFraction( fuel, oxidizer )

gas = ct.Solution('gri30.xml')
f = ct.CounterflowDiffusionFlame(gas, width=0.01)

for i, phi in enumerate(phif):
    axf = fig.add_axes(
        [margin_left/plot_width,
         (margin_bottom+(2-i)*(space_height+subplot_height))/plot_height,
         subplot_width/plot_width,
         subplot_height/plot_height])

    folder_params['phif'] = phi
    flame_params['phif'] = phi

    folder = params2name(folder_params)
    flame = params2name(flame_params)
    
    file_name = '{}/{}.xml'.format(folder,flame)
    f.restore( file_name, loglevel=0 )
    
    Z = canteraFlame.BilgerMixtureFraction( f, fuel, oxidizer )
    c = canteraFlame.ProgressVariable( f, speciesProgressVariable )
    
    axf.plot(Z,c,lw=1)
    axf.plot([0,Zst,1],[0,Zst*5,0],'k:',lw=1)
    
    axf.set_xlim([0,0.21])
    axf.set_ylim([0,0.3])
    axf.set_ylabel(r'$c$')
    
    text_loc = 0.03
    if phi != float('inf'):
        axf.text(text_loc,0.01,
                 ''.join([
                     r'$\varphi_l\,=$',
                     '{:g}'.format(0),
                     '\n',
                     r'$\varphi_r=$',
                     '{:g}'.format(phi)
                 ]))
    else:
        axf.text(text_loc,0.01,
                 ''.join([
                     r'$\varphi_l\,=$',
                     '{:g}'.format(0),
                     '\n',
                     r'$\varphi_r=\infty$'
                 ]))

axf.set_xlabel(r'$Z$')


# In[6]:


fig.savefig('figFlameIndexScatter.png'.format(dst))
fig.savefig('figFlameIndexScatter.eps'.format(dst))

