"""
Zhen Lu 2017/07/16 <albert.lz07@gmail.com>

plot PaSR results with three mixing models

two rows, three columes
"""

import numpy as np
import matplotlib.pyplot as plt

SMALL = 1.e-20

idx_Z = 0
idx_C = 1
idx_I = 3
idx_T = 4

# model names
models = ['IEM','MC','EMST']

case_pre = 'H2_NON_phi1_tres4e-3_tmix7e-4_'

# plot
# use TeX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
plot_width    = 19.0 / 2.54
subplot_h     = 4.0  / 2.54
margin_left   = 1.8  / 2.54
margin_right  = 0.5  / 2.54
margin_bottom = 1.2  / 2.54
margin_top    = 1.0  / 2.54
space_width   = 2.4  / 2.54
space_height  = 1.5  / 2.54
ftsize        = 12
plot_height   = subplot_h*2+space_height+margin_bottom+margin_top

fig, axes = plt.subplots(2,3,sharex='all',sharey='row',
        figsize=(plot_width,plot_height))

for i, model in enumerate(models):
    particles = np.genfromtxt('{0}{1}/particle_post.dat'.format(
        case_pre,model))
    Z = []
    I = []
    for p in particles:
        if abs(p[-1])>SMALL or abs(p[-2])>SMALL:
            Z.append(p[idx_Z])
            I.append(p[idx_I])
    I_ave = np.average(np.array(I))
    # plot the temperature scatter
    axes[0,i].scatter(particles[:,idx_Z],particles[:,idx_T],
            marker='.',c='k',edgecolor='none')
    axes[1,i].scatter(Z,I,
            marker='.',c='k',edgecolor='none')

    axes[1,i].text(0.6,0.85,
            r'$\langle\mathrm{FI}\rangle$='+'{0:.2g}'.format(I_ave),
            fontsize=ftsize)
    axes[1,i].set_xlabel('$Z$',fontsize=ftsize)
    axes[0,i].set_title(model,fontsize=ftsize)

axes[0,0].set_ylim(250,2100)
axes[0,0].set_ylabel(r'$T\;\left(\mathrm{K}\right)$',fontsize=ftsize)
axes[1,0].set_ylim(0.0,1.0)
axes[1,0].set_ylabel(r'$\mathrm{FI}$',fontsize=ftsize)

axes[1,0].set_xlim(0.0,1.0)

plt.subplots_adjust(left   = margin_left   / plot_width,
                    bottom = margin_bottom / plot_height,
                    right  = 1.0 - margin_right / plot_width,
                    top    = 1.0 - margin_top   / plot_height,
                    wspace = space_width   / plot_width,
                    hspace = space_height  / plot_height)

plt.show()

plt.savefig('nonpremix_scatter.png',dpi=400)
plt.savefig('nonpremix_scatter.eps')
plt.savefig('nonpremix_scatter.pdf')
