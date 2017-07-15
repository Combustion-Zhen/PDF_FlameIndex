"""
Zhen Lu, 2017/07/12 <albert.lz07@gmail.com>
Plot PaSR results, scatter plot in Z, T space
"""

import numpy as np
import matplotlib.pyplot as plt

SMALL = 1.e-20
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

Z=[]
I=[]
I_S=[]
for p in particle:
    if abs(p[-1]) > SMALL or abs(p[-2]) > SMALL:
        Z.append(p[0])
        I.append(p[2])
        dC = abs(p[-1])/max(p[1],SMALL)
        dZ = abs(p[-2])/max(p[0],SMALL)
        #NI=abs(p[-1])/(abs(p[-1])+abs(p[-2]))
        NI=dC/(dC+dZ)
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

isa = np.array(I_S)
isa_p = isa[isa>0.9]
num_p = isa_p.size
isa_n = isa[isa<0.5]
num_n = isa_n.size
print(num_p)
print(num_n)
