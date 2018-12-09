import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from counterflow_file import *

# parameters
models = ['EMST','EMSTHYB']
modeln = ['EMST','EMST-FI']
params = {}
params['MIX'] = None
params['tres'] = -3.65
params['tmix'] = 0.2
params['eqv'] = 1.0

op_name = 'particle_info.op'

# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
margin_left   = 1.4
margin_right  = 0.1
margin_bottom = 1.0
margin_top    = 0.1
space_width   = 3.5
space_height  = 0.5
ftsize        = 9

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
plt.rc('text.latex', preamble=[r'\usepackage{amsmath}',r'\usepackage{bm}'])
# use serif font
plt.rc('font',**font)

num_cols = 2
num_rows = 1

colors = ['tab:orange','tab:blue','tab:green','tab:red']

mft = ['o','s']
mfc = ['w',None]

dst = '.'

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.8

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

# plot against tmix
fig, ax = plt.subplots(num_rows,num_cols,sharex=True,
                       figsize=cm2inch(plot_width,plot_height))

for i, model in enumerate(models):
    params['MIX'] = model
    case_name = params2name( params )
    file_name = '/'.join([case_name,op_name])

    os.chdir( case_name )
    subprocess.run('particles_post')
    os.chdir( '..' )

    data = np.genfromtxt( file_name )
    ax[i].scatter( data[:,0], data[:,1], s=4, marker='.' )

    ax[i].text(0.01,0.24,'({})'.format(chr(ord('a')+i)))
    ax[i].text(0.1,0.24,modeln[i])

ax[0].set_xlim([0, 0.156])
ax[0].set_xticks(np.linspace(0,0.15,6))
ax[0].set_ylim([0, 0.27])
ax[0].set_yticks(np.linspace(0, 0.25, 6))
ax[1].set_ylim([0, 0.27])
ax[1].set_yticks(np.linspace(0, 0.25, 6))

# labels
ax[0].set_xlabel(r'$Z$')
ax[1].set_xlabel(r'$Z$')
ax[0].set_ylabel(r'$c$')
ax[1].set_ylabel(r'$c$')

# notes
ax[0].text(
        0.09,0.15,
        ''.join([
            r'$\tau_{\mathrm{res}}\,=\,$',
            '{:.3g}'.format(np.power(10.,params['tres'])*1000),
            '$\;\mathrm{ms}$',
            '\n',
            r'$\tau_{\mathrm{mix}}\!=\,$',
            '{:.3g}'.format(np.power(10.,params['tres'])*params['tmix']*1000),
            '$\;\mathrm{ms}$']))
ax[1].text(
        0.09,0.15,
        ''.join([
            r'$\tau_{\mathrm{res}}\,=\,$',
            '{:.3g}'.format(np.power(10.,params['tres'])*1000),
            '$\;\mathrm{ms}$',
            '\n',
            r'$\tau_{\mathrm{mix}}\!=\,$',
            '{:.3g}'.format(np.power(10.,params['tres'])*params['tmix']*1000),
            '$\;\mathrm{ms}$']))

fig.subplots_adjust(left = margin_left/plot_width,
                    bottom = margin_bottom/plot_height,
                    right = 1.0-margin_right/plot_width,
                    top = 1.0-margin_top/plot_height,
                    wspace = space_width/plot_width,
                    hspace = space_height/plot_height
                    )

fig.savefig('fig_scatter_EMST.pdf')
fig.savefig('fig_scatter_EMST.eps')
