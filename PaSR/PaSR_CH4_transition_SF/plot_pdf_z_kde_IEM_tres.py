
# coding: utf-8

# # plot pdf of z with different $\tau_{res}$ and fixed $\tau_{mix}/\tau_{res}$

# In[1]:


import os
import math
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from counterflow_file import *


# In[2]:


# parameters
models = ['IEM','IEMHYB']
modeln = ['IEM','IEM-FI']

# In[3]:

tau_log = [-2.5,-3,-3.5]

z_lb = 0
z_ub = 0.156


# In[6]:


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

colors = ['tab:blue','tab:green','tab:red']
lines = ['--','-','-.']

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.8

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)


# In[10]:


# plot against tmix
fig, ax = plt.subplots(num_rows,num_cols,
                       figsize=cm2inch(plot_width,plot_height))

for i, t in enumerate(tau_log):
    for j, m in enumerate(models):

        file_name = 'pdfs_z_tres-{}.csv'.format(t)

        data = np.genfromtxt(file_name, names=True, delimiter=',')

        t_exp_index = math.ceil(-t)

        ax[j].plot(data['x'], data[m],
                   c = colors[i], ls = lines[i], lw = 1.,
                   label=''.join([
                       r'$\tau_{\mathrm{res}}=$',
                       '{:.1f}'.format(np.power(10.,t)*np.power(10.,t_exp_index)),
                       r'$\times 10^{',
                       '{:g}'.format(-t_exp_index),
                       r'}$',
                       r'$\;\mathrm{s}$'])
                  )

        
for j, m in enumerate(modeln):
    ax[j].text(0.01,8/9*80,'({})'.format(chr(ord('a')+j)))
    # legend
    ax[j].legend(frameon=False,loc='upper right')

    # limits
    ax[j].set_xlim([z_lb, z_ub])
    ax[j].set_xticks(np.linspace(0,0.15,6))
    ax[j].set_ylim([0, 80])
    ax[j].set_yticks(np.linspace(0,80,9))

    # labels
    ax[j].set_xlabel(r'$Z$')
    ax[j].set_ylabel(r'$\langle\tilde{f}_Z\rangle$')

    ax[j].text(0.005,45,
               ''.join([
                   m,
                   '\n',
                   r'$\dfrac{\tau_{\mathrm{mix}}}{\tau_{\mathrm{res}}}=0.2$'])
              )

fig.subplots_adjust(left = margin_left/plot_width,
                    bottom = margin_bottom/plot_height,
                    right = 1.0-margin_right/plot_width,
                    top = 1.0-margin_top/plot_height,
                    wspace = space_width/plot_width,
                    hspace = space_height/plot_height
                    )

for j, m in enumerate(models):
    sub_ax_left = (
            j*(space_width/subplot_width*0.7+1)
            +0.62
            )*subplot_width+margin_left
    sub_ax_bottom = 0.15*subplot_height+margin_bottom

    axs = fig.add_axes([sub_ax_left/plot_width,
                        sub_ax_bottom/plot_height,
                        0.57*subplot_width/plot_width,
                        0.42*subplot_height/plot_height])
    for i, t in enumerate(tau_log):
        file_name = 'pdfs_z_tres-{}.csv'.format(t)

        data = np.genfromtxt(file_name, names=True, delimiter=',')

        axs.plot(data['x'],data[m],
                 c = colors[i], ls = lines[i], lw = 1.)

        axs.set_xlim([0.049,0.058])
        axs.set_ylim([0, 80])
        axs.set_yticks([0,40,80])

fig.savefig('fig_pdf_z_IEMHYB_tres.pdf')

