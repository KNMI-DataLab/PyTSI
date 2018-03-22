###############################################################################
# DESCRIPTION: Reads a file from the image library, creates a circular mask
#              using OpenCV (cv2), applies the mask and creates a histogram
#              of the masked image.
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

# load the original image and displayi it
# flag "1" indicates color image
# flag "0" indicates greyscale image
# flag "-1" indicates unchanged (?) image
img = cv2.imread('processed_images/semi_clouds.jpg')
#cv2show(img,"Original image")

# resolution of the image ( 352x288(x3) ) 
# print(img.shape)

# create mask
mask = createmask(img)

# apply the mask and display the result
maskedImg = cv2.bitwise_and(img, mask)
# cv2.namedWindow("Masked Image", cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Masked Image', 600,600)
# cv2.imshow("Masked Image", maskedImg)
# cv2.waitKey(0)

# plot the overview showing the image, mask, and histogram
#overviewPlot(img,mask,maskedImg)

# set thresholds for plotting and sky cover calculations
sunnyThreshold,thinThreshold = setThresholds()

# calculate red/blue ratio per pixel
redBlueRatio = calculateRatio(img, maskedImg)

# plot the reb/blue ratios
#plotRatio(img,redBlueRatio, sunnyThreshold, thinThreshold)

# can add:
# if the average of all the ratios is > ... sunny
# if the average of all the ratios is < ... cloudy
# or vice versa

# calculate solid angle corrections
#calculateSACorrections(...)

# calculate fractional skycover
calculateSkyCover(redBlueRatio, sunnyThreshold, thinThreshold)