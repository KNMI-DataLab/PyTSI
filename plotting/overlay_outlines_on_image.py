###############################################################################
# DESCRIPTION: read the information from the properties file
#
#
#
#
# AUTHOR: Job Mos			            # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *
from setthresholds import setThresholds

np.set_printoptions(threshold=np.nan)

def overlayOutlinesOnImage(img,outlines,stencil):
	yres, xres = img.shape
	nColors = 1
	imgRGB = np.zeros(outlines.shape, np.uint8)

	sunnyThreshold,thinThreshold = setThresholds()

	#sunny
	imgRGB[np.where(np.logical_and(img>0,img<=sunnyThreshold))] = (0,0,255)
	#thin
	imgRGB[np.where(np.logical_and(img>=sunnyThreshold,img<=thinThreshold))] = (150,150,150)
	#opaque
	imgRGB[np.where(img>=thinThreshold)] = (255,255,255)
	#mask
	imgRGB[np.where(img==0)] = (0,0,0)

	# create mask of outlines and create inverse mask
	img2gray = cv2.cvtColor(outlines,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)

	# black out area of outlines
	img_bg = cv2.bitwise_and(imgRGB[0:yres,0:xres], imgRGB[0:yres,0:xres], mask = mask_inv)

	# take only region of outlines from outlines image
	outlines_fg = cv2.bitwise_and(outlines, outlines, mask = mask)

	dst = cv2.add(img_bg,outlines_fg)

	imageWithOutlines = cv2. bitwise_and(dst,stencil)

	return imageWithOutlines
