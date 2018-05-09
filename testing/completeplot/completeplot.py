import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors
from PIL import Image
import matplotlib.image as mpimg

def completeplot(filename,img,imgTSI,regions,imageWithOutlines,imageWithOutlinesHYTA,azimuth):
	currentAzimuth = azimuth

	data = np.genfromtxt('../../data_backup.csv', delimiter='\t', names=['filename',
															'altitude',
															'azimuth',
															'thinskycover',
															'opaqueskycover',
															'totalskycover',
															'HYTAskycover',
															'thinskycoverTSI',
															'opaqueskycoverTSI',
															'totalskycoverTSI',
															'energy',
															'entropy',
															'contrast',
															'homogeneity'])

	gs = gridspec.GridSpec(3, 5)
	ax10 = plt.subplot(gs[0, 1])
	ax20 = plt.subplot(gs[0, 2])
	ax30 = plt.subplot(gs[0, 3])
	ax40 = plt.subplot(gs[0, 4])
	ax50 = plt.subplot(gs[0, 5])
	plt.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax2 = plt.subplot(gs[1:,:2])
	ax3 = plt.subplot(gs[1,2:])
	ax4 = plt.subplot(gs[2,2:])

	histogram = mpimg.imread('../../results/test/2018020108480.png')

	img = img[...,::-1] # convert from BGR -> RGB
	imgTSI = imgTSI[...,::-1] # convert from BGR -> RGB

	ax10.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax10.set_title('Original image')
	ax10.imshow(img)

	ax20.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax20.set_title('Old software')
	ax20.imshow(imgTSI)

	ax30.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax30.set_title('New segments')
	ax30.imshow(regions)

	ax40.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax40.set_title('Fixed')
	ax40.imshow(imageWithOutlines)

	ax50.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax50.set_title('HYTA')
	ax50.imshow(imageWithOutlinesHYTA)

	ax2.imshow(histogram)

	ax3.plot(data['azimuth'],data['totalskycoverTSI']*100, color = 'tab:red', label = 'Old software', linewidth = 2.0)
	ax3.plot(data['azimuth'],data['totalskycover']*100, color = 'tab:green', label = 'New software', linewidth = 2.0)
	ax3.plot(data['azimuth'],data['HYTAskycover']*100, color = 'tab:purple', label = 'HYTA', linewidth = 2.0)
	ax3.axvline(currentAzimuth, color='k', linestyle='dashed', linewidth=2, label='threshold:'+str(round(currentAzimuth, 2)))

	ax4.plot(data['azimuth'],abs((data['totalskycoverTSI']-data['totalskycover'])*100), color = 'tab:green', label = 'Old-new', linewidth = 2.0)
	ax4.plot(data['azimuth'],abs((data['totalskycoverTSI']-data['HYTAskycover'])*100), color = 'tab:purple', label = 'Old-new', linewidth = 2.0)
	ax4.axvline(currentAzimuth, color='k', linestyle='dashed', linewidth=2, label='threshold:'+str(round(currentAzimuth, 2)))

	ax3.set_ylabel('absolute (%)')
	ax4.set_ylabel('difference (%)')
	ax4.set_xlabel('azimuth (deg)')

	ax3.set_ylim([-5,105])
	ax4.set_ylim([-5,105])

	ax3.grid()
	ax4.grid()

	# for i in images:
		# load 5x1 image
		# load histogram
		# get azimuth

		# plot 5x1 image
		# plot hitogram
		# plot cloud fraction with azimuth line
		# plot cloud fraction difference with azimuth line

	plt.tight_layout(pad=0.3)

	plt.show()
