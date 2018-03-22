###############################################################################
# DESCRIPTION: sets the thresholds used in plotting and sky cover calculation
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

def setThresholds():
	sunnyThreshold = 0.795
	thinThreshold = 0.9

	return sunnyThreshold,thinThreshold