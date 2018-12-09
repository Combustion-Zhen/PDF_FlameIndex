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

models = np.array([['IEM','EMST'],
                   ['IEMHYB','EMSTHYB']])
modeln = np.array([['IEM','EMST'],
                   ['IEM-FI','EMST-FI']])
colors = np.array([
        ['tab:orange','tab:purple'],
        ['tab:blue','tab:red']])

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
margin_left   = 1.3
margin_right  = 0.22
margin_bottom = 0.85
margin_top    = 0.1
space_width   = 0.
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
num_rows = 2

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.4

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
                        num_rows,num_cols,sharex=True,
                        figsize=cm2inch(plot_width,plot_height))

                ax[0].plot([0,1],[0.5,0.5],'k--',linewidth=1)

                for i in range(2):
                    for j in range(2):
                        model = models[i,j]
                        label = modeln[i,j]
                        params['MIX'] = model


                        for phi in equiv_ratio:
                            params['eqv'] = phi

                            data = np.zeros((len(mix_res_ratio),5))

                            for k, tmix_ratio in enumerate(mix_res_ratio):
                                tmix = tmix_ratio*tres
                                params['tmix'] = tmix_ratio

                                case = params2name(params)
                                file_name = '/'.join([model,case,dat_name])

                                if os.path.exists(file_name):
                                    FI = np.genfromtxt(file_name,usecols=(3,))
                                    T = np.genfromtxt(file_name,usecols=(-4,))
                                else:
                                    print(file_name)
                                    continue

                                FI_ave = np.mean(FI[-300:])
                                FI_rms = np.std(FI[-300:])

                                T_ave = np.mean(T[-300:])
                                T_rms = np.std(T[-300:])

                                data[k,0] = tmix_ratio
                                data[k,1] = FI_ave
                                data[k,2] = FI_rms
                                data[k,3] = T_ave
                                data[k,4] = T_rms

                            flag = data[:,1] > 0.05
                            #ax[i,j].plot(data[flag,0],data[flag,1],label='{:g}'.format(phi))
                            ax[0].errorbar(
                                    data[flag,0],
                                    data[flag,1],
                                    yerr=2*data[flag,2],
                                    c=colors[i,j],
                                    fmt=mft[j],
                                    ms=4,
                                    mfc=mfc[i],
                                    mew=0.5,
                                    capsize=3,
                                    capthick=1,
                                    elinewidth=1,
                                    label=label)

                            ax[1].errorbar(
                                    data[flag,0],
                                    data[flag,3],
                                    yerr=2*data[flag,4],
                                    c=colors[i,j],
                                    fmt=mft[j],
                                    ms=4,
                                    mfc=mfc[i],
                                    mew=0.5,
                                    capsize=3,
                                    capthick=1,
                                    elinewidth=1,
                                    label=label)

                ax[1].legend(
                        handletextpad=0.05,
                        columnspacing=0.2,
                        ncol=2,
                        frameon=False
                        )
                ax[0].set_xscale('log')
                ax[0].set_xlim(0.01,1)
                ax[0].set_ylim(0.45,1)
                ax[0].set_yticks([0.5,0.75,1])
                ax[0].set_yticklabels(['0','0.5','1'])
                ax[1].set_ylim(1000,2000)
                ax[1].set_xlabel(r'$\tau_{\mathrm{mix}}/\tau_{\mathrm{res}}$')
                ax[0].set_ylabel(r'$\langle\tilde{\mathrm{FI}}\rangle$',labelpad=10)
                ax[1].set_ylabel(r'$\langle\tilde{T}\rangle\;(\mathrm{K})$')

                ax[0].text(
                        0.23,0.8,
                        ''.join([
                            r'$\tau_{\mathrm{res}}\,=0.01\;\mathrm{s}$',
                            '\n',
                            r'$\varphi\quad\;\!=1.2$',
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
