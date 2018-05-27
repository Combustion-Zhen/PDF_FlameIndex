import numpy as np
import matplotlib.pyplot as plt

particles = np.genfromtxt('particle_info.op',usecols=(0,1))

fig = plt.figure()

plt.scatter(particles[:,0],particles[:,1])

plt.show()
