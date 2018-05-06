
# coding: utf-8

# # get the particle information with assistance of cantera

# In[1]:


import cantera as ct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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


models = ['IEM','EMST','IEMHYB','EMSTHYB']
mix_res_ratio = [0.035, 0.06, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5]

params = {}
params['MIX'] = None
params['tres'] = 1.e-2
params['tmix'] = None
params['eqv'] = 1.0
params['Zfvar'] = 0.1
params['dtmix'] = 0.01
params['phif'] = 4.76

op_name = 'pasrfull.op'

data_params = {}
data_params['MIX'] = None
data_params['tmix'] = None
data_params['var'] = None
data_params['statics'] = None


# In[3]:


Z_f = np.genfromtxt('template/flame_Z.dat',skip_header=1,usecols=(0,))
Z_lb = np.arange(0,Z_f.min(),0.004)
Z_ub = np.arange(Z_f.max(),0.2,0.005)
Z_ub = np.delete(Z_ub,0)
Z_r = np.arange(0.22,1,0.02)
Z_bins = np.concatenate((Z_lb,Z_f,Z_ub,Z_r,[1,]))

Z_mid = (Z_bins[1:]+Z_bins[:-1])/2
num_bins = len(Z_mid)


# In[4]:


gas = ct.Solution('gri30.xml')
element_index = np.empty([len(gas.species_names),len(gas.element_names)])
for i, species in enumerate(gas.species_names):
    for j, element in enumerate(gas.element_names):
        element_index[i,j] = gas.n_atoms(species,element)


# In[5]:


# Bilger's mixture fraction
coeff_Z = ( 2 * element_index[:,gas.element_index('C')]
            + element_index[:,gas.element_index('H')] / 2
            - element_index[:,gas.element_index('O')] )

OXY = {'O2':1, 'N2':3.76}
FUEL = {'CH4':1}

T_OXY = 300.
T_FUEL = 300.

p = 1. * ct.one_atm

# oxidizer stream
gas.TPX = T_OXY, p, OXY
# specific mole number
z_OXY = gas.Y/gas.molecular_weights
Z_OXY = np.dot(coeff_Z,z_OXY)

# fuel stream
gas.TPX = T_FUEL, p, FUEL
# specific mole number
z_FUEL = gas.Y/gas.molecular_weights
Z_FUEL = np.dot(coeff_Z,z_FUEL)

# coefficients for the progress variable
C_species = ['CO2','CO','H2O','H2']
coeff_C = np.zeros(gas.n_species)
for spe in C_species:
    spe_index = gas.species_index(spe)
    coeff_C[spe_index] = gas.molecular_weights[spe_index]
    
#gas.TPX = T_OXY, p, {'CH4':1,'O2':2,'N2':3.76*2}
#z_mix = gas.Y/gas.molecular_weights
#Z_mix = np.dot(coeff_Z,z_mix)
#Z_st(Z_mix-Z_OXY)/(Z_FUEL-Z_OXY)


# In[6]:


df = pd.DataFrame(Z_mid,index=np.arange(1,num_bins+1),columns=['Z',])
# obtain data
# time, density, pressue/one_atm, temperature, sensible enthalpy, specific mole number
for model in models:
    params['MIX'] = model
    data_params['MIX'] = model
    for tmix in mix_res_ratio:
        params['tmix'] = tmix
        data_params['tmix'] = tmix
        
        case = params2name(params)

        file_name = '/'.join([case,op_name])
        data = np.genfromtxt(file_name)
        
        Z = np.dot(coeff_Z,data[:,-gas.n_species:].T)
        Z = (Z-Z_OXY)/(Z_FUEL-Z_OXY)
        
        C = np.dot(coeff_C,data[:,-gas.n_species:].T)
        
        df_tmp = pd.DataFrame({
            'Z':Z,
            'C':C,
            'T':data[:,3],
            'R':data[:,1],
            'B':np.digitize(Z,Z_bins)}).groupby('B')
        
        for var in list('CT'):
            data_params['var'] = var

            data_tmp = df_tmp.apply(lambda x: weighted_avg_and_var(x[var],x['R']))
            
            for statics in ['avg','var']:
                data_params['statics'] = statics
                data_name = params2name(data_params)

                s_tmp = np.array([x[statics] for x in data_tmp.values])
                df_new = pd.DataFrame(
                        s_tmp,
                        index=data_tmp.index,
                        columns=[data_name,])
            
                df = df.combine_first(df_new)

df.index.name = 'B'
df.to_csv('cond-CT_eqv-{:g}.csv'.format(params['eqv']))

