###############################################################################
# DESCRIPTION: creates a circular mask using OpenCV (cv2), applies the mask and
#              creates a histogram of the masked image.
#              
#
#
# AUTHOR: Job Mos			            # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *

# import external functions
from cv2show import cv2show
from createmask import createmask
from overviewplot import overviewPlot
from calculateratio import calculateRatio
from plotratio import plotRatio
from calculateskycover import calculateSkyCover
from setthresholds import setThresholds
from calculateintensity import calculateIntensity
from performstatisticalanalysis import performStatisticalAnalysis

def processor(img, azimuth):
	#cv2show(img,"Original image")

	# resolution of the image ( 352x288(x3) ) 
	#print(img.shape)

	# create mask
	mask = createmask(img, azimuth)

	# apply the mask and display the result
	maskedImg = cv2.bitwise_and(img, mask)

	# plot the overview showing the image, mask, and histogram
	#overviewPlot(img,mask,maskedImg)

	# set thresholds for plotting and sky cover calculations
	sunnyThreshold,thinThreshold = setThresholds()

	# calculate red/blue ratio per pixel
	redBlueRatio = calculateRatio(maskedImg)

	# calculate the intensity values
	#intensityValues = calculateIntensity(maskedImg)

	# plot the reb/blue ratios
	#plotRatio(img,redBlueRatio, sunnyThreshold, thinThreshold)

	# calculate solid angle corrections
	#calculateSACorrections(...)

	# calculate fractional skycover
	fractionalSkyCover = calculateSkyCover(redBlueRatio, sunnyThreshold, thinThreshold)

	# calculates statistical properties of the image
	energy, entropy, contrast, homogeneity = performStatisticalAnalysis(maskedImg)

	return fractionalSkyCover, energy, entropy, contrast, homogeneity