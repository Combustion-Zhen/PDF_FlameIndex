"""
Zhen Lu, 10/07/2017 <albert.lz07@gmail.com>
python script to plot the results of PaSR
"""
import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt

# temperautre 17
pasr_mean=np.genfromtxt('pasrm.op',usecols=(3,17))

fig = plt.figure()

plt.plot(pasr_mean[:,0],pasr_mean[:,1])

plt.show()
