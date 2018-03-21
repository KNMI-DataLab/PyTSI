###############################################################################
# DESCRIPTION: Reads a file from the image library, creates a circular mask
#              using OpenCV (cv2), applies the mask and creates a histogram
#              of the masked image.
#
#
# AUTHOR: Job Mos						# EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *

# import external functions
from cv2show import cv2show
from createmask import createmask
from overviewplot import overviewPlot
from calculateratio import calculateRatio

# load the original image and displayi it
# flag "1" indicates color image
# flag "0" indicates greyscale image
# flag "-1" indicates unchanged (?) image
img = cv2.imread('../images/20180309084700.jpg')
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

#plot the overview showing the image, mask, and histogram
#overviewPlot(img,mask,maskedImg)

#calculate red/blue ratio per pixel
calculateRatio(img, maskedImg)