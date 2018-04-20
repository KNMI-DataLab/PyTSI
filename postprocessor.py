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

# read columns of file
df = genfromtxt('/usr/people/mos/Documents/cloudDetection/data_backup.csv',delimiter='\t')

print(data[:,1])
sys.exit('')

# sky cover calculations

sun            = sunS + horizonS + innerS	+ outsideS
cloud          = sunC + horizonC + innerC	+ outsideC

skyCoverSuncircle = sunC / (sun + cloud)
skyCoverHorizon   = horizonC   / (sun + cloud)

totalSkyCover = cloud / (sun + cloud)

# initial guess
remainderSkyCover = totalSkyCover - skyCoverSuncircle - skyCoverHorizon
initialAdjustmentFactor = 1 - remainderSkyCover

if initialAdjustmentFactor > initialAdjustmentFactorLimit:
	initialAdjustmentFactor = initialAdjustmentFactorLimit

firstGuess = sunC * initialAdjustmentFactor

# calculate running

# sun circle performStatisticalAnalysis

# horizon area analysis

# 11 point smoothing

# adjust sky cover amount
