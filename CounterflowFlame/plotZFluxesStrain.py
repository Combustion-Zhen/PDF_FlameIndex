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
margin_right    =0.3
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

linestyle = ['-', '--', '-.', ':']

strain = np.array([50, 100, 200, 400])

speciesProgressVariable = ['CO2', 'CO', 'H2O', 'H2']
slopeProgressVariable = 5.

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = 200
flame_params['phif'] = 'inf'
flame_params['phio'] = 0
flame_params['tf'] = 300
flame_params['to'] = 300
flame_name = params2name( flame_params )

p = flame_params['p']*ct.one_atm

fuel = ct.Solution('gri30.xml')
fuel.TPX = flame_params['tf'], p, {flame_params['F']:1}

oxidizer = ct.Solution('gri30.xml')
oxidizer.TPX = flame_params['to'], p, {'O2':1,'N2':3.76}

Zst = canteraFlame.StoichiometricMixtureFraction( fuel, oxidizer )

gas = ct.Solution('gri30.xml')
f = ct.CounterflowDiffusionFlame(gas, width=0.01)

f.restore( '{}.xml'.format(flame_name), loglevel=0 )

Z = canteraFlame.BilgerMixtureFraction( f, fuel, oxidizer )

C, D, S = canteraFlame.TransportBudget( f )

vMixtureFraction = canteraFlame.VectorMixtureFractionForMassFraction(
        fuel, oxidizer )
vProgressVariable = canteraFlame.VectorProgressVariableForMassFraction(
        gas, speciesProgressVariable )

fluxMixtureFraction = np.dot( D.transpose(), vMixtureFraction )
fluxProgressVariable = np.dot( D.transpose(), vProgressVariable )

omegaProgressVariable = canteraFlame.ProgressVariableReactionRate(
        f, speciesProgressVariable )

convProgressVariable = np.dot( C.transpose(), vProgressVariable )

ax.plot( Z, fluxMixtureFraction, 'k-',
         label = r'$\nabla\cdot(\rho D \nabla Z)$', 
         lw = 1 )

ax.plot( Z, convProgressVariable, 'm:',
         label = r'$\rho u \nabla c$',
         lw = 1 )

ax.plot( Z, fluxProgressVariable, 'b-.',
         label = r'$\nabla\cdot(\rho D \nabla c)$', 
         lw = 1 )

ax.plot( Z, omegaProgressVariable, 'r--',
         label = r'$\dot{\omega}_c$', 
         lw = 1 )

ax.legend( frameon = False )

ax.set_xlim(0,1)

ax.set_xlabel(r'$Z$')
ax.set_ylabel('Transport Budget '+r'$(\mathrm{kg/(m^3\cdot s)})$')

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/subplot_width,
        hspace = space_height/subplot_height
        )

fig.savefig('figZFluxes.eps')
fig.savefig('figZFluxes.png')
