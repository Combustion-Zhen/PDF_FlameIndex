"""
Zhen Lu 2017/11/13

plot ave and confidence region of FI
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
colors = np.array([
        ['tab:purple','tab:orange','tab:brown'],
        ['tab:blue','tab:red','tab:green']])

mft = ['o','^','s']
mfc = ['w',None]

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

dst = 'figs_FI_ave'
dat_name = 'pasrm.op'

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 6.7
margin_left   = 1.03
margin_right  = 0.22
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

# loop over all parameters
for tres in time_res:
    params['tres'] = tres
    for var in Zf_variance:
        params['Zfvar'] = var
        for dt in dtmix:
            params['dtmix'] = dt
            for phif in equiv_ratio_f:
                params['phif'] = phif

                # plot against tmix

                fig, ax = plt.subplots(
                        figsize=cm2inch(plot_width,plot_height))

                ax.plot([0,1],[0.5,0.5],'k--',linewidth=1)

                for i in range(2):
                    for j in range(3):
                        model = models[i,j]
                        params['MIX'] = model


                        for phi in equiv_ratio:
                            params['eqv'] = phi

                            data = np.zeros((len(mix_res_ratio),3))

                            for k, tmix_ratio in enumerate(mix_res_ratio):
                                tmix = tmix_ratio*tres
                                params['tmix'] = tmix_ratio

                                case = params2name(params)
                                file_name = '/'.join([model,case,dat_name])

                                if os.path.exists(file_name):
                                    FI = np.genfromtxt(file_name,usecols=(3,))
                                else:
                                    print(file_name)
                                    continue

                                FI_ave = np.mean(FI)
                                FI_rms = np.std(FI)

                                data[k,0] = tmix_ratio
                                data[k,1] = FI_ave
                                data[k,2] = FI_rms

                            flag = data[:,1] > 0.05
                            #ax[i,j].plot(data[flag,0],data[flag,1],label='{:g}'.format(phi))
                            ax.errorbar(
                                    data[flag,0],
                                    data[flag,1],
                                    yerr=3*data[flag,2],
                                    c=colors[i,j],
                                    fmt=mft[j],
                                    ms=4,
                                    mfc=mfc[i],
                                    mew=0.5,
                                    capsize=3,
                                    capthick=1,
                                    elinewidth=1,
                                    label=model)
                ax.legend(
                        loc=(0.36,0.74),
                        handletextpad=0.05,
                        columnspacing=0.2,
                        ncol=2,
                        frameon=False
                        )
                ax.set_xscale('log')
                ax.set_xlim(0.01,1)
                ax.set_ylim(0,1)
                ax.set_xlabel(r'$\tau_{\mathrm{mix}}/\tau_{\mathrm{res}}$')
                ax.set_ylabel(r'$\tilde{\mathrm{FI}}$')

                ax.text(
                        0.25,0.03,
                        ''.join([
                            r'$\tau_{\mathrm{res}}\,=0.01\;\mathrm{s}$',
                            '\n',
                            r'$\varphi\quad\;\!=1.2$',
                            '\n',
                            r'$\langle\varphi_r\rangle\!=4.76$',
                            '\n',
                            r'$\eta_{Z,r}\!\!\:=\;\:\!$',
                            '{:g}'.format(var)]))

                fig.subplots_adjust(
                        left = margin_left/plot_width,
                        bottom = margin_bottom/plot_height,
                        right = 1.0-margin_right/plot_width,
                        top = 1.0-margin_top/plot_height,
                        wspace = space_width/plot_width,
                        hspace = space_height/plot_height
                        )

                plot_params = copy.deepcopy(params)
                del plot_params['MIX']
                del plot_params['tres']
                del plot_params['dtmix']
                del plot_params['phif']
                del plot_params['tmix']
                del plot_params['eqv']
                plot_name = params2name(plot_params)

                fig.savefig('{}/{}.eps'.format(dst,plot_name))

                plt.close('all')
