"""
Zhen Lu 2017/10/25
post-process and sampling from the counterflow flame calculations

numpy 1.13 is required for np.gradient,
conflict with the conda environment of cantera, with numpy 1.12
"""

import numpy as np
import glob

npts = 1000
variance = np.arange(0.1,1.0,0.2)

# read the species names from chem.inp, guarantee the sequence
comp_names = []
spe_end = False
with open('chem.inp','r') as f:
    for line in f:
        if line[:7] == 'SPECIES':
            while True:
                newline = f.readline()[:-1].split()
                if newline[0] == 'END':
                    break
                else:
                    comp_names.extend(newline)
            break
comp_names.append('T')
comp_names.append('chi')

for case in glob.glob('*.xml'):
    flame = case[:-4]
    file_name = '{}.dat'.format(flame)
    
    # import data
    with open(file_name,'r') as f:

        fuel_str = f.readline()[:-1].split()[1:]
        fuel_TY = [float(x) for x in fuel_str]
        oxy_str = f.readline()[:-1].split()[1:]
        oxy_TY = [float(x) for x in oxy_str]

        zst_str = f.readline()[:-1].split(';')
        Zst = float(zst_str[0].split()[-1])
        Z1st = float(zst_str[1].split()[-1])

        name_str = f.readline()[:-1].split()
        comp_str = name_str[name_str.index('T'):name_str.index('Z')]

    data = np.genfromtxt(file_name,skip_header=3,names=True)

    # scalar dissipation rate
    gradZ = np.gradient(data['Z'],data['grid'])
    chi = 2.*data['nu']/0.7*gradZ*gradZ

    # requirement for Z<1 and Z>0 in the domain
    flag_Z1 = data['Z'] < 1
    flag_Z0 = data['Z'] > 0
    flag = np.all(np.vstack((flag_Z1,flag_Z0)),axis=0)

    # get the data for interpolate
    Z_interp = data[flag]['Z']

    # names read by np.genfromtxt are not exact same as text
    data_names = data.dtype.names

    dt = {'names':comp_names, 'formats':[np.float64]*len(comp_names)}
    data_interp = np.zeros(len(Z_interp), dtype=dt)
    fuel_YTchi = []
    oxy_YTchi = []

    # guarantee the sequence of compositions
    for name in comp_names[:-1]:
        data_interp[name] = data[data_names[name_str.index(name)]][flag]
        fuel_YTchi.append(fuel_TY[comp_str.index(name)])
        oxy_YTchi.append(oxy_TY[comp_str.index(name)])

    data_interp['chi'] = chi[flag]
    fuel_YTchi.append(0.)
    oxy_YTchi.append(0.)

    # check whether the mixture fraction is monotonic
    flag_mono = Z_interp[1:] > Z_interp[:-1]
    index_loc = []
    for i, mono in enumerate(flag_mono[:-1]):
        if mono != flag_mono[i+1]:
            index_loc.append(i+1)
    if len(index_loc) == 2:
        # one non-monotonic region
        Z_loc_min = Z_interp[index_loc[0]]
        Z_loc_max = Z_interp[index_loc[1]]
    elif len(index_loc) != 0:
        sys.exit('Unexpected Z profile')

    # interpolate
    # xp must be increasing
    for var in variance:
        # beta pdf
        alpha = Zst*(1./var-1.)
        beta = (1.-Zst)*(1./var-1.)
        #print(file_name)
        #print('{:g} {:g}'.format(alpha,beta))
        Z = np.random.beta(alpha,beta,npts)

        # Y, T, chi
        samples = np.zeros((npts,len(comp_names)))

        for i, Z_sample in enumerate(Z):
            for j, name in enumerate(comp_names):
                if len(index_loc) == 2:
                    if Z_sample > Z_loc_max:
                        samples[i,j] = np.interp(Z_sample,
                                Z_interp[index_loc[0]::-1],
                                data_interp[name][index_loc[0]::-1],
                                right = fuel_YTchi[j])
                    elif Z_sample < Z_loc_min:
                        samples[i,j] = np.interp(Z_sample,
                                Z_interp[-1:index_loc[1]-1:-1],
                                data_interp[name][-1:index_loc[1]-1:-1],
                                left = oxy_YTchi[j])
                    else:
                        # randomly choose one section to interpolate
                        sec_ran = np.random.uniform()
                        if sec_ran < 1./3.:
                            samples[i,j] = np.interp(Z_sample,
                                    Z_interp[index_loc[0]::-1],
                                    data_interp[name][index_loc[0]::-1],
                                    right = fuel_YTchi[j])
                        elif sec_ran < 2./3.:
                            samples[i,j] = np.interp(Z_sample,
                                    Z_interp[index_loc[0]:index_loc[1]+1],
                                    data_interp[name][index_loc[0]:index_loc[1]+1])
                        else:
                            samples[i,j] = np.interp(Z_sample,
                                    Z_interp[-1:index_loc[1]-1:-1],
                                    data_interp[name][-1:index_loc[1]-1:-1],
                                    left = oxy_YTchi[j])
                else:
                    samples[i,j] = np.interp(Z_sample,
                            Z_interp[::-1],
                            data_interp[name][::-1],
                            left = oxy_YTchi[j],
                            right = fuel_YTchi[j])

        np.savetxt('{0}_var{1:g}.sample'.format(flame,var),samples,fmt='%12.5f')
