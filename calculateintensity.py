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

	# calculate image properties (resolution of the image)
	# calculation doesn't work yet, setting manually
	#[xres,yres]=img.shape
	xres=288
	yres=352

	# setup the numpy array, fill it with zeros
	intensityValues = np.zeros([yres,xres])

	# compute the average of RGB for each pixel
	for i in range (0,yres):
		for j in range (0,xres):
			#avoiding the masked part of the image
			if maskedImg[i,j,0] != 0:
				intensityValues[i,j] = sum(maskedImg[i,j])

	grid = intensityValues.reshape((yres, xres))
	plt.imshow(grid, cmap='gray')
	plt.show()

	return intensityValues