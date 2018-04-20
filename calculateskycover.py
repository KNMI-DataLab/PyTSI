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

	# classify each pixel as cloudy/clear
	# for i in range (0,settings.yres):
	# 	for j in range (0,settings.xres):
	# 		# avoid mask
	# 		if redBlueRatio[i,j] != 0:
	# 			if redBlueRatio[i,j] <= sunnyThreshold:
	# 				sunnyPixels += 1
	# 			elif redBlueRatio[i,j] <= thinThreshold:
	# 				thinPixels += 1
	# 			else:
	# 				opaquePixels += 1)

	sunnyPixels = np.sum(((redBlueRatio!=0) & (redBlueRatio<=sunnyThreshold)))
	thinPixels = np.sum(((redBlueRatio!=0) & (redBlueRatio>sunnyThreshold)) & (redBlueRatio<=thinThreshold))
	opaquePixels = np.sum(((redBlueRatio!=0) & (redBlueRatio>thinThreshold)))

	cloudyPixels = thinPixels + opaquePixels

	thinSkyCover = thinPixels / (sunnyPixels+cloudyPixels)
	opaqueSkyCover = opaquePixels / (sunnyPixels+cloudyPixels)
	fractionalSkyCover = thinSkyCover + opaqueSkyCover

	print('number of sunny pixels + cloudy pixels =',sunnyPixels+cloudyPixels)

	if sunnyPixels + cloudyPixels > 60000:
		sys.exit('')

	return thinSkyCover, opaqueSkyCover, fractionalSkyCover
