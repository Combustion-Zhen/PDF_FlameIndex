"""
Zhen Lu 2017/11/13

plot conditional omega
"""

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

model = 'IEMHYB'

tres = 0.01
mix_res_ratio = [0.02, 0.05, 0.1, 0.2, 0.5]
phif = 4.76
phi = [1.0, 1.2, 1.4]
Zf_variance = [0.01, 0.02, 0.05, 0.1, 0.15]
dtmix = 0.01

params = {}
params['MIX'] = None
params['tres'] = None
params['tmix'] = None
params['eqv'] = None
params['Zfvar'] = None
params['dtmix'] = None
params['phif'] = None

dst = 'figs_FI_ave'
dat_name = 'pasrm.op'

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 6.7
margin_left   = 1.0
margin_right  = 0.25
margin_bottom = 0.85
margin_top    = 0.1
space_width   = 0.
space_height  = 0.
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

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.8

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)


