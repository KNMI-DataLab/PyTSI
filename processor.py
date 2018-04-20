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
from project3d import project3d
from createregions import createRegions
from overview_with_segments import saveOutputToFigures
from overlay_outlines_on_image import overlayOutlinesOnImage
from presolarcorrection import preSolarCorrection

def processor(img, imgTSI, azimuth, altitude, filename):
	#cv2show(img,"Original image")

	# resolution of the image ( 352x288(x3) )
	#print(img.shape)

	# create mask
	print('create mask')
	mask = createmask(img, azimuth, altitude)

	# apply the mask and display the result
	maskedImg = cv2.bitwise_and(img, mask)

	# plot the data onto a 3d projected plane
	#project3d(maskedImg)

	# plot the overview showing the image, mask, and histogram
	#overviewPlot(img,mask,maskedImg)

	# set thresholds for plotting and sky cover calculations
	print('thresholds')
	sunnyThreshold,thinThreshold = setThresholds()

	# calculate red/blue ratio per pixel
	print('calculate ratios')
	redBlueRatio = calculateRatio(maskedImg)

	# calculate the intensity values
	#intensityValues = calculateIntensity(maskedImg)

	# create the segments for solar correction
	print('create regions')
	regions, outlines, labels, stencil, imageWithOutlines = createRegions(img, imgTSI, azimuth, altitude, filename)

	# plot the reb/blue ratios
	#plotRatio(img,redBlueRatio, sunnyThreshold, thinThreshold, filename)

	# calculate solid angle corrections
	#calculateSACorrections(...)

	# calculate fractional skycover
	print('calculate sky cover')
	thinSkyCover, opaqueSkyCover, fractionalSkyCover = calculateSkyCover(redBlueRatio, sunnyThreshold, thinThreshold)

	print('overlay outlines on image')
	imageWithOutlines = overlayOutlinesOnImage(redBlueRatio,outlines,stencil)

	print('perform horizon/solar corrections')
	outsideC, outsideS, horizonC, horizonS, innerC, innerS, sunC, sunS = preSolarCorrection(labels, redBlueRatio, sunnyThreshold)

	# plot overview with outlines
	print('save output to figures')
	saveOutputToFigures(filename,img,imgTSI,regions,imageWithOutlines)

	return thinSkyCover, opaqueSkyCover, fractionalSkyCover, maskedImg, outsideC, outsideS, horizonC, horizonS, innerC, innerS, sunC, sunS
