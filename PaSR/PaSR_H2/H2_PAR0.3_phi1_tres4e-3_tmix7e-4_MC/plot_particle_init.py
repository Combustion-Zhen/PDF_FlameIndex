import numpy as np
import matplotlib.pyplot as plt

particles = np.genfromtxt('particle_init.dat',usecols=(0,1))

fig = plt.figure()

plt.plot(particles[:,0],particles[:,1])

plt.show()
