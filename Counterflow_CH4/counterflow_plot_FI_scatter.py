"""
Zhen Lu 2017/11/07

scatter plot of constructed subgrid
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

eqv = 1.2
Zmin = 0.02

loc_legend = (0., 0.45)

Zst = 0.0551863

variance = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
phif   = [1.3, 1.7, 2.3, 3.2, 4.8]
strain = [100, 150, 200, 250, 300]
eqv_ratio = [0.8,0.9,1.0,1.1,1.2,1.3,1.4]

dst = 'figs_sample_scatter_all'

models = ['IEM','MC','EMST']

folder_params = {}
folder_params['phif'] = None
folder_params['phio'] = 0

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = None
flame_params['phif'] = None
flame_params['phio'] = 0
flame_params['tf'] = 300
flame_params['to'] = 300
flame_params['eqv'] = None
flame_params['var'] = None

plot_params = {}
plot_params['a'] = None
plot_params['phif'] = None
plot_params['var'] = None

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 19.0
margin_left   = 1.6
margin_right  = 0.1
margin_bottom = 1.2
margin_top    = 0.2
space_width   = 0.
space_height  = 0.
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
subplot_height = subplot_width * 0.5

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

flame_params['eqv'] = eqv

for a in strain:
    flame_params['a'] = a
    for var in variance:
        flame_params['var'] = var

        for a in strain:
            flame_params['a'] = a
            for phi in phif:
                folder_params['phif'] = phi
                flame_params['phif'] = phi

                Zlim = equiv2Z(phi,Zst)

                folder = params2name(folder_params)

                # get data
                flame = params2name(flame_params)

                label = r'$\varphi_r=$'+'{0:g}'.format(phi)

                flame_params['eqv'] = eqv

                # generate figure and axes
                fig, ax = plt.subplots(num_rows,num_cols,
                                       sharex=True,sharey=True,
                                       figsize=cm2inch(plot_width,
                                                       plot_height))

#        fig.text(0.05,0.95,''.join([r'$\eta_Z=$','{:g}'.format(var)]))
#            ax[i,1].text(0.045,0.52,r'$\tilde{\mathrm{FI}}=0.5$')

                for j, model in enumerate(models):

                    file_name = '{}/{}.{}'.format(folder,flame,model)

                    ax[j].plot([0,1],[0.5,0.5],'k--',linewidth=1)
                    ax[j].plot([Zst,Zst],[0,1],'k-.',linewidth=1)

                    if not os.path.exists(file_name):
                        continue
                    # Z, C, FI
                    FI = np.genfromtxt(file_name)

                    # 1000 pts at largest
                    ntotal = FI.shape[0]
                    if ntotal > 1000:
                        idx = np.random.randint(0,ntotal,200)
                        FI = FI[idx,:]

                    cplt = ax[j].scatter(FI[:,0],FI[:,2],c=FI[:,1],
                                         marker='.',cmap='seismic')

                    ax[j].text(Zmin,0.55,
                               ''.join([model,
                                        '\n',
                                        r'$a\;\;=$',
                                        '{:g}'.format(a),
                                        r'$\;\mathrm{s}^{-1}$',
                                        '\n',
                                        r'$\eta_Z=$',
                                        '{:g}'.format(var)]))

                    ax[j].set_xlim(Zmin,Zlim*1.05)
                    ax[j].set_xlabel('$Z$')
                    ax[j].set_ylim(0.,1.)

                ax[0].set_ylabel('FI')

                # colorbar
                cbar = fig.colorbar(cplt)

                # file name for plot
                plot_params['a'] = flame_params['a']
                plot_params['phif'] = flame_params['phif']
                plot_params['var'] = flame_params['var']

                fig.subplots_adjust(
                    left = margin_left/plot_width,
                    bottom = margin_bottom/plot_height,
                    right = 1.0-margin_right/plot_width,
                    top = 1.0-margin_top/plot_height,
                    wspace = space_width/plot_width,
                    hspace = space_height/plot_height
                    )

                plot_name = params2name(plot_params)

                fig.savefig('{0}/FI_scatter_{1}.pdf'.format(dst,plot_name))
                plt.close('all')
