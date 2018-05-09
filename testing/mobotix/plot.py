import matplotlib.pyplot as plt
import numpy as np


data = np.loadtxt('mobotix_cloud_cover.csv', delimiter='\t')

plt.plot(data[:,0],data[:,2])
plt.grid()
plt.show()
plt.close()
