
# coding: utf-8

# """
# Zhen Lu 2018/04/23
# plot the averaged flame index and mixing rate of PaSR results
# """

# In[1]:


import numpy as np
import pandas as pd
from counterflow_file import *

def weighted_avg_and_var(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    # Fast and numerically precise:
    variance = np.average((values-average)**2, weights=weights)
    return {'avg':average, 'var':variance}


# In[2]:


models = np.array(['IEM','EMST','IEMHYB','EMSTHYB'])

mix_res_ratio = [0.035, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]

params = {}
params['MIX'] = None
params['tres'] = 1.e-2
params['tmix'] = None
params['eqv'] = 1.0
params['Zfvar'] = 0.1
params['dtmix'] = 0.01
params['phif'] = 4.76

# In[3]:

Z_f = np.genfromtxt('template/flame_Z.dat',skip_header=1,usecols=(0,))
Z_lb = np.arange(0,Z_f.min(),0.004)
Z_ub = np.arange(Z_f.max(),0.2,0.005)
Z_ub = np.delete(Z_ub,0)
Z_r = np.arange(0.22,1,0.02)
Z_bins = np.concatenate((Z_lb,Z_f,Z_ub,Z_r,[1,]))

Z_mid = (Z_bins[1:]+Z_bins[:-1])/2
num_bins = len(Z_mid)

df = pd.DataFrame(Z_mid,index=np.arange(1,num_bins+1),columns=['Z',])

data_params = {}
data_params['MIX'] = None
data_params['tmix'] = None
data_params['var'] = None
data_params['statics'] = None

# obtain data
for i, tmix_ratio in enumerate(mix_res_ratio):
    params['tmix'] = tmix_ratio
    data_params['tmix'] = tmix_ratio
    for j, model in enumerate(models):
        params['MIX'] = model
        data_params['MIX'] = model
        
        case = params2name(params)
        
        # fifull.op, containing time, flameindex, Z, c, rho
        file_name = '/'.join([case,'fifull.op'])
        data = np.genfromtxt(file_name)
        
        data = data[data[:,2]>=0,:]
        data = data[data[:,2]<=1,:]
        
        data[:,0] = np.digitize(data[:,2],Z_bins)
        
        df_tmp = pd.DataFrame(data,columns=list('BFZCR'))
        # conditioning on Z
        df_tmp = df_tmp.groupby('B')
        
        # statics for FI and c
        for var in list('FC'):
            data_params['var'] = var

            data_tmp = df_tmp.apply(
                    lambda x: weighted_avg_and_var(x[var],x['R']))
            
            for statics in ['avg','var']:
                data_params['statics'] = statics
                data_name = params2name(data_params)

                s_tmp = np.array([x[statics] for x in data_tmp.values])
                df_new = pd.DataFrame(
                        s_tmp,
                        index=data_tmp.index,
                        columns=[data_name,])
            
                df = df.combine_first(df_new)


# In[9]:


df.index.name = 'B'
df.to_csv('cond-FC_eqv-{:g}.csv'.format(params['eqv']))

