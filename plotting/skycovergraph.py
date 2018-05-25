###############################################################################
# DESCRIPTION:
#
#
#
#
# AUTHOR: Job Mos	                            # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors
import sys as sys
import matplotlib.gridspec as gridspec

sunny = np.genfromtxt('../sunny.csv', delimiter='\t', names=True)
rainy = np.genfromtxt('../rainy.csv', delimiter='\t', names=True)
sunny_corr = np.genfromtxt('../sunny_corr.csv', delimiter='\t', names=True)
rainy_corr = np.genfromtxt('../rainy_corr.csv', delimiter='\t', names=True)

gs = gridspec.GridSpec(2, 1)

plt.figure(figsize=(14,5.6))

ax1 = plt.subplot2grid((2,1), (0,0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid((2,1), (1,0), rowspan=1, colspan=1)

ax1.set_adjustable('box-forced')
ax2.set_adjustable('box-forced')

ax1.plot(sunny['azimuth'],     sunny['fractionalSkyCoverTSI']*100, color = 'tab:red', label = 'TSI', linewidth = 2.0)
ax1.plot(sunny['azimuth'],     sunny['fractionalSkyCover']*100, color = 'tab:green', label = 'New Fixed', linewidth = 2.0)
ax1.plot(sunny_corr['azimuth'],sunny_corr['correctedSkyCover']*100, color = 'tab:blue', label = 'New Corrected', linewidth = 2.0)
ax1.plot(sunny_corr['azimuth'],sunny_corr['smoothCorrectedSkyCover']*100, color = 'tab:orange', label = 'New Corrected + Smoothened', linewidth = 2.0)
ax1.plot(sunny['azimuth'],     sunny['fractionalSkyCoverHYTA']*100, color = 'tab:purple', label = 'Hybrid', linewidth = 2.0)

ax2.plot(rainy['azimuth'],     rainy['fractionalSkyCoverTSI']*100, color = 'tab:red', label = 'TSI', linewidth = 2.0)
ax2.plot(rainy['azimuth'],     rainy['fractionalSkyCover']*100, color = 'tab:green', label = 'New Fixed', linewidth = 2.0)
ax2.plot(rainy_corr['azimuth'],rainy_corr['correctedSkyCover']*100, color = 'tab:blue', label = 'New Corrected', linewidth = 2.0)
ax2.plot(rainy_corr['azimuth'],rainy_corr['smoothCorrectedSkyCover']*100, color = 'tab:orange', label = 'New Corrected + Smoothened', linewidth = 2.0)
ax2.plot(rainy['azimuth'],     rainy['fractionalSkyCoverHYTA']*100, color = 'tab:purple', label = 'Hybrid', linewidth = 2.0)

ax2.set_xlabel('azimuth (deg)')
ax1.set_ylabel('cloud fraction (%)',labelpad=20)
ax2.set_ylabel('cloud fraction (%)',labelpad=13)

ax1.grid()
ax2.grid()

ax1.set_ylim([-5,25])
ax2.set_ylim([-5,105])

ax1.legend(loc = 'upper center', mode='expand', ncol=5)

plt.savefig('../results/sunny_rainy_comparison.eps')
plt.show()
plt.close()
