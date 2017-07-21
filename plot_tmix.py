"""
Zhen Lu 2017/07/16 <albert.lz07@gmail.com>

plot PaSR results with three mixing models

On averaged FI with respect to the equivalence ratio
"""

import glob
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import os
from subprocess import call

SMALL = 1.e-20

idx_Z = 0
idx_C = 1
idx_I = 3
idx_T = 4

# model names
models = ['IEM','MC','EMST']
lines = ['-','--','-.']

case_pre = 'H2_NON_phi1_tres4e-3_tmix'

# plot
# use TeX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
plot_width    = 9.0 / 2.54
plot_height   = 8.0 / 2.54
margin_left   = 1.8 / 2.54
margin_right  = 0.3 / 2.54
margin_bottom = 1.2 / 2.54
margin_top    = 0.3 / 2.54
space_width   = 2.4 / 2.54
space_height  = 1.5 / 2.54
ftsize        = 12

fig, axes = plt.subplots(1,1,
        figsize=(plot_width,plot_height))

for j, model in enumerate(models):
    data=np.zeros((len(glob.glob('{0}*_{1}'.
        format(case_pre,model))),2))
    i = 0
    t_ext = []
    for folder in glob.glob('{0}*_{1}'.format(
        case_pre,model)):

        tmix = float(folder[len(case_pre):folder.find(model)-1])

        os.chdir(folder)
        call(["PaSR_particles_post"])
        os.chdir('..')

        particles = np.genfromtxt('{0}/particle_post.dat'.format(folder))

        I = []
        for p in particles:
            if abs(p[-1])>SMALL or abs(p[-2])>SMALL:
                I.append(p[idx_I])
        I_ave = np.average(np.array(I))
        data[i,0] = tmix
        data[i,1] = I_ave
        if tmix > 1.e-3 :
            t_ext.append(i)
        i = i + 1
    if model != 'EMST':
        data=np.delete(data,t_ext,0)
    # sort the data
    data = data[np.argsort(data[:,0])]

    axes.plot(data[:,0],data[:,1],lines[j],label=model,linewidth=1.5)

axes.set_ylabel(r'$\langle\mathrm{FI}\rangle$',fontsize=ftsize)
#axes.set_ylim(0.15,0.7)
axes.set_xlabel(r'$\tau_{mix}\;\left(\mathrm{s}\right)$',fontsize=ftsize)
#axes.set_xlim(1.e-4,1.e-2)
axes.set_xscale('log')

# legend
axes.legend(fontsize=ftsize,frameon=False)

plt.subplots_adjust(left   = margin_left   / plot_width,
                    bottom = margin_bottom / plot_height,
                    right  = 1.0 - margin_right / plot_width,
                    top    = 1.0 - margin_top   / plot_height,
                    wspace = space_width   / plot_width,
                    hspace = space_height  / plot_height)

plt.show()

plt.savefig('nonpremix_tmix.png',dpi=400)
plt.savefig('nonpremix_tmix.eps')
plt.savefig('nonpremix_tmix.pdf')
