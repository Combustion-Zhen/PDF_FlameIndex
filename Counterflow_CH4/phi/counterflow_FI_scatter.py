"""
Zhen Lu 2017/10/29
"""

import numpy as np
import matplotlib.pyplot as plt
from counterflow_file import *

SMALL = 1.e-20
models = ['IEM','MC','EMST']

# parameters
flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1.
flame_params['a'] = 100.
flame_params['phif'] = 1.3
flame_params['phio'] = 0.
flame_params['tf'] = 300.
flame_params['to'] = 300.
flame_params['var'] = 0.5

case_name = params2name(flame_params)

# plot
# use TeX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
plot_width    = 19.0
subplot_h     = 4.0
margin_left   = 1.8
margin_right  = 0.5
margin_bottom = 1.2
margin_top    = 1.0
space_width   = 2.4
space_height  = 1.5
ftsize        = 12
plot_height   = subplot_h+margin_bottom+margin_top

fig, axes = plt.subplots(1,3,sharex='all',sharey='row',
        figsize=cm2inch(plot_width,plot_height))

for i, model in enumerate(models):
    file_name = '{0}.{1}'.format(case_name,model)
    particles = np.genfromtxt(file_name)

    Z = []
    C = []
    I = []
    for p in particles:
        if abs(p[-1])>SMALL or abs(p[-2])>SMALL:
            Z.append(p[0])
            C.append(p[1])
            I.append(p[2])

    axes[i].scatter(Z,C,c=I)

plt.show()
