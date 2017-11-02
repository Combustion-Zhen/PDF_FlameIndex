"""
Zhen Lu 2017/10/29
"""

import numpy as np
import matplotlib.pyplot as plt
from counterflow_file import *

SMALL = 1.e-7
models = ['IEM-FI','MC-FI','EMST-FI']

# parameters
flame_params = {}
flame_params['F'] = 'CH4'
flame_params['p'] = 1.
flame_params['a'] = 424.742
flame_params['phif'] = 1.7
flame_params['phio'] = 0.
flame_params['tf'] = 300.
flame_params['to'] = 300.
flame_params['eqv'] = 1.2
flame_params['var'] = 0.05

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
    print(file_name)
    p = np.genfromtxt(file_name)

    print(p.shape)
    # too many points, sample randomly
    npts = p.shape[0]
    if npts > 2000:
        pre=np.random.randint(0,npts,size=1000)
        axes[i].scatter(p[pre,0],p[pre,2],c=p[pre,1])
    else:
        axes[i].scatter(p[:,0],p[:,2],c=p[:,1])


plt.show()
