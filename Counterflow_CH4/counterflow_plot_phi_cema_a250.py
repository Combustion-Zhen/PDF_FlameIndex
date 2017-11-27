"""
Zhen Lu 2017/11/11

plot counterflow profiles colored by CEMA results
"""

import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

phif   = [1.3, 1.7, 2.3, 3.2, 4.8, float('inf')]
phio = [0, 0.05, 0.1, 0.2, 0.3]

#strain = [100, 150, 200, 250, 300]
a = 250

dst = 'figs_phif_cema'

Zst = 0.0551863
Zp = 0.06
beta = 5

folder_params = {}
folder_params['phif'] = float('inf')
folder_params['phio'] = 0

flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1
flame_params['a'] = 100
flame_params['phif'] = float('inf')
flame_params['phio'] = 0
flame_params['tf'] = 300
flame_params['to'] = 300

# plot
# use TEX for interpreter
plt.rc('text',usetex=True)
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.1
margin_right  = 1.4
margin_bottom = 0.8
margin_top    = 0.1
space_width   = 0.5
space_height  = 1.0
ftsize        = 7

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

plt.rc('font',**font)

nrow = 1
ncol = 2

subplot_width = (plot_width-margin_left-margin_right-(ncol-1)*space_width)/2
subplot_height = subplot_width * 0.7

plot_height = (nrow*subplot_height
              +margin_bottom
              +margin_top
              +(nrow-1)*space_height)

flame_params['a'] = a

# generate figure and axes
fig, ax = plt.subplots(nrow,ncol,sharey=True,
                       figsize=cm2inch(plot_width,plot_height))

# get data
folder_params['phif'] = float('inf')
flame_params['phif'] = float('inf')
for phi in phio:
    folder_params['phio'] = phi
    flame_params['phio'] = phi

    folder = params2name(folder_params)
    flame = params2name(flame_params)

    label = r'$\varphi_r=$'+'{0:g}'.format(phi)

    file_name = '{}/{}.dat'.format(folder,flame)
    cema_name = '{}/{}.cema'.format(folder,flame)

    if not os.path.exists(file_name):
        continue
    data = np.genfromtxt(file_name,skip_header=3,names=True)

    # scalar dissipation rate
    gradZ = np.gradient(data['Z'],data['grid'])
    chi = 2.*data['nu']/0.8*gradZ*gradZ

    cema = np.genfromtxt(cema_name,usecols=(0,))
    lamb = cema-chi

    cema = np.sign(cema)*np.log10(1+np.absolute(cema))
    lamb = np.sign(lamb)*np.log10(1+np.absolute(lamb))

    cplt = ax[0].scatter(data['Z1'],data['C_4spe'],
                         s=5,marker='.',
                         c=lamb,vmin=-3,vmax=3,cmap='jet')

folder_params['phio'] = 0
flame_params['phio'] = 0
for phi in phif:
    folder_params['phif'] = phi
    flame_params['phif'] = phi

    folder = params2name(folder_params)
    flame = params2name(flame_params)

    label = r'$\varphi_r=$'+'{0:g}'.format(phi)

    file_name = '{}/{}.dat'.format(folder,flame)
    cema_name = '{}/{}.cema'.format(folder,flame)

    if not os.path.exists(file_name):
        continue
    data = np.genfromtxt(file_name,skip_header=3,names=True)

    # scalar dissipation rate
    gradZ = np.gradient(data['Z'],data['grid'])
    chi = 2.*data['nu']/0.8*gradZ*gradZ

    cema = np.genfromtxt(cema_name,usecols=(0,))
    lamb = cema-chi

    cema = np.sign(cema)*np.log10(1+np.absolute(cema))
    lamb = np.sign(lamb)*np.log10(1+np.absolute(lamb))

    cplt = ax[1].scatter(data['Z1'],data['C_4spe'],
                         s=5,marker='.',
                         c=lamb,vmin=-3,vmax=3,cmap='jet')

# text

# beta
ax[0].plot([0,Zp],[0,Zp*beta],
           'k:',linewidth=1)
ax[0].text(0.017,0.1,
           r'$\beta$'
           )
# Zst
ax[0].plot([Zst,Zst],[0,Zp*beta],
           'k-.',linewidth=1)
ax[0].text(0.05,0.1,
           '$Z_{st}$'
           )

# labels
#ax[0].text(0.033,0.01,
#           r'$\varphi_l=0.3$')
#ax[0].text(0.023,0.01,
#           r'$\varphi_l=0.2$')
#ax[0].text(0.013,0.01,
#           r'$\varphi_l=0.1$')
#ax[0].text(0.002,0.08,
#           r'$\varphi_l=0.05$')
#ax[0].text(0.002,0.05,
#           r'$\varphi_l=0$')

