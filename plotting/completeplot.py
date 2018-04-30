import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors
from PIL import Image
import matplotlib.image as mpimg

def completeplot(filename,img,imgTSI,regions,imageWithOutlines,imageWithOutlinesHYTA,azimuth,flatNormalizedRatioBRNoZeros,threshold,stDev):
	currentAzimuth = azimuth

	data = np.genfromtxt('data_backup.csv', delimiter='\t', names=['filename',
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
	# ax10 = plt.subplot(gs[0, 0])
	# ax20 = plt.subplot(gs[0, 1])
	# ax30 = plt.subplot(gs[0, 2])
	# ax40 = plt.subplot(gs[0, 3])
	# ax50 = plt.subplot(gs[0, 4])
	# plt.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	# ax2 = plt.subplot(gs[1:,:2])
	# ax3 = plt.subplot(gs[1,2:])
	# ax4 = plt.subplot(gs[2,2:])


	plt.figure(figsize=(14,8))

	ax1 = plt.subplot2grid((3,5), (0,0), colspan=1, rowspan=1)
	ax2 = plt.subplot2grid((3,5), (0,1), colspan=1, rowspan=1)
	ax3 = plt.subplot2grid((3,5), (0,2), colspan=1, rowspan=1)
	ax4 = plt.subplot2grid((3,5), (0,3), colspan=1, rowspan=1)
	ax5 = plt.subplot2grid((3,5), (0,4), colspan=1, rowspan=1)
	ax6 = plt.subplot2grid((3,5), (1,0), colspan=2, rowspan=2)
	ax7 = plt.subplot2grid((3,5), (1,2), colspan=3, rowspan=1)
	ax8 = plt.subplot2grid((3,5), (2,2), colspan=3, rowspan=1)


	ax1.set_adjustable('box-forced')
	ax2.set_adjustable('box-forced')
	ax3.set_adjustable('box-forced')
	ax4.set_adjustable('box-forced')
	ax5.set_adjustable('box-forced')

	img = img[...,::-1] # convert from BGR -> RGB
	imgTSI = imgTSI[...,::-1] # convert from BGR -> RGB

	ax1.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax1.set_title('Original image')
	ax1.imshow(img)

	ax2.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax2.set_title('Old software')
	ax2.imshow(imgTSI)

	ax3.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax3.set_title('New segments')
	ax3.imshow(regions)

	ax4.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax4.set_title('Fixed')
	ax4.imshow(imageWithOutlines)

	ax5.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax5.set_title('HYTA')
	ax5.imshow(imageWithOutlinesHYTA)

	nbins=100
	ax6.set_title('Histogram StDev='+str(stDev))
	ax6.set_ylabel('Frequency')
	ax6.set_xlabel('Normalized B/R Ratio')
	ax6.set_ylim([0,30])
	ax6.axvline(threshold, color='k', linestyle='dashed', linewidth=2, label='threshold:'+str(round(threshold, 2)))
	#plt.hist(cloudHistoData,10, range=[0,1], label='cloud', normed=1, color='tab:grey')
	#plt.hist(skyHistoData,10, range=[0,1], label='sky', histtype='bar', normed=1, color='tab:blue')
	ax6.hist(flatNormalizedRatioBRNoZeros,nbins,range=[0,1],density=1)
	ax6.legend()

	ax7.plot(data['azimuth'],data['totalskycoverTSI']*100, color = 'tab:red', label = 'Old software', linewidth = 2.0)
	ax7.plot(data['azimuth'],data['totalskycover']*100, color = 'tab:green', label = 'New software', linewidth = 2.0)
	ax7.plot(data['azimuth'],data['HYTAskycover']*100, color = 'tab:purple', label = 'HYTA', linewidth = 2.0)
	ax7.axvline(currentAzimuth, color='k', linestyle='dashed', linewidth=2, label='threshold:'+str(round(currentAzimuth, 2)))
	ax7.set_title('Cloud cover. Current azimuth='+str(currentAzimuth))

	ax8.plot(data['azimuth'],abs((data['totalskycoverTSI']-data['totalskycover'])*100), color = 'tab:green', label = 'Old-new', linewidth = 2.0)
	ax8.plot(data['azimuth'],abs((data['totalskycoverTSI']-data['HYTAskycover'])*100), color = 'tab:purple', label = 'Old-new', linewidth = 2.0)
	ax8.axvline(currentAzimuth, color='k', linestyle='dashed', linewidth=2, label='threshold:'+str(round(currentAzimuth, 2)))

	ax7.set_ylabel('absolute (%)')
	ax8.set_ylabel('difference (%)')
	ax8.set_xlabel('azimuth (deg)')

	ax7.set_ylim([-5,105])
	ax8.set_ylim([-5,105])

	ax7.grid()
	ax8.grid()

	plt.tight_layout()

	plt.savefig('results/completeoverview/'+filename)
	plt.close()
