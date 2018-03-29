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
	# calculate image properties (resolution of the image)
	# calculation doesn't work yet, setting manually
	#[xres,yres]=img.shape
	xres = 288
	yres = 352

	# setup the numpy array, fill it with zeros
	redBlueRatio = np.zeros([yres,xres])

	# blue red ratio calculation for each pixel in the image
	for i in range (0,yres):
		for j in range (0,xres):
			# check whether on pixel is part of mask
			# if pixel is masked, do nothing
			if maskedImg[i,j,0] == 0:
				continue
			else:
				# i = ypixel, j = xpixel, 0,2 = blue, red
				redBlueRatio[i,j] = maskedImg[i,j,2] / maskedImg[i,j,0]

	return redBlueRatio