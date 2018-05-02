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

def plotCorrectionResults(azimuth,correctedSkyCover,smoothCorrectedSkyCover,stDevWidth):

	data = np.genfromtxt('data.csv', delimiter='\t', names=True)

	nSamples = len(data[1])

	fig, (ax1,ax2) = plt.subplots(2, 1, sharex=True)

	ax1.plot(data['azimuth'],data['fractionalSkyCoverTSI']*100, color = 'tab:red', label = 'Old software', linewidth = 2.0)
	ax1.plot(data['azimuth'],data['fractionalSkyCover']*100, color = 'tab:green', label = 'New software', linewidth = 2.0)
	ax1.plot(data['azimuth'],data['fractionalSkyCoverHYTA']*100, color = 'tab:purple', label = 'HYTA', linewidth = 2.0)
	ax1.plot(data['azimuth'],correctedSkyCover*100, color = 'tab:blue', label = 'New software (corrected)', linewidth = 2.0)
	ax1.plot(data['azimuth'],smoothCorrectedSkyCover*100, color = 'tab:orange', label = 'New software (corrected/smoothened)', linewidth = 2.0)

	ax2.plot(data['azimuth'],abs((data['fractionalSkyCoverTSI']-data['fractionalSkyCover'])*100), color = 'tab:green', label = 'Old-new', linewidth = 2.0)
	ax2.plot(data['azimuth'],abs((data['fractionalSkyCoverTSI']-correctedSkyCover)*100), color = 'tab:blue',label = 'Old-new(corrected)', linewidth = 2.0)
	ax2.plot(data['azimuth'],abs((data['fractionalSkyCoverTSI']-smoothCorrectedSkyCover)*100), color = 'tab:orange',label = 'Old-new(corrected/smoothened)', linewidth = 2.0)
	ax2.plot(data['azimuth'],abs((data['fractionalSkyCoverTSI']-data['fractionalSkyCoverHYTA'])*100), color = 'tab:purple',label = 'Old-new(corrected/smoothened)', linewidth = 2.0)

	ax2.set_xlabel('azimuth (deg)')
	ax1.set_ylabel('cloud fraction (%)')
	ax2.set_ylabel('cloud fraction difference (%)')
	ax1.grid()
	ax2.grid()

	ax1.set_ylim([-5,105])
	ax2.set_ylim([-1,101])

	ax1.legend(loc = 'upper center')
	ax2.legend(loc = 'upper center')

	#plt.savefig('results/comparison_sunny.png')
	plt.show()

	plt.close()
