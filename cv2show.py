###############################################################################
# DESCRIPTION: plots the image with corresponding name in OpenCV style
#             
#              
#
#
# AUTHOR: Job Mos				    # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
import cv2

def cv2show (img,name):
	cv2.namedWindow(name,cv2.WINDOW_NORMAL)
	cv2.resizeWindow(name, 600,600)
	cv2.imshow(name,img)
	cv2.waitKey(0)
