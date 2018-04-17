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
import sys as sys
import matplotlib.pyplot as plt

# print options
np.set_printoptions(threshold=np.nan)

def largeCircle(radiusCircle):
	cv2.circle(regions, (int(xres/2),int(yres/2)), radiusCircle, (255,0,0), -1)
	cv2.circle(labels, (int(xres/2),int(yres/2)), radiusCircle, 1, -1)
	cv2.circle(outlines, (int(xres/2),int(yres/2)), radiusCircle, (255,0,0), outlineThickness)

def horizonArea(widthHorizonAreaDegrees):
	global theta, horizonArea
	azimuthFromEast = azimuth - 90
	r = xres/2
	theta = azimuthFromEast * pi / 180
	width = widthHorizonAreaDegrees * pi / 180
	# four points that comprise the poligon
	p1 = [int(xres/2), int(yres/2)]
	p2 = [int(xres/2) + r * cos(theta-width), int(yres/2) + r * sin(theta-width)]
	p3 = [int(xres/2) + r * cos(theta), int(yres/2) + r * sin(theta)]
	p4 = [int(xres/2) + r * cos(theta+width), int(yres/2) + r * sin(theta+width)]
	horizonArea = np.array([p1,p2,p3,p4],dtype = int)
	cv2.fillConvexPoly(regions, horizonArea, color=(0,255,255))
	cv2.fillConvexPoly(labels, horizonArea, color=2)
	cv2.fillConvexPoly(outlines, horizonArea, color=(0,0,0))
	cv2.polylines(outlines, [horizonArea], True, (0,255,255), outlineThickness)

def innerCircle(radiusInnerCircle):
	cv2.circle(regions, (int(xres/2),int(yres/2)), radiusInnerCircle, (0,255,0), -1)
	cv2.circle(labels, (int(xres/2),int(yres/2)), radiusInnerCircle, 3, -1)
	cv2.circle(outlines, (int(xres/2),int(yres/2)), radiusInnerCircle, (0,0,0), -1)
	cv2.circle(outlines, (int(xres/2),int(yres/2)), radiusInnerCircle, (0,255,0), outlineThickness)

def sunCircle(radiusSunCircle, radiusMirror):
	altitudeRadians = altitude * pi /180
	a = -0.23
	b = -tan(altitudeRadians)
	c = 1.25
	d = b**2 - 4 * a * c
	r = radiusMirror * (-b - sqrt(d)) / (2 * a) / 2
	xSun = int(xres/2 + r * cos (theta))
	ySun = int(yres/2 + r * sin (theta))
	cv2.circle(regions, (xSun,ySun), radiusSunCircle, (255,255,0), -1)
	cv2.circle(labels, (xSun,ySun), radiusSunCircle, 4, -1)
	cv2.circle(outlines, (xSun,ySun), radiusSunCircle, (0,0,0), -1)
	cv2.circle(outlines, (xSun,ySun), radiusSunCircle, (255,255,0), outlineThickness)

def createStencil(radiusCircle):
	cv2.circle(stencil, (int(xres/2), int(yres/2)), radiusCircle, (255,255,255), -1)
	cv2.circle(stencilLabels, (int(xres/2), int(yres/2)), radiusCircle, 1, -1)

def outerCircle():
	global regions, labels, outlines
	regions = cv2.bitwise_and(regions,stencil)
	labels = cv2.bitwise_and(labels,labels,mask=stencilLabels)
	outlines = cv2.bitwise_and(outlines,stencil)

def overlayOutlinesOnImage():
	global imageWithOutlines
	# create mask of outlines and create inverse mask
	img2gray = cv2.cvtColor(outlines,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)

	# black out area of outlines
	img_bg = cv2.bitwise_and(img[0:yres,0:xres], img[0:yres,0:xres], mask = mask_inv)

	# take only region of outlines from outlines image
	outlines_fg = cv2.bitwise_and(outlines, outlines, mask = mask)

	dst = cv2.add(img_bg,outlines_fg)

	imageWithOutlines = cv2. bitwise_and(dst,stencil)

def drawArm():
	cv2.rectangle(regions, (141,190), (154,153), (0,0,0), -1)
	cv2.rectangle(regions, (145,154), (152,91) , (0,0,0), -1)
	cv2.rectangle(regions, (144,91) , (152,26) , (0,0,0), -1)
	cv2.rectangle(labels, (141,190), (154,153), 0, -1)
	cv2.rectangle(labels, (145,154), (152,91) , 0, -1)
	cv2.rectangle(labels, (144,91) , (152,26) , 0, -1)
	cv2.rectangle(imageWithOutlines, (141,190), (154,153), (0,0,0), -1)
	cv2.rectangle(imageWithOutlines, (145,154), (152,91) , (0,0,0), -1)
	cv2.rectangle(imageWithOutlines, (144,91) , (152,26) , (0,0,0), -1)

def drawBand(bandThickness):
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
	cv2.line(regions, (xInner,yInner), (xOuter,yOuter), (0,0,0), bandThickness)
	cv2.line(labels, (xInner,yInner), (xOuter,yOuter), 0, bandThickness)
	cv2.line(imageWithOutlines, (xInner,yInner), (xOuter,yOuter), 0, bandThickness)

def createRegions(img):
	# variable assignment
	global regions, stencil, labels, outlines, stencilLabels
	global yres, xres
	global azimuth, altitude
	global outlineThickness
	yres, xres, nColors = img.shape
	labels = np.zeros((yres,xres))
	regions = np.zeros((yres,xres,nColors), dtype="uint8")
	outlines = np.zeros((yres,xres,nColors), dtype="uint8")
	stencil = np.zeros(regions.shape, dtype="uint8")
	stencilLabels = np.zeros(labels.shape, dtype="uint8")
	radiusSunCircle = 40
	radiusInnerCircle = 90
	radiusCircle = 130
	radiusMirror = 140
	azimuth = 66.868741228036
	altitude = 10.056278611719174
	outlineThickness = 3
	bandThickness = 35
	widthHorizonAreaDegrees = 50

	# drawing the shapes on arrays
	largeCircle(radiusCircle)
	horizonArea(widthHorizonAreaDegrees)
	innerCircle(radiusInnerCircle)
	sunCircle(radiusSunCircle, radiusMirror)
	createStencil(radiusCircle)
	outerCircle()
	overlayOutlinesOnImage()
	drawArm()
	drawBand(bandThickness)

	return regions, labels, outlines, stencil, stencilLabels

def saveOutputToFigures(regions,imageWithOutlines):
	fig, (ax1,ax2,ax3) = plt.subplots(1,3)
	ax1.set_adjustable('box-forced')
	ax2.set_adjustable('box-forced')
	ax3.set_adjustable('box-forced')

	ax1.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax1.set_title('Original image')
	ax1.imshow(img)

	ax2.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax2.set_title('Segments')
	ax2.imshow(regions)

	ax3.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax3.set_title('Segmented image')
	ax3.imshow(imageWithOutlines)

	plt.tight_layout()

	plt.savefig('segmented_image.png',bbox_inches='tight')
	plt.close()

def main():
	# read image
	global img
	img = cv2.imread('20170601044900.jpg')

	# convert image to RGB
	img = img[...,::-1]

	# create all the regions and outlines
	createRegions(img)

	saveOutputToFigures(regions,imageWithOutlines)

if __name__ == '__main__':
	main()
