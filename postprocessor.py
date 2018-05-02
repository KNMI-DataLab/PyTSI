# DESCRIPTION: cperform sun circle/horizon area corrections as postprocessing
#              the approach by Long is used

from myimports import *
from numpy import genfromtxt
from plotcorrectionresult import plotCorrectionResults
import csv as csv

def postProcessor():
	# set thresholds/variables/limits
	initialAdjustmentFactorLimit = 0.5 #0.5
	stDevLimit = 0.09 #0.09
	remainderStDevLimit = 0.05 #0.05
	sunSkyCoverLimit = 0.3 #0.3
	horizonSkyCoverLimit = 0.2 #0.2
	remainderLimit = 0.2 #0.2
	stDevWidth = 11 #11
	smoothingWidth = 5 #5

	# read columns of file
	df = genfromtxt('/usr/people/mos/Documents/cloudDetection/data.csv',skip_header=1,delimiter='\t')

	azimuth = df[:,2]
	outsideC = df[:,14] ; outsideS = df[:,15]
	horizonC = df[:,16] ; horizonS = df[:,17]
	innerC   = df[:,18] ; innerS   = df[:,19]
	sunC     = df[:,20] ; sunS     = df[:,21]

	nSamples = len(df[:,0])

	# total amount of sun and cloud pixels
	sun   = np.add(sunS, np.add(horizonS, np.add(innerS, outsideS)))
	cloud = np.add(sunC, np.add(horizonC, np.add(innerC, outsideC)))

	# total sky cover before corrections
	originalSkyCover = np.divide(cloud, (sun + cloud))

	# individual sky covers of different parts
	sunSkyCoverIndiv = np.divide(sunC, (sunS + sunC))
	horizonSkyCoverIndiv = np.divide(horizonC, (horizonS + horizonC))

	# what part of the total sky cover is made up of sun and horizon areas
	sunSkyCoverPartial = np.divide(sunC, (sun + cloud))
	horizonSkyCoverPartial = np.divide(horizonC, (sun + cloud))

	# first guess
	remainderSkyCover = np.subtract(originalSkyCover, np.add(sunSkyCoverPartial, horizonSkyCoverPartial))

	initialAdjustmentFactor = np.subtract(1, remainderSkyCover)


	initialAdjustmentFactor = np.where(initialAdjustmentFactor>initialAdjustmentFactorLimit,
			 				  initialAdjustmentFactorLimit,
			 			  	  initialAdjustmentFactor)

	firstGuess = np.multiply(sunC, initialAdjustmentFactor)

	# calculate standard deviations
	sunStDev = np.zeros(nSamples)
	remainderStDev = np.zeros(nSamples)
	horizonStDev = np.zeros(nSamples)
	for i in range(0+stDevWidth,nSamples-stDevWidth):
		sunStDev[i] = np.std(sunSkyCoverIndiv[i-stDevWidth:i+stDevWidth])
		remainderStDev[i] = np.std(remainderSkyCover[i-stDevWidth:i+stDevWidth])
		horizonStDev[i] = np.std(horizonSkyCoverIndiv[i-stDevWidth:i+stDevWidth])

	cloudCorrected = np.copy(cloud)
	sunCorrected = np.copy(sun)

	#carry out corrections if criterions match
	# sun circle
	cloudCorrected = np.where(np.logical_and(sunStDev<stDevLimit,
							  np.logical_and(sunSkyCoverIndiv>sunSkyCoverLimit,
							  np.logical_and(remainderSkyCover<remainderLimit,
							  remainderStDev<remainderStDevLimit))),
							  cloudCorrected - sunC, cloudCorrected - firstGuess)

	sunCorrected = np.where(np.logical_and(sunStDev<stDevLimit,
							  np.logical_and(sunSkyCoverIndiv>sunSkyCoverLimit,
							  np.logical_and(remainderSkyCover<remainderLimit,
							  remainderStDev<remainderStDevLimit))),
							  sunCorrected + sunC, sunCorrected + firstGuess)

	# horizon area
	cloudCorrected = np.where(np.logical_and(horizonStDev<stDevLimit,
							  np.logical_and(horizonSkyCoverIndiv>horizonSkyCoverLimit,
							  np.logical_and(remainderSkyCover<remainderLimit,
							  remainderStDev<remainderStDevLimit))),
							  cloudCorrected - horizonC, cloudCorrected)

	sunCorrected = np.where(np.logical_and(horizonStDev<stDevLimit,
							  np.logical_and(horizonSkyCoverIndiv>horizonSkyCoverLimit,
							  np.logical_and(remainderSkyCover<remainderLimit,
							  remainderStDev<remainderStDevLimit))),
							  sunCorrected + horizonC, sunCorrected)

	# corrected sky cover
	correctedSkyCover = np.divide(cloudCorrected, (sunCorrected + cloudCorrected))

	difference = np.subtract(originalSkyCover, correctedSkyCover)

	# smoothing
	runningMean = np.copy(difference)

	for i in range(0+smoothingWidth,nSamples-smoothingWidth):
		runningMean[i] = np.mean(difference[i-smoothingWidth:i+smoothingWidth])

	smoothCorrectedSkyCover = originalSkyCover - runningMean

	# plot
	plotCorrectionResults(azimuth,correctedSkyCover,smoothCorrectedSkyCover,stDevWidth)

	# zip data and put into file
	rows = zip(azimuth,correctedSkyCover,smoothCorrectedSkyCover)

	with open('corrections.csv', 'w') as f:
		writer = csv.writer(f, delimiter='\t')
		writer.writerow(['azimuth','correctedSkyCover','smoothCorrectedSkyCover'])
		for row in rows:
			writer.writerow(row)
