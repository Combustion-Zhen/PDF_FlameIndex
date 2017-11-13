"""
Zhen Lu 2017/11/12

plot the ensemble average of flame index
"""

import os
import copy
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from counterflow_file import *

models = np.array([['IEM','MC','EMST'],
                   ['IEMHYB','MCHYB','EMSTHYB']])

time_res = [1.e-2,]
mix_res_ratio = [0.02, 0.05, 0.1, 0.2, 0.5]
equiv_ratio_f = [4.76,]
#equiv_ratio = [1.0, 1.2, 1.4]
equiv_ratio = [1.2,]
Zf_variance = [0.01, 0.02, 0.05, 0.1, 0.15]
dtmix = [0.01,]

params = {}
params['MIX'] = None
params['tres'] = None
params['tmix'] = None
params['eqv'] = None
params['Zfvar'] = None
params['dtmix'] = None
params['phif'] = None

dst = 'figs_FI_ave_all'
dat_name = 'pasrm.op'

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 19.0
margin_left   = 1.2
margin_right  = 0.1
margin_bottom = 1.0
margin_top    = 0.8
space_width   = 0.
space_height  = 0.
ftsize        = 10

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = 3
num_rows = 2

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.3

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

# loop over all parameters
for tres in time_res:
    params['tres'] = tres
    for tmix_ratio in mix_res_ratio:
        tmix = tmix_ratio*tres
        params['tmix'] = tmix_ratio
        for dt in dtmix:
            params['dtmix'] = dt
            for phif in equiv_ratio_f:
                params['phif'] = phif

                # plot against variance

                fig, ax = plt.subplots(
                        num_rows, num_cols,
                        sharex = True, sharey = True,
                        figsize=cm2inch(plot_width,plot_height))

                for i in range(num_rows):
                    for j in range(num_cols):
                        model = models[i,j]
                        params['MIX'] = model

                        ax[i,j].plot([0,0.2],[0.5,0.5],'--',linewidth=0.5)

                        for phi in equiv_ratio:
                            params['eqv'] = phi

                            data = np.zeros((len(Zf_variance),3))

                            for k, var in enumerate(Zf_variance):
                                params['Zfvar'] = var

                                case = params2name(params)
                                file_name = '/'.join([model,case,dat_name])

                                if os.path.exists(file_name):
                                    FI = np.genfromtxt(file_name,usecols=(3,))
                                else:
                                    print(file_name)
                                    continue

                                FI_ave = np.mean(FI)
                                FI_rms = np.std(FI)

                                data[k,0] = var
                                data[k,1] = FI_ave
                                data[k,2] = FI_rms


                            #flag = data[:,1] > 0.05
                            #ax[i,j].plot(data[flag,0],data[flag,1],label='{:g}'.format(phi))
                            ax[i,j].plot(data[:,0],data[:,1],label='{:g}'.format(phi))
                            ax[i,j].fill_between(data[:,0],data[:,1]+data[:,2],data[:,1]-data[:,2])
                        ax[i,j].legend(frameon=False)

                plot_params = copy.deepcopy(params)
                del plot_params['MIX']
                del plot_params['tres']
                del plot_params['dtmix']
                del plot_params['phif']
                del plot_params['Zfvar']
                del plot_params['eqv']
                plot_name = params2name(plot_params)

                fig.savefig('{}/{}.eps'.format(dst,plot_name))

                plt.close('all')
