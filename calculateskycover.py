###############################################################################
# DESCRIPTION: calculates the fractional cloud sky cover
#             
#              
#
#
# AUTHOR: Job Mos						# EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *

# set printing options to print full np array in stead of summarized
np.set_printoptions(threshold=np.nan)

def calculateSkyCover(redBlueRatio,sunnyThreshold,thinThreshold):

	# calculate image properties (resolution of the image)
	# calculation doesn't work yet, setting manually
	#[xres,yres]=img.shape
	xres=288
	yres=352

	sunnyPixels=0
	cloudyPixels=0

	# classify each pixel as cloudy/clear
	for i in range (0,yres):
		for j in range (0,xres):
			if redBlueRatio[i,j] != 0:
				if redBlueRatio[i,j] <= sunnyThreshold:
					sunnyPixels+=1
				else:
					cloudyPixels+=1

	print('amount of sunny pixels: ', sunnyPixels)
	print('amount of cloudy pixels:', cloudyPixels)

	fractionalSkyCover = sunnyPixels/(sunnyPixels+cloudyPixels)

	print('fractional sky cover   :', fractionalSkyCover)