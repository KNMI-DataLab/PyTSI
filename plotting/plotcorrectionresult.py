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

def plotCorrectionResults(azimuth,correctedSkyCover,smoothCorrectedSkyCover,stDevWidth):

	data = np.genfromtxt('data_backup.csv', delimiter='\t', names=['filename',
															'altitude',
															'azimuth',
															'thinskycover',
															'opaqueskycover',
															'totalskycover',
															'thinskycoverTSI',
															'opaqueskycoverTSI',
															'totalskycoverTSI',
															'energy',
															'entropy',
															'contrast',
															'homogeneity'])

	nSamples = len(data[1])

	fig, (ax1,ax2) = plt.subplots(2, 1, sharex=True)

	#print(np.delete(data['azimuth'], np.s_[0,11]))
	#print(data['azimuth'])

	ax1.plot(data['azimuth'],data['totalskycoverTSI']*100, color = 'tab:red', label = 'Old software', linewidth = 2.0)
	ax1.plot(data['azimuth'],data['totalskycover']*100, color = 'tab:green', label = 'New software', linewidth = 2.0)
	ax1.plot(azimuth,correctedSkyCover*100, color = 'tab:blue', label = 'New software (corrected)', linewidth = 2.0)
	ax1.plot(azimuth,smoothCorrectedSkyCover*100, color = 'tab:orange', label = 'New software (corrected/smoothened)', linewidth = 2.0)

	#print(len(data['totalskycoverTSI']), len(correctedSkyCover))

	ax2.plot(data['azimuth'],abs((data['totalskycoverTSI']-data['totalskycover'])*100), color = 'tab:green', label = 'Old-new', linewidth = 2.0)
	ax2.plot(azimuth,abs((data['totalskycoverTSI']-correctedSkyCover)*100), color = 'tab:blue',label = 'Old-new(corrected)', linewidth = 2.0)
	ax2.plot(azimuth,abs((data['totalskycoverTSI']-smoothCorrectedSkyCover)*100), color = 'tab:orange',label = 'Old-new(corrected/smoothened)', linewidth = 2.0)

	ax1.set_xlabel('azimuth (deg)')
	ax1.set_ylabel('cloud fraction (%)')
	ax2.set_ylabel('cloud fraction difference (%)')
	ax1.grid()
	ax2.grid()

	ax1.set_ylim([-5,105])
	ax2.set_ylim([-1,20])

	ax1.legend(loc = 'lower center')
	ax2.legend(loc = 'upper center')

	plt.show()

	plt.close()
