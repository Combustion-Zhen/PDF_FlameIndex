
# coding: utf-8

# # plot pdf of Z, obtained with np.hist

# In[1]:


import copy
import numpy as np
import matplotlib.pyplot as plt
from counterflow_file import *


# In[3]:


# parameters
models = ['IEM','IEMHYB']
modeln = ['IEM','IEM-FI']
params = {}
params['MIX'] = None
params['tres'] = -3
params['tmix'] = 0.2
params['eqv'] = 1.0

csv_name = 'ZCTR.csv'

npts = 100
z_lb = 0
z_ub = 0.156


# In[4]:


pdfs = np.empty([npts, len(models)])
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
    
    pdfs[:,i] = hist


# In[5]:


# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 6.7
margin_left   = 1.3
margin_right  = 0.2
margin_bottom = 1.0
margin_top    = 0.1
space_width   = 3.5
space_height  = 0.5
ftsize        = 7

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = 1
num_rows = 1

colors = ['tab:blue','tab:red']
lines = ['--','-']

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.8

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
    ax.plot(z, pdfs[:,i],
            c = colors[i], ls = lines[i], lw = 1.,
            label=modeln[i])
    
# legend
ax.legend(frameon=False)

# limits
ax.set_xlim([z_lb, z_ub])
ax.set_ylim([0, 68])

# labels
ax.set_xlabel(r'$Z$')
ax.set_ylabel(r'$\langle\tilde{f}_Z\rangle$')

# notes
ax.text(
        0.1,30,
        ''.join([
            r'$\tau_{\mathrm{res}}\,=\,$',
            '{:g}'.format(np.power(10.,params['tres'])*1000),
            '$\;\mathrm{ms}$',
            '\n',
            r'$\tau_{\mathrm{mix}}\!=\,$',
            '{:g}'.format(np.power(10.,params['tres'])*params['tmix']*1000),
            '$\;\mathrm{ms}$']))

fig.subplots_adjust(left = margin_left/plot_width,
                    bottom = margin_bottom/plot_height,
                    right = 1.0-margin_right/plot_width,
                    top = 1.0-margin_top/plot_height,
                    wspace = space_width/plot_width,
                    hspace = space_height/plot_height
                    )

# In[7]:


fig.savefig('fig_pdf_z_IEM.pdf')

