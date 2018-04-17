###############################################################################
# DESCRIPTION: creates the mask needed for RGB calculations such as the
#              histogram and cloud/no cloud determination.
#
#
#
# AUTHOR: Job Mos				    # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
import cv2 as cv2
import scipy as scipy
from math import cos,sin,sqrt,tan,pi
import numpy as np
import matplotlib.pyplot as plt

# print options
np.set_printoptions(threshold=np.nan)

# calculate the outer point of the shadow band position required for drawing
# the shadowband line. the formula of a circle is used: x=r*cos(t),y=r*sin(t)
def calculateBandPosition(xres, yres, theta):
	# rInner defines how many pixels from the center
	# the shadowband should be drawn
	# rOuter
	rInner = 40
	rOuter = 140

	#for i in range (0,n):
	#theta=-i/(n-1)*3.1415
	xInner = int(xres / 2 + rInner * cos(theta))
	yInner = int(yres / 2 + rInner * sin(theta))
	xOuter = int(xres / 2 + rOuter * cos(theta))
	yOuter = int(yres / 2 + rOuter * sin(theta))

	return xInner,yInner,xOuter,yOuter

def polygon():
	azimuth = azimuth - 90
	width = 50
	r = xres/2
	theta = azimuth * pi / 180
	width = width * pi / 180
	p1 = [int(xres/2), int(yres/2)]
	p2 = [int(xres/2) + r * cos(theta-width), int(yres/2) + r * sin(theta-width)]
	p3 = [int(xres/2) + r * cos(theta+width), int(yres/2) + r * sin(theta+width)]
	p4 = [int(xres/2) + r * cos(theta), int(yres/2) + r * sin(theta)]
	polygon = np.array([p1,p2,p4,p3],dtype = int)
	cv2.fillConvexPoly(regions, polygon, color=(0,255,255))

def innerCircle():
	cv2.circle(regions, (int(xres/2),int(yres/2)), 90, (0,255,0), -1)

def largeCircle():
	cv2.circle(regions, (int(xres/2),int(yres/2)), radiusCircle, (255,255,0), -1)

def sunCircle():
	altitude = altitude * pi /180
	a = -0.23
	b = -tan(altitude)
	c = 1.25
	d = b**2 - 4 * a * c
	r = radiusMirror * (-b - sqrt(d)) / (2 * a) / 2
	xSun = int(xres/2 + r * cos (theta))
	ySun = int(yres/2 + r * sin (theta))
	cv2.circle(regions, (xSun,ySun), 40, (255,0,0), -1)

def createStencil():
	stencil = np.zeros((yres,xres,ncolors), dtype="uint8")
	cv2.circle(stencil, (int(xres/2), int(yres/2)), radiusCircle, (255,255,255), -1)
	return stencil

def outerCircle():
	regions = cv2.bitwise_and(regions,stencil)

def createRegions(img):
	yres, xres, ncolors = img.shape
	regions = np.zeros((yres,xres,ncolors), dtype="uint8")
	radiusCircle = 120
	radiusMirror = 140
	azimuth = 92.32342601883832
	altitude = 16.160075768731204

	# shadowband
	xInner,yInner,xOuter,yOuter = calculateBandPosition(xres, yres, theta)
	cv2.line(regions, (xInner,yInner), (xOuter,yOuter), (0,0,0), 35)

	# arm
	cv2.rectangle(regions, (141,190), (154,153), (0,0,0), -1)
	cv2.rectangle(regions, (145,154), (152,91) , (0,0,0), -1)
	cv2.rectangle(regions, (144,91) , (152,26) , (0,0,0), -1)

	# outlines
	outlines = np.zeros((yres,xres,ncolors), dtype="uint8")
	#outlines = img
	# polygon
	cv2.fillConvexPoly(outlines, polygon, color=(0,0,0))
	cv2.polylines(outlines, [polygon], True, (0,255,255),2)
	# inner circle
	cv2.circle(outlines, (int(xres/2),int(yres/2)), 90, (0,0,0), -1)
	cv2.circle(outlines, (int(xres/2),int(yres/2)), 90, (0,255,0), 2)
	# sun circle
	cv2.circle(outlines, (xSun,ySun), 40, (0,0,0), -1)
	cv2.circle(outlines, (xSun,ySun), 40, (255,0,0), 2)
	# outer circle
	cv2.circle(outlines, (int(xres/2),int(yres/2)), radiusCircle, (255,255,0), 2)
	# outer circle outside black fill
	outlines = cv2.bitwise_and(outlines,stencil)

	return regions, outlines, stencil

def main():
	global regions

	img = cv2.imread('test_img.jpg')

	# convert image to RGB
	img = img[...,::-1]

	xres, yres, ncolors = img.shape

	regions, outlines, stencil = createRegions(img)

	# create mask of outlines and create inverse mask
	img2gray = cv2.cvtColor(outlines,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)

	# black out area of outlines
	img_bg = cv2.bitwise_and(img[0:xres,0:yres], img[0:xres,0:yres], mask = mask_inv)

	# take only region of outlines from outlines image
	outlines_fg = cv2.bitwise_and(outlines, outlines, mask = mask)

	dst = cv2.add(img_bg,outlines_fg)

	result = cv2. bitwise_and(dst,stencil)

	#result = cv2.bitwise_and(result, img)

	plt.imshow(result)
	plt.savefig('outline_regions.png')
	plt.imshow(regions)
	plt.savefig('regions.png')
	#plt.show()
	plt.close()

if __name__ == '__main__':
	main()
