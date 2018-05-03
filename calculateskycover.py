# DESCRIPTION: calculate the fractionalsky cover based on fixed thresholding

from myimports import *
import math

def calculateSkyCover(redBlueRatio,sunnyThreshold,thinThreshold):
	# calculate number of sunny/thin and opaque pixels
	sunnyPixels  = np.sum(np.logical_and(redBlueRatio>0.01, redBlueRatio<=sunnyThreshold))
	thinPixels   = np.sum(np.logical_and(redBlueRatio>0.01, np.logical_and(redBlueRatio>sunnyThreshold,redBlueRatio<=thinThreshold)))
	opaquePixels = np.sum(np.logical_and(redBlueRatio>0.01, redBlueRatio>thinThreshold))

	cloudyPixels = thinPixels + opaquePixels

	thinSkyCover = thinPixels / (sunnyPixels+cloudyPixels)
	opaqueSkyCover = opaquePixels / (sunnyPixels+cloudyPixels)
	fractionalSkyCover = thinSkyCover + opaqueSkyCover

	# check for NaN and odd values
	if math.isnan(np.min(redBlueRatio)):
		print('R/B ratio NaN found')
		sys.exit('')

	if sunnyPixels + cloudyPixels > resolution.y*resolution.x:
		print('Total amount of non-mask pixels error: ',sunnyPixels,cloudyPixels)
		sys.exit('')

	return thinSkyCover, opaqueSkyCover, fractionalSkyCover
