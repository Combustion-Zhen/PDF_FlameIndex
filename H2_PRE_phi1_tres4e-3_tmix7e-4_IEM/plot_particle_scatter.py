"""
Zhen Lu, 2017/07/12 <albert.lz07@gmail.com>
Plot PaSR results, scatter plot in Z, T space
"""

import numpy as np
import matplotlib.pyplot as plt

# import data
particle = np.genfromtxt('particle_post.dat')

fig = plt.figure(1)

plt.scatter(particle[:,0],particle[:,2])

plt.show()

fig = plt.figure(2)

plt.scatter(particle[:,0],particle[:,1])

plt.show()
