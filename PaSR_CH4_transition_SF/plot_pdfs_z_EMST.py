
# coding: utf-8

# # plot pdf of Z, obtained with np.hist

# In[1]:


import copy
import numpy as np
import matplotlib.pyplot as plt
from counterflow_file import *


# In[3]:


# parameters
models = ['EMST','EMSTHYB']
modeln = ['EMST','EMST-FI']
params = {}
params['MIX'] = None
params['tres'] = -3.65
params['tmix'] = 0.2
params['eqv'] = 1.0

csv_name = 'ZCTR.csv'

npts = 100
z_lb = 0
z_ub = 0.156


# In[4]:


pdfs_r = np.empty([npts, len(models)])
pdfs_u = np.empty([npts, len(models)])
for i, model in enumerate(models):
    params['MIX'] = model
    case_name = params2name(params)
    
    data = np.genfromtxt('/'.join([case_name,csv_name]),
                         delimiter=',',
                         names=True)
    
    hist, bins = np.histogram(data['Z'], 
                              bins=npts, 
                              range=(z_lb, z_ub), 
                              weights=data['R'], 
                              density=True
                             )
    
    pdfs_r[:,i] = hist

    hist, bins = np.histogram(data['Z'], 
                              bins=npts, 
                              range=(z_lb, z_ub), 
                              density=True
                             )
    
    pdfs_u[:,i] = hist


# In[5]:


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
# use serif font
plt.rc('font',**font)

num_cols = 2
num_rows = 1

colors = ['tab:blue','tab:red']
lines = ['--','-']

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.9

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)


# In[6]:


z = (bins[1:]+bins[:-1])/2

# plot against tmix
fig, ax = plt.subplots(num_rows,num_cols,sharex=True,
                       figsize=cm2inch(plot_width,plot_height))

for i, model in enumerate(models):
    ax[0].plot(z, pdfs_r[:,i],
            c = colors[i], ls = lines[i], lw = 1.,
            label=modeln[i])
    ax[1].plot(z, pdfs_u[:,i],
            c = colors[i], ls = lines[i], lw = 1.,
            label=modeln[i])
    
# legend
ax[0].legend(frameon=False)
ax[1].legend(frameon=False)

# limits
ax[0].set_xlim([z_lb, z_ub])
ax[0].set_xticks(np.linspace(0,0.15,6))
ax[0].set_ylim([0, 130])
ax[1].set_ylim([0, 220])

# labels
ax[0].set_xlabel(r'$Z$')
ax[1].set_xlabel(r'$Z$')
ax[0].set_ylabel(r'$\langle\tilde{f}_Z\rangle$')
ax[1].set_ylabel(r'$\langle f_Z \rangle$')

# notes
ax[0].text(0.01,114.4,'(a)')
ax[1].text(0.01,193.6,'(b)')

ax[0].text(
        0.09,65,
        ''.join([
            r'$\tau_{\mathrm{res}}\,=\,$',
            '{:.3g}'.format(np.power(10.,params['tres'])*1000),
            '$\;\mathrm{ms}$',
            '\n',
            r'$\tau_{\mathrm{mix}}\!=\,$',
            '{:.3g}'.format(np.power(10.,params['tres'])*params['tmix']*1000),
            '$\;\mathrm{ms}$']))
ax[1].text(
        0.09,110,
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

# In[7]:


fig.savefig('fig_pdfs_z_EMST.pdf')
fig.savefig('fig_pdfs_z_EMST.eps')

