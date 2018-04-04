###############################################################################
# DESCRIPTION: calculates the intensity of the masked image
#              the calculation consists of computing 1/2 of the sum of
#              the three color components (or simply: calculating the average)
#
#
# AUTHOR: Job Mos						# EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *

def calculateIntensity(maskedImg):
	# setup the numpy array, fill it with zeros
	intensityValues = np.zeros([settings.yres,settings.xres])

	# compute the average of RGB for each pixel
	for i in range (0,settings.yres):
		for j in range (0,settings.xres):
			#avoiding the masked part of the image
			if maskedImg[i,j,0] != 0:
				intensityValues[i,j] = sum(maskedImg[i,j])

	grid = intensityValues.reshape((settings.yres, settings.settings.xres))
	plt.imshow(grid, cmap='gray')
	plt.show()

	return intensityValues