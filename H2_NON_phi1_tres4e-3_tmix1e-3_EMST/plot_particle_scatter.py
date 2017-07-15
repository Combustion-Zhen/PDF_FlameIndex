"""
Zhen Lu, 2017/07/12 <albert.lz07@gmail.com>
Plot PaSR results, scatter plot in Z, T space
"""

import numpy as np
import matplotlib.pyplot as plt

# import data
particle = np.genfromtxt('particle_post.dat')

# Flame index

fig = plt.figure(1)

plt.scatter(particle[:,0],particle[:,2])

plt.show()

print(np.average(particle[:,2]))

# Temperature

fig = plt.figure(2)

plt.scatter(particle[:,0],particle[:,3])

plt.show()

# Progress variable

fig = plt.figure(3)

plt.scatter(particle[:,0],particle[:,1])

plt.show()

scale=5.0
Z=[]
I=[]
I_S=[]
for p in particle:
    if abs(p[-1]) >1.e-10 or abs(p[-2]) > 1.e-10:
        Z.append(p[0])
        I.append(p[2])
        NI=abs(p[-1])/(abs(p[-1])+scale*abs(p[-2]))
        I_S.append(NI)
    else:
        print(p)

fig = plt.figure(4)

plt.scatter(Z,I)
plt.show()

print(np.average(np.array(I)))

fig = plt.figure(5)

plt.scatter(Z,I_S)
plt.show()

print(np.average(np.array(I_S)))
