"""
Zhen Lu, 2017/10/31
plot the scatter plot of Z, C, and FI of PaSR calculation
"""
import numpy as np
import matplotlib.pyplot as plt

p = np.genfromtxt('particle_fi.dat')

flag = [a and b for a, b in zip(p[:,-1]>1.e-20,p[:,-2]>1.e-20)]

plt.scatter(p[flag,0],p[flag,1],c=p[flag,2])
plt.show()
