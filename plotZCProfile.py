# plot progress variable versus mixture fraction with different strain rate
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import figureSize
from filename import params2name
import canteraFlame

# figure specification
plot_width      =19.0
margin_left     =1.8
margin_right    =0.2
margin_bottom   =1.2
margin_top      =0.3
space_width     =2.0
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

ncol = 2
nrow = 1

plot_height, subplot_height, subplot_width = figureSize.UniformSubplots(
    plot_width, [nrow, ncol], subplot_ratio, 
    [margin_left, margin_bottom, margin_right, margin_top],
    [space_height, space_width])

fig, ax = plt.subplots(
        nrow, ncol,
        figsize=figureSize.cm2inch(plot_width,plot_height) )

#

speciesProgressVariable = ['CO2', 'CO', 'H2O', 'H2']
slopeProgressVariable = 5.

linestyle = ['-.', '--', '-']

strain = np.array([100, 200, 400])

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = None
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

ax[0].plot([0., Zst, 1.], 
        [0., slopeProgressVariable*Zst, 0.], 
        'k:', lw=1, label=r'$\mathrm{Da}\rightarrow\infty$')

for i, a in enumerate(strain):

    flame_params['a'] = a

    label = r'$a=\;$'+'{:g}'.format(a)+r'$\;\mathrm{s}^{-1}$'

    flame_name = params2name( flame_params )
    file_name = '/'.join(['CounterflowFlame',
                          'CH4',
                          'phif-inf_phio-0',
                          '{}.xml'.format(flame_name)])
    f.restore( file_name, loglevel=0 )

    Z = canteraFlame.BilgerMixtureFraction( f, fuel, oxidizer )
    c = canteraFlame.ProgressVariable( f, speciesProgressVariable )

    ax[0].plot( Z, c, label=label, ls=linestyle[i], lw=1 )

eqvList = [0.4, 0.7, 1.0, 1.4, 1.8, 2.4]

linestyle = ['--', '-.', '-', '--', '-.', '-']
linewidth = [ 1, 1, 1, 2, 2, 2 ]

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['T'] = 300
flame_params['eqv'] = None

p = flame_params['p'] * ct.one_atm

fuel = ct.Solution('gri30.xml')
fuel.TPX = flame_params['T'], p, {flame_params['F']:1}

oxidizer = ct.Solution('gri30.xml')
oxidizer.TPX = flame_params['T'], p, {'O2':1,'N2':3.76}

Zst = canteraFlame.StoichiometricMixtureFraction( fuel, oxidizer )

gas = ct.Solution('gri30.xml')
f = ct.FreeFlame(gas, width=0.03)

for i, eqv in enumerate(eqvList) :

    flame_params['eqv'] = eqv
    flame_name = params2name( flame_params )
    file_name = '/'.join(['FreelyPropagatingFlame',
                          'CH4',
                          '{}.xml'.format(flame_name)])
    f.restore( file_name, loglevel=0 )

    Z = canteraFlame.BilgerMixtureFraction( f, fuel, oxidizer )
    c = canteraFlame.ProgressVariable( f, speciesProgressVariable )

    label = r'$\varphi$'+'={:g}'.format(eqv)

    ax[1].plot( Z, c, 
             ls=linestyle[i], lw=linewidth[i],
             label=label )

for i in range(ncol):
    ax[i].legend(handlelength=3, frameon=False)

    ax[i].plot([0., Zst, 1.], 
               [0., slopeProgressVariable*Zst, 0.], 
               'k:', lw=1, label=r'Da')

    ax[i].set_xlabel(r'$Z$')
    ax[i].set_ylabel(r'$c$')

ax[0].text( 0.15, 0.27, '(a)' )
ax[1].text( 0.0315, 0.27, '(b)' )

ax[0].set_xlim(0, 1)
ax[0].set_ylim(0, 0.3)

ax[1].set_xlim(0, 0.21)
ax[1].set_ylim(0, 0.3)

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/subplot_width,
        hspace = space_height/subplot_height
        )

fig.savefig('figZCProfile.eps')
fig.savefig('figZCProfile.png')
