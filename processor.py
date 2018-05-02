# DESCRIPTION: main processing function containing calls to many functions

from myimports import *

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
from calculateskycoverHYTA import calculateSkyCoverWithHYTA
from set_hyta_threshold import setHYTAThreshold
from overlay_outlines_on_HYTA_image import overlayOutlinesOnHYTAImage
from plot_HYTA_histogram import plotHYTAHistogram
from completeplot import completeplot

def processor(img, imgTSI, azimuth, altitude, filename):
	# create mask
	mask = createmask(img, azimuth, altitude)

	# apply the mask and display the result
	maskedImg = cv2.bitwise_and(img, mask)

	# plot the data onto a 3d projected plane
	#project3d(maskedImg)

	# plot the overview showing the image, mask, and histogram
	#overviewPlot(img,mask,maskedImg)

	# set thresholds for plotting and sky cover calculations
	sunnyThreshold,thinThreshold = setThresholds()
	HYTAThreshold,HYTACloud,HYTASun,flatNormalizedRatioBRNoZeros,stDev = setHYTAThreshold(maskedImg)

	# calculate red/blue ratio per pixel
	redBlueRatio = calculateRatio(maskedImg)

	# create the segments for solar correction
	regions, outlines, labels, stencil, imageWithOutlines = createRegions(img, imgTSI, azimuth, altitude, filename)

	# plot the reb/blue ratios
	#plotRatio(img,redBlueRatio, sunnyThreshold, thinThreshold, filename)

	# calculate fractional skycover
	thinSkyCover, opaqueSkyCover, fractionalSkyCover = calculateSkyCover(redBlueRatio, sunnyThreshold, thinThreshold)
	fractionalSkyCoverHYTA = calculateSkyCoverWithHYTA(HYTACloud,HYTASun)

	# overlay outlines on image(s)
	imageWithOutlines = overlayOutlinesOnImage(redBlueRatio,outlines,stencil)
	imageWithOutlinesHYTA = overlayOutlinesOnHYTAImage(maskedImg,outlines,stencil,HYTAThreshold,filename)

	# get some data before doing actual solar/horizon area corrections
	outsideC, outsideS, horizonC, horizonS, innerC, innerS, sunC, sunS = preSolarCorrection(labels, redBlueRatio, sunnyThreshold)

	# plot overview with outlines
	#saveOutputToFigures(filename,img,imgTSI,regions,imageWithOutlines,imageWithOutlinesHYTA)

	# plot complete overview with 5 different images, histogram and cloud cover comparisons
	completeplot(filename,img,imgTSI,regions,imageWithOutlines,imageWithOutlinesHYTA,azimuth,flatNormalizedRatioBRNoZeros,HYTAThreshold,stDev)

	return thinSkyCover, opaqueSkyCover, fractionalSkyCover,fractionalSkyCoverHYTA, maskedImg, outsideC, outsideS, horizonC, horizonS, innerC, innerS, sunC, sunS
