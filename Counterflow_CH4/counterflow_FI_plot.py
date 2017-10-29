"""
Zhen Lu 2017/10/29 <albert.lz07@gmail.com>
"""

import glob
import numpy as np
import matplotlib.pyplot as plt
from counterflow_file import *

SMALL  = 1.e-20
idx_I  = 2
models = ['IEM','MC','EMST']

# plot
# use TeX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
plot_width    = 9.0 / 2.54
plot_height   = 9.0 / 2.54
margin_left   = 1.8 / 2.54
margin_right  = 0.3 / 2.54
margin_bottom = 1.2 / 2.54
margin_top    = 1.0 / 2.54
space_width   = 2.4 / 2.54
space_height  = 1.5 / 2.54
ftsize        = 12

#str_legend = r'$\tilde{Z^{\prime\prime 2}}/($'+r'$\tilde{Z}(1-$'+r'$\tilde{Z}))=$'
#str_legend = r'$\tilde{Z^{\prime\prime 2}}/(\tilde{Z}(1-\tilde{Z}))=$'

for i, model in enumerate(models):

    fig = plt.figure(i,figsize=(plot_width,plot_height))
    ax  = fig.add_subplot(1,1,1)

    # file list
    extension = '.{}'.format(model)
    param_list = paramlist(extension)
    print(param_list)

    data = np.zeros((len(param_list['a']),2))

    for var in param_list['var']:
        for j, strain in enumerate(param_list['a']):
            flame = {}
            for k, v in param_list.items():
                flame[k] = v[0]
            flame['var'] = var
            flame['a'] = strain
            flame_name = params2name(flame)

            file_name = '{0}{1}'.format(flame_name,extension)
            try:
                particles = np.genfromtxt(file_name)
            except OSError:
                continue

            I = []
            for p in particles:
                if abs(p[-1])>SMALL or abs(p[-2])>SMALL:
                    I.append(p[idx_I])
            I_ave = np.average(np.array(I))

            data[j,0] = strain
            data[j,1] = I_ave

        # plot for each mean and var
        label = r'$\eta_Z$='+'{0:g}'.format(var)
        ax.plot(data[data[:,0]>0,0],data[data[:,0]>0,1],label=label,linewidth=1)

    ax.set_ylabel(r'$\tilde\mathrm{FI}$',fontsize=ftsize)
    ax.set_ylim(0.0,1.0)
    ax.set_xlabel(r'$a\;\mathrm{(1/s)}$',fontsize=ftsize)
#    ax.set_xscale('log')
    ax.set_title(model,fontsize=ftsize)
    ax.legend(fontsize=ftsize,frameon=False)

    fig.subplots_adjust(left   = margin_left   / plot_width,
                        bottom = margin_bottom / plot_height,
                        right  = 1.0 - margin_right / plot_width,
                        top    = 1.0 - margin_top   / plot_height,
                        wspace = space_width   / plot_width,
                        hspace = space_height  / plot_height)

#    fig.savefig('chi_{0}.png'.format(model),dpi=400)
#    fig.savefig('chi_{0}.eps'.format(model))
    fig.savefig('chi_{0}.pdf'.format(model))
