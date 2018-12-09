"""
Zhen Lu, 2017/10/31
plot the scatter plot of Z, C, and FI of PaSR calculation
"""
import numpy as np
import matplotlib.pyplot as plt

p = np.genfromtxt('particle_fi.dat')

plt.scatter(p[:,1],p[:,2],c=p[:,0])
plt.show()
