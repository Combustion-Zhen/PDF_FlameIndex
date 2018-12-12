# plot progress variable versus mixture fraction with different strain rate
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import figureSize
from filename import params2name
import canteraFlame

# figure specification
plot_width      =9.0
margin_left     =1.8
margin_right    =0.2
margin_bottom   =1.2
margin_top      =0.3
space_width     =1.0
space_height    =1.0
subplot_ratio   =0.8
ftsize          =11

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
plt.rc('text.latex', preamble=[r'\usepackage{amsmath}',r'\usepackage{bm}'])
# use serif font
plt.rc('font',**font)

ncol = 1
nrow = 1

plot_height, subplot_height, subplot_width = figureSize.UniformSubplots(
    plot_width, [nrow, ncol], subplot_ratio, 
    [margin_left, margin_bottom, margin_right, margin_top],
    [space_height, space_width])

fig, ax = plt.subplots(
        nrow, ncol, figsize=figureSize.cm2inch(plot_width,plot_height) )

#

phif = [1.2, 2.4, 4.8, float('inf')]

linestyle = ['-', '--', '-.', ':']
linecolor = ['r', 'm', 'b', 'k']

speciesProgressVariable = ['CO2', 'CO', 'H2O', 'H2']
slopeProgressVariable = 5.

folder_params = {}
folder_params['phif'] = float('inf')
folder_params['phio'] = 0

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = 200
flame_params['phif'] = 'inf'
flame_params['phio'] = 0
flame_params['tf'] = 300
flame_params['to'] = 300

p = flame_params['p']*ct.one_atm

fuel = ct.Solution('gri30.xml')
fuel.TPX = flame_params['tf'], p, {flame_params['F']:1}

oxidizer = ct.Solution('gri30.xml')
oxidizer.TPX = flame_params['to'], p, {'O2':1,'N2':3.76}

Zst = canteraFlame.StoichiometricMixtureFraction( fuel, oxidizer )

gas = ct.Solution('gri30.xml')
f = ct.CounterflowDiffusionFlame(gas, width=0.01)

for i, phi in enumerate(phif):

    folder_params['phif'] = phi
    flame_params['phif'] = phi

    label = r'$\varphi_r=\;$'+'{:g}'.format(phi)

    if phi == float('inf'):
        label = r'$\varphi_r=\infty$'

    folderName = params2name( folder_params )
    flameName = params2name( flame_params )

    fileName = '{}/{}.xml'.format( folderName, flameName )

    f.restore( fileName, loglevel=0 )

    Z = canteraFlame.BilgerMixtureFraction( f, fuel, oxidizer )

    rangeIndex = np.where(np.logical_and( Z < 0.06, Z > 0.05 ))
    rangeZ = Z[ rangeIndex ]
    rangeGrid = f.grid[ rangeIndex ]
    locZst = np.interp( Zst, rangeZ[::-1], rangeGrid[::-1])

    ax.plot( locZst-f.grid, f.T, label = label,
             ls=linestyle[i], c=linecolor[i], lw=1 )

#    omega = canteraFlame.ProgressVariableReactionRate( 
#            f, speciesProgressVariable )
#
#    ax.plot( locZst-f.grid, omega, label = label,
#             ls=linestyle[i], c=linecolor[i], lw=1 )

ax.legend(frameon=False,loc='upper left')

xlim = 0.002
ax.set_xlim(-xlim, xlim)
ax.set_xticks(np.linspace(-xlim, xlim, num=5))
ax.set_xticklabels(np.linspace(-xlim*1000,xlim*1000,num=5))
#ax.set_ylim(275, 2100)

ax.set_xlabel(r'$x\;\mathrm{(mm)}$')
ax.set_ylabel(r'$T\;\mathrm{(K)}$')

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/subplot_width,
        hspace = space_height/subplot_height
        )

fig.savefig('fig_flameT_phi.eps')
