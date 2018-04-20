###############################################################################
# DESCRIPTION: calculates the red/blue ratio of each pixel in the image
#              r~=1 indicates a cloud, r~0.5 (?) indicates blue sky
#	       https://stackoverflow.com/questions/9707676/defining-a-
#	       discrete-colormap-for-imshow-in-matplotlib
#
# AUTHOR: Job Mos	                            # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *

# set printing options to print full np array in stead of summarized
#np.set_printoptions(threshold=np.nan)

def calculateRatio(maskedImg):
	# setup the numpy array, fill it with zeros
	#redBlueRatio = np.zeros([settings.yres,settings.xres])

	# blue red ratio calculation for each pixel in the image
	# for i in range (0,settings.yres):
	# 	for j in range (0,settings.xres):
	# 		# check whether on pixel is part of mask
	# 		# if pixel is masked, do nothing
	# 		if maskedImg[i,j,0] == 0:
	# 			continue
	# 		else:
	# 			# i = ypixel, j = xpixel, 0,2 = blue, red
	# 			redBlueRatio[i,j] = maskedImg[i,j,2] / maskedImg[i,j,0]

	blueBand = np.zeros([settings.yres,settings.xres])
	redBand = np.zeros([settings.yres,settings.xres])

	blueBand = maskedImg[:,:,0]
	redBand = maskedImg[:,:,2]

	#nonzerosBlue = maskedImg[np.nonzero(maskedImg[:,:,0])]
	#nonzerosRed = maskedImg[np.nonzero(maskedImg[:,:,2])]

	redBlueRatio = np.divide(maskedImg[:,:,2],maskedImg[:,:,0],where=(blueBand!=0))

	return redBlueRatio
