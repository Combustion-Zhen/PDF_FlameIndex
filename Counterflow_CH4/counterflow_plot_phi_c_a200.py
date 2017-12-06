"""
Zhen Lu 2017/11/29

plot c Z of counterflow flames with different extent of premixing
"""
import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

phif = [1.3, 1.7, 2.3, 3.2, 4.8, float('inf')]
phio = [0, 0.1, 0.2, 0.3]

#strain = [100, 150, 200, 250, 300]
a = 200

dst = 'figs_phi'

Zst = 0.0551863
Zp = 0.06
beta = 5
Zsp = 0.12

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
plot_width    = 6.7
margin_left   = 0.7
margin_right  = 0.2
margin_bottom = 0.5
margin_top    = 0.1
space_width   = 0.
space_height  = 1.0
ftsize        = 6

subplot_w = plot_width - margin_left - margin_right
subplot_h = subplot_w/1.618

plot_height = subplot_h + margin_top + margin_bottom

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

plt.rc('font',**font)

flame_params['a'] = a

fig = plt.figure(figsize=cm2inch(plot_width,plot_height),frameon=True)

rect = (margin_left/plot_width,
        margin_bottom/plot_height,
        0.8*subplot_w/plot_width,
        subplot_h/plot_height)
ax0 = fig.add_axes(rect)
rect = ((margin_left+0.8*subplot_w)/plot_width,
        margin_bottom/plot_height,
        0.2*subplot_w/plot_width,
        subplot_h/plot_height)
ax1 = fig.add_axes(rect)

# get data
folder_params['phif'] = float('inf')
flame_params['phif'] = float('inf')
for phi in phio:
    folder_params['phio'] = phi
    flame_params['phio'] = phi

    folder = params2name(folder_params)
    flame = params2name(flame_params)

    file_name = '{}/{}.dat'.format(folder,flame)

    if not os.path.exists(file_name):
        continue
    data = np.genfromtxt(file_name,skip_header=3,names=True)

    ax0.plot(data['Z1'],data['C_4spe'],lw=1)
    ax1.plot(data['Z1'],data['C_4spe'],lw=1)

folder_params['phio'] = 0
flame_params['phio'] = 0
for phi in phif:
    folder_params['phif'] = phi
    flame_params['phif'] = phi

    folder = params2name(folder_params)
    flame = params2name(flame_params)

    label = r'$\varphi_r=$'+'{0:g}'.format(phi)

    file_name = '{}/{}.dat'.format(folder,flame)

    if not os.path.exists(file_name):
        continue
    data = np.genfromtxt(file_name,skip_header=3,names=True)

    ax0.plot(data['Z1'],data['C_4spe'],lw=1)
    ax1.plot(data['Z1'],data['C_4spe'],lw=1)

#ax0.plot([Zst,Zst],[0,1],'k-.',lw=1)
ax0.text(0.056,-0.03,
           r'$Z_{st}$')
ax0.annotate(
    '',xy=(0.055,0.005),xytext=(0.055,-0.03),
    arrowprops=dict(arrowstyle="-",color="k",lw=0.5,ls='--')
    )
ax0.plot([0,Zst,1],[0,Zst*5,0],'k:',lw=1)
ax1.plot([0,Zst,1],[0,Zst*5,0],'k:',lw=1)
ax1.plot([Zsp,Zsp],[0,1],'k--',lw=1)
# scale split for two axis
ax0.set_xlim(0,Zsp)
ax1.set_xlim(Zsp,1)
ax0.set_ylim(0,0.3)
ax1.set_ylim(0,0.3)
ax0.set_xticks([0,0.025,0.05,0.075,0.1])
ax0.set_xticklabels(['0','0.025','0.5','0.075','0.1'])
ax0.set_yticks([0,0.1,0.2,0.3])
ax1.set_yticks([])
ax0.tick_params(length=2,pad=1)
ax1.tick_params(length=2,pad=1)
ax0.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)

ax0.set_ylabel('$c$',labelpad=2)
ax0.set_xlabel('$Z$',labelpad=2)
ax0.xaxis.set_label_coords(0.6,-0.09)

## text
#
ax0.annotate(
        r'$(0.3,\infty)$',
        xy = (0.031, 0.025),
        xytext= (0.04, 0.02),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax0.annotate(
        r'$(0.2,\infty)$',
        xy = (0.023, 0.054),
        xytext= (0.04, 0.049),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax0.annotate(
        r'$(0.1,\infty)$',
        xy = (0.017, 0.05),
        xytext= (0.002, 0.14),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
#ax0.annotate(
#        r'$\varphi_l 0$',
#        xy = (0.005, 0.025),
#        xytext= (0.001, 0.07),
#        arrowprops=dict(arrowstyle="-",
#                        connectionstyle="arc3",
#                        linewidth=0.5),
#        )

ax0.annotate(
        ''.join([
            r'$(\varphi_l,\varphi_r)$',
            '\n',
            r'$=(0,\infty)$'
            ]),
        xy = (0.06,0.25),
        xytext = (0.041,0.15),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )

ax0.annotate(
        r'$(0,1.3)$',
        xy = (0.069, 0.085),
        xytext= (0.04, 0.08),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )
ax0.annotate(
        r'$(0,1.7)$',
        xy = (0.083, 0.06),
        xytext= (0.087, 0.013),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )

ax0.text(0.1,0.147,
           r'$(0,3.2)$')
ax0.text(0.1,0.22,
           r'$(0,4.8)$')

ax0.annotate(
        r'$(0,2.3)$',
        xy = (0.108, 0.03),
        xytext= (0.1, 0.09),
        arrowprops=dict(arrowstyle="->",
                        connectionstyle="arc3",
                        linewidth=0.5),
        )

ax0.text(
        0.002,0.2,
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
                 ])
        )

ax0.text(0.122,0.265,
           'scale\n split')

fig.savefig('{0}/phi_a{1:g}_c.pdf'.format(dst,a))
fig.savefig('{0}/phi_a{1:g}_c.eps'.format(dst,a))
plt.close('all')
