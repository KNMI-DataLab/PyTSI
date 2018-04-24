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
import math

# set printing options to print full np array in stead of summarized
np.set_printoptions(threshold=np.nan)

def calculateSkyCover(redBlueRatio,sunnyThreshold,thinThreshold):

	# calculate image properties (resolution of the image)
	# calculation doesn't work yet, setting manually
	#[xres,yres]=img.shape

	# classify each pixel as cloudy/clear
	#for i in range (0,settings.yres):
	#	for j in range (0,settings.xres):
	#	# avoid mask
	#		if redBlueRatio[i,j] != 0:
	#			if redBlueRatio[i,j] <= sunnyThreshold:
	#				sunnyPixels += 1
	#			elif redBlueRatio[i,j] <= thinThreshold:
	#				thinPixels += 1
	#			else:
	#				opaquePixels += 1

	#np.savetxt('test.txt',redBlueRatio)

	sunnyPixels  = np.sum(np.logical_and(redBlueRatio>0.01, redBlueRatio<=sunnyThreshold))
	thinPixels   = np.sum(np.logical_and(redBlueRatio>0.01, np.logical_and(redBlueRatio>sunnyThreshold,redBlueRatio<=thinThreshold)))
	opaquePixels = np.sum(np.logical_and(redBlueRatio>0.01, redBlueRatio>thinThreshold))

	cloudyPixels = thinPixels + opaquePixels

	thinSkyCover = thinPixels / (sunnyPixels+cloudyPixels)
	opaqueSkyCover = opaquePixels / (sunnyPixels+cloudyPixels)
	fractionalSkyCover = thinSkyCover + opaqueSkyCover

	if math.isnan(np.min(redBlueRatio)):
		print('R/B ratio NaN found')
		sys.exit('')

	if sunnyPixels + cloudyPixels > 60000:
		print('Total amount of non-mask pixels error: ',sunnyPixels,cloudyPixels)
		sys.exit('')

	return thinSkyCover, opaqueSkyCover, fractionalSkyCover
