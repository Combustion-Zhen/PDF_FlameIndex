import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import figureSize
from filename import params2name
import canteraFlame
import sys
sys.path.append('/home/luz0a/Documents/flamelet2table')
import beta_integration

################################################################################

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

flame_name = params2name( flame_params )
f.restore( '{}.xml'.format(flame_name), loglevel=0 )

################################################################################

speciesProgressVariable = ['CO2', 'CO', 'H2O', 'H2']
slopeProgressVariable = 5.

Z = canteraFlame.BilgerMixtureFraction( f, fuel, oxidizer )
lagrangianFI = canteraFlame.LagrangianFlameIndex( f, fuel, oxidizer )

# remove spurius points on the boundaries
Z = Z[-5:5:-1]
lagrangianFI = lagrangianFI[-5:5:-1]

Z = np.insert(Z, 0, 0)
Z = np.append(Z, 1)
lagrangianFI = np.insert( lagrangianFI, 0, lagrangianFI[0])
lagrangianFI = np.append( lagrangianFI, lagrangianFI[-1])

# remove duplication at Z direction
differenceZ = Z[1:] - Z[:-1]
indexNonDuplication = np.insert( np.array(np.where(differenceZ > 1.E-9)) + 1, 
                                 0, 0 )

# generate integrated data
axisMean = np.linspace(0, 0.2, num = 101)
axisVar = np.linspace(0, 0.1, num = 81)

integratedFI = beta_integration.beta_integration_table(
    lagrangianFI[indexNonDuplication], 
    Z[indexNonDuplication], 
    axisMean, 
    axisVar)

X, Y = np.meshgrid(axisVar, axisMean)

################################################################################

# figure specification
plot_width      =9.0
margin_left     =0.
margin_right    =0.
margin_bottom   =0.5
margin_top      =0.
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

fig = plt.figure(figsize=figureSize.cm2inch(plot_width, plot_width))
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect(0.618)

surf = ax.plot_surface(X, Y, integratedFI,
                       cmap=cm.rainbow, vmin=-1, vmax=1,
                       rstride=1, cstride=1,
                       linewidth=1, antialiased=False)

ax.set_xlim3d(0,0.1)
ax.set_ylim3d(0,0.2)
ax.set_zlim3d(-1,1)

ax.set_xlabel('$\eta_Z$')
ax.set_ylabel('$Z$')
ax.set_zlabel('FI')

cax = fig.add_axes([0.3/plot_width, 2.5/plot_height, 0.3/plot_width, 3/plot_height])
cbar = fig.colorbar(surf, cax=cax)
cbar.set_ticks([-1, 0, 1])
cax.set_title('FI')

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/subplot_width,
        hspace = space_height/subplot_height
        )

fig.savefig('figIntegratedFlameIndexPhifInf.eps')
