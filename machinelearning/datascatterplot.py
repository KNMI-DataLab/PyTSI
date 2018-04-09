import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors

data = np.genfromtxt('data_tsi_32levels.csv', delimiter=',', names=['filename','meanR','meanG','meanB','stDev','skewness','diffRG','diffRB','diffGB','energy','entropy','contrast','homogeneity','cloudClass'])

#plt.plot(data['azimuth'],data['thinskycoverTSI']*100, color = 'tab:red', label = 'thin (TSI)', linewidth = 2.0)

xdata = 'diffRB'
ydata = 'homogeneity'

plt.scatter(data[xdata],data[ydata],c=data['cloudClass'])

plt.xlabel(xdata)
plt.ylabel(ydata)

plt.grid()
#plt.xlim([0,32])
#plt.legend(loc = 'upper center')
#plt.set_xlabel('azimuth (deg)')

plt.colorbar()

plt.show()

plt.close()
