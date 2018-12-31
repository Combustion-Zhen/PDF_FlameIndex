import os
import glob
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import figureSize
from filename import params2name, name2params
import cantera as ct
import canteraFlame

phif   = [2.4, 4.8, float('inf')]
lineColor = ['r','b','k']
lineStyle = ['-','-.','--']

models = ['IEM','MC','EMST']

folder_params = {}
folder_params['phif'] = None
folder_params['phio'] = 0

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 19.0
margin_left   = 1.2
margin_right  = 0.1
margin_bottom = 1.2
margin_top    = 0.3
space_width   = 0.5
space_height  = 0.5
subplot_ratio = 0.8
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
num_rows = 1

plot_height, subplot_height, subplot_width = figureSize.UniformSubplots(
    plot_width, [num_rows, num_cols], subplot_ratio, 
    [margin_left, margin_bottom, margin_right, margin_top],
    [space_height, space_width])

# generate figure and axes
fig, ax = plt.subplots(
        num_rows,num_cols,
        sharex=True,sharey=True,
        figsize=figureSize.cm2inch(plot_width,plot_height))

#for i in range(num_cols):
#    ax[i].plot([0,1],[0.5,0.5],'k:',linewidth=1)

# get data
for k, phi in enumerate(phif):
    folder_params['phif'] = phi

    folder = params2name(folder_params)

    label = r'$\varphi_r=$'+'{0:g}'.format(phi)

    os.chdir(folder)

    for i, model in enumerate(models):
        fileList = glob.glob('*.{}'.format(model))
        data = np.zeros((len(fileList), 2))

        for j, fileName in enumerate(fileList):
            flameName = fileName[:fileName.find(model)]
            flameParams = name2params(flameName)
            data[j,0] = flameParams['ave']

            FI = np.genfromtxt(fileName, usecols=(3,))
            data[j,1] = np.average(FI)

        data = data[data[:,0].argsort()]

        ax[i].plot(data[:,0], data[:,1], 
                   c = lineColor[k], ls = lineStyle[k],
                   label=label, lw=1)

    os.chdir('..')

for i in range(num_cols):
    ax[i].set_xlabel(r'$\widetilde{Z}$')
ax[0].set_ylabel(r'FI')

ax[0].set_xlim(0, 0.21)
ax[0].set_xticks([0, 0.05, 0.1, 0.15, 0.2])
ax[0].set_ylim(0, 1)
ax[0].set_yticks([0, 0.5, 1])
ax[0].set_yticklabels([-1, 0, 1])

ax[0].text(0.005,0.82,
           ''.join([r'$a\;\;\,\!=200\;\mathrm{s}^{-1}$',
                    '\n',
                    r'$\eta_Z=0.05$']))

ax[-1].legend(loc='lower right',
              frameon=False
             )

fig.subplots_adjust(
    left = margin_left/plot_width,
    bottom = margin_bottom/plot_height,
    right = 1.0-margin_right/plot_width,
    top = 1.0-margin_top/plot_height,
    wspace = space_width/subplot_width,
    hspace = space_height/subplot_height
    )

fig.savefig('figFlameIndexAverage.eps')
