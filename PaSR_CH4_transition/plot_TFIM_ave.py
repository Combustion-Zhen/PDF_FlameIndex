"""
Zhen Lu 2018/04/12

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
mix_res_ratio = [0.02, 0.035, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]
equiv_ratio_f = [4.76,]
equiv_ratio = [1.2,]
Zf_variance = [0.1,]
dtmix = [0.01,]

params = {}
params['MIX'] = None
params['tres'] = None
params['tmix'] = None
params['eqv'] = None
params['Zfvar'] = None
params['dtmix'] = None
params['phif'] = None

dst = '.'
dat_name = 'pasrm.op'

# plot
# figure and axes parameters
# total width is fixed, for one column plot
plot_width    = 14.4
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

num_cols = 3
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
                        num_rows,num_cols,sharex=True,
                        figsize=cm2inch(plot_width,plot_height))

                ax[1].plot([0,1],[0.5,0.5],'k--',linewidth=1)

                for i in range(2):
                    for j in range(2):
                        model = models[i,j]
                        label = modeln[i,j]
                        params['MIX'] = model


                        for phi in equiv_ratio:
                            params['eqv'] = phi

                            data = np.zeros((len(mix_res_ratio),4))

                            for k, tmix_ratio in enumerate(mix_res_ratio):
                                tmix = tmix_ratio*tres
                                params['tmix'] = tmix_ratio

                                case = params2name(params)
                                file_name = '/'.join([case,dat_name])

                                if os.path.exists(file_name):
                                    """
                                    FI = np.genfromtxt(file_name,usecols=(3,))
                                    T = np.genfromtxt(file_name,usecols=(-4,))
                                    OM = np.genfromtxt(file_name,usecols=(4,))
                                    """
                                    data_raw = np.genfromtxt(
                                            file_name,
                                            usecols=(-4,3,4)
                                            )
                                else:
                                    print(file_name)
                                    continue

                                data[k,0] = tmix_ratio
                                data[k,1:] = np.mean(data_raw[-2000:,:],axis=0)

                            flag = data[:,2] > 0.05

                            for k in range(num_cols):
                                ax[k].plot(
                                        data[flag,0],
                                        data[flag,k+1],
                                        c=colors[i,j],
                                        ls='',
                                        marker=mft[j],
                                        ms=4,
                                        mfc=mfc[i],
                                        mew=0.5,
                                        label=label
                                        )

                ax[1].legend(
                        handletextpad=0.05,
                        columnspacing=0.2,
                        ncol=2,
                        frameon=False
                        )
                ax[0].set_xscale('log')
                ax[2].plot([0.01,1],[10000,100])
                ax[2].set_yscale('log')
                ax[0].set_xlim([0.01,0.6])
                """
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
                """

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

                fig.savefig('{}/{}.pdf'.format(dst,plot_name))

                plt.close('all')