ax[0].annotate(
        r'$\varphi_l\!=\!0.3$',
        xy = (0.034, 0.05),
        xytext= (0.033, 0.01),
        arrowprops=dict(arrowstyle="-",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax[0].annotate(
        r'$\varphi_l\!=\!0.2$',
        xy = (0.025, 0.05),
        xytext= (0.023, 0.01),
        arrowprops=dict(arrowstyle="-",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax[0].annotate(
        r'$\varphi_l\!=\!0.1$',
        xy = (0.017, 0.05),
        xytext= (0.013, 0.01),
        arrowprops=dict(arrowstyle="-",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax[0].annotate(
        r'$\varphi_l\!=\!0.05$',
        xy = (0.013, 0.05),
        xytext= (0.001, 0.08),
        arrowprops=dict(arrowstyle="-",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax[0].annotate(
        r'$\varphi_l\!=\!0$',
        xy = (0.005, 0.025),
        xytext= (0.001, 0.05),
        arrowprops=dict(arrowstyle="-",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )

# beta
ax[1].plot([Zp,2*Zp],[Zp*beta,0],
           'k:',linewidth=1)
ax[1].text(0.1,0.1,
           r'$-\beta$'
           )
# Zst
ax[1].plot([Zst,Zst],[0,Zp*beta],
           'k-.',linewidth=1)
ax[1].text(0.057,0.1,
           '$Z_{st}$'
           )

# labels
#ax[1].text(0.0685,0.013,
#           r'$\varphi_r=1.3$')
#ax[1].text(0.088,0.013,
#           r'$\varphi_r=1.7$')
#ax[1].text(0.118,0.013,
#           r'$\varphi_r=2.3$')
ax[1].text(0.13,0.075,
           r'$\varphi_r=3.2$')
ax[1].text(0.13,0.165,
           r'$\varphi_r=4.8$')
ax[1].text(0.13,0.25,
           r'$\varphi_r=\mathrm{inf}$')

ax[1].annotate(
        r'$\varphi_r\!=\!1.3$',
        xy = (0.068, 0.06),
        xytext= (0.0685, 0.013),
        arrowprops=dict(arrowstyle="-",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax[1].annotate(
        r'$\varphi_r\!=\!1.7$',
        xy = (0.0835, 0.06),
        xytext= (0.088, 0.013),
        arrowprops=dict(arrowstyle="-",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax[1].annotate(
        r'$\varphi_r\!=\!2.3$',
        xy = (0.1055, 0.06),
        xytext= (0.118, 0.013),
        arrowprops=dict(arrowstyle="-",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )

ax[0].set_xlim(0.0,0.058)
ax[0].set_xlabel('$Z$')
ax[1].set_xlim(0.05,0.15)
ax[1].set_xlabel('$Z$')

ax[0].set_ylim(0.0,0.275)
ax[0].set_ylabel('$c$')

ax[1].tick_params(axis='y',length=0)

ax[0].text(
        0.002,0.15,
        ''.join([r'$\mathrm{CH}_4/\mathrm{Air}$',
                 '\n',
                 '$a\;\:=\;$',
                 '{:g}'.format(a),
                 r'$\;\mathrm{s}^{-1}$',
                 '\n',
                 r'$p\;\;=1\;\mathrm{atm}$',
                 '\n',
                 r'$T_r=300\;\mathrm{K}$',
                 '\n',
                 r'$T_l\,=300\;\mathrm{K}$'
                 ]),
        linespacing=1.5
        )

ax[0].text(0.027,0.26,'(a)',fontweight='bold')
ax[1].text(0.1,0.26,'(b)',fontweight='bold')

cax = fig.add_axes([(plot_width-margin_right+0.2)/plot_width,
                    margin_bottom/plot_height,
                    0.2/plot_width,
                    subplot_height/plot_height])
clb = fig.colorbar(cplt,cax=cax)
cax.set_ylabel(
        r'$\mathrm{sign}(\mathrm{Re}(\Lambda_e))\times$'
        +r'$\lg(1+\left\vert\mathrm{Re}(\Lambda_e)\right\vert)$')
#clb.set_ticks([0.05,0.15,0.25])
cax.tick_params(labelsize='small')
#cax.xaxis.set_ticks_position('top')
#cbar = figs[i].colorbar(cplt)

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/plot_width,
        hspace = space_height/plot_height
        )

fig.savefig('{0}/phi_a{1:g}.pdf'.format(dst,a))
fig.savefig('{0}/phi_a{1:g}.eps'.format(dst,a))
plt.close('all')
