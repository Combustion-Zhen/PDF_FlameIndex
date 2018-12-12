# plot progress variable versus mixture fraction with different strain rate
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import figureSize
from filename import params2name
import canteraFlame

# figure specification
plot_width      =9.0
margin_left     =1.5
margin_right    =0.3
margin_bottom   =1.2
margin_top      =0.2
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

#fig, ax = plt.subplots(
#        nrow, ncol, figsize=figureSize.cm2inch(plot_width,plot_height) )

fig = plt.figure( figsize = figureSize.cm2inch( plot_width, plot_height ),
                  frameon = True )

axRatio = 0.618

rect = (margin_left/plot_width,
        margin_bottom/plot_height,
        axRatio*subplot_width/plot_width,
        subplot_height/plot_height)
ax0 = fig.add_axes(rect)

rect = ((margin_left+axRatio*subplot_width)/plot_width,
        margin_bottom/plot_height,
        (1-axRatio)*subplot_width/plot_width,
        subplot_height/plot_height)
ax1 = fig.add_axes(rect)

#

phif = [1.2, 1.8, 2.4, 3.2, 4.8, 9.6, float('inf')]
phio = [0, 0.2, 0.4, 0.6]

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
Zsp = 0.125

gas = ct.Solution('gri30.xml')
f = ct.CounterflowDiffusionFlame(gas, width=0.01)

folder_params['phif'] = float('inf')
flame_params['phif'] = float('inf')

for phi in phio:

    folder_params['phio'] = phi
    flame_params['phio'] = phi

    folderName = params2name( folder_params )
    flameName = params2name( flame_params )

    fileName = '{}/{}.xml'.format( folderName, flameName )

    f.restore( fileName, loglevel=0 )

    Z = canteraFlame.BilgerMixtureFraction( f, fuel, oxidizer )
    c = canteraFlame.ProgressVariable( f, speciesProgressVariable )

    ax0.plot( Z, c, lw=1 )
    ax1.plot( Z, c, lw=1 )

folder_params['phio'] = 0
flame_params['phio'] = 0

for phi in phif:

    folder_params['phif'] = phi
    flame_params['phif'] = phi

    folderName = params2name( folder_params )
    flameName = params2name( flame_params )

    fileName = '{}/{}.xml'.format( folderName, flameName )

    f.restore( fileName, loglevel=0 )

    Z = canteraFlame.BilgerMixtureFraction( f, fuel, oxidizer )
    c = canteraFlame.ProgressVariable( f, speciesProgressVariable )

    ax0.plot( Z, c, lw=1 )
    ax1.plot( Z, c, lw=1 )

ax0.plot([0., Zst, 1.], 
         [0., slopeProgressVariable*Zst, 0.], 
         'k:', lw=1)
ax1.plot([0., Zst, 1.], 
         [0., slopeProgressVariable*Zst, 0.], 
         'k:', lw=1)

ax0.text(0.056,-0.04,
           r'$Z_\mathrm{st}$')
ax0.annotate(
    '',xy=(Zst,0.005),xytext=(Zst,-0.03),
    arrowprops=dict(arrowstyle="-",color="k",lw=0.5,ls='--')
    )

ax0.set_xlim(0, Zsp)
ax0.set_xticks([0,0.04,0.08,0.12])
ax0.set_ylim(0, 0.3)
ax0.spines['right'].set_visible(False)

ax1.set_xlim(Zsp, 1)
ax1.set_ylim(0, 0.3)
ax1.set_yticks([])
ax1.spines['left'].set_visible(False)
ax1.plot([Zsp, Zsp], [0, 1], 'k-.', lw=1)

ax0.set_xlabel(r'$Z$')
ax0.set_ylabel(r'$c$')
ax0.xaxis.set_label_coords(0.8,-0.12)

## text
#
ax0.annotate(
        r'$(0.2,\infty)$',
        xy = (0.021, 0.075),
        xytext= (0.002, 0.2),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )

ax0.annotate(
        ''.join([
            r'$(\varphi_l,\varphi_r)$',
            '\n',
            r'$=(0,\infty)$'
            ]),
        xy = (0.062,0.25),
        xytext = (0.002,0.25),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax0.annotate(
        r'$(0.6,\infty)$',
        xy = (0.033, 0.045),
        xytext= (0.044, 0.04),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax0.annotate(
        r'$(0.4,\infty)$',
        xy = (0.027, 0.075),
        xytext= (0.044, 0.07),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax0.text(0.044, 0.1,
         r'$(0, 1.2)$')

ax0.text(0.08, 0.013,
         r'$(0,1.8)$')

ax0.text(0.09, 0.1,
         r'$(0,2.4)$')

ax0.text(0.09,0.17,
           r'$(0,3.2)$')

ax0.text(0.09,0.215,
           r'$(0,4.8)$')

ax0.text(0.145, 0.013,
         r'$(0,9.6)$')

ax1.text(
        0.98,0.19,
        ''.join([r'$\mathrm{CH}_4/\mathrm{Air}$',
                 '\n',
                 '$a=200\;\mathrm{s}^{-1}$',
                 '\n',
                 r'$p\;\;=1\;\mathrm{atm}$',
                 '\n',
                 r'$T_l\,=300\;\mathrm{K}$',
                 '\n',
                 r'$T_r=300\;\mathrm{K}$'
                 ]),
        horizontalalignment = 'right'
        )

ax0.text(0.078,0.28, 'scale split')

fig.savefig('fig_ZC_phi.eps')
