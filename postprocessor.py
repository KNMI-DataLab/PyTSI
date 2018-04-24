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
from numpy import genfromtxt
from plotcorrectionresult import plotCorrectionResults

# set thresholds/variables
initialAdjustmentFactorLimit = 0.5
stDevLimit = 0.09
remainderStDevLimit = 0.05
sunSkyCoverLimit = 0.3
horizonSkyCoverLimit = 0.2
remainderLimit = 0.2
stDevWidth = 11
smoothingWidth = 5

# read columns of file
df = genfromtxt('/usr/people/mos/Documents/cloudDetection/data_backup.csv',delimiter='\t')

azimuth = df[:,2]

outsideC = df[:,13] ; outsideS = df[:,14]
horizonC = df[:,15] ; horizonS = df[:,16]
innerC   = df[:,17] ; innerS   = df[:,18]
sunC     = df[:,19] ; sunS     = df[:,20]

nSamples = len(df[:,0])

# sky cover calculations

sun   = np.add(sunS, np.add(horizonS, np.add(innerS, outsideS)))
cloud = np.add(sunC, np.add(horizonC, np.add(innerC, outsideC)))

# individual sky covers of different parts
sunSkyCoverIndiv = np.divide(sunC, (sunS + sunC))
horizonSkyCoverIndiv = np.divide(horizonC, (horizonS + horizonC))

# what part of the total sky cover is made up of sun and horizon areas
sunSkyCoverPartial = np.divide(sunC, (sun + cloud))
horizonSkyCoverPartial = np.divide(horizonC, (sun + cloud))

originalSkyCover = np.divide(cloud, (sun + cloud))

# initial guess
remainderSkyCover = np.subtract(originalSkyCover, np.add(sunSkyCoverPartial, horizonSkyCoverPartial))

initialAdjustmentFactor = np.subtract(1, remainderSkyCover)


initialAdjustmentFactor = np.where(initialAdjustmentFactor>initialAdjustmentFactorLimit,
		 				  initialAdjustmentFactorLimit,
		 			  	  initialAdjustmentFactor)

firstGuess = np.multiply(sunC, initialAdjustmentFactor)

# calculate running mean

# sun circle/horizon area analysis
sunStDev = np.zeros(nSamples)
remainderStDev = np.zeros(nSamples)
horizonStDev = np.zeros(nSamples)
for i in range(0+stDevWidth,nSamples-stDevWidth):
	sunStDev[i] = np.std(sunSkyCoverIndiv[i-stDevWidth:i+stDevWidth])
	remainderStDev[i] = np.std(remainderSkyCover[i-stDevWidth:i+stDevWidth])
	horizonStDev[i] = np.std(horizonSkyCoverIndiv[i-stDevWidth:i+stDevWidth])

cloudCorrected = np.copy(cloud)
sunCorrected = np.copy(sun)

# essentially an if-statement which returns x if true, y if negative
# where x is cloudCorrected - sunC and y is cloudCorrected
# equal for other corrections
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
						  sunCorrected - sunC, sunCorrected + firstGuess)

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

correctedSkyCover = np.divide(cloudCorrected, (sunCorrected + cloudCorrected))

# 11 point smoothing
difference = np.subtract(originalSkyCover, correctedSkyCover)

runningMean = np.copy(difference)

for i in range(0+smoothingWidth,nSamples-smoothingWidth):
	runningMean[i] = np.mean(difference[i-smoothingWidth:i+smoothingWidth])

smoothCorrectedSkyCover = originalSkyCover - runningMean

# plot
plotCorrectionResults(azimuth,correctedSkyCover,smoothCorrectedSkyCover,stDevWidth)
