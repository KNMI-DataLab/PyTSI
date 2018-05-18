# DESCRIPTION: subdivides the iamge into four regions. these regions are used
#              to carry out horizon/sun area corrections

from myimports import *
import cv2 as cv2
import scipy as scipy
from math import cos,sin,sqrt,tan,pi
import numpy as np
import sys as sys
import matplotlib.pyplot as plt
from tqdm import tqdm
import gzip
import os

# outer circle
def largeCircle(radiusCircle):

	cv2.circle(regions,  (int(int(resolution.x/2)),int(int(resolution.y/2))), radiusCircle, (255,0,0), -1)
	cv2.circle(labels,   (int(int(resolution.x/2)),int(int(resolution.y/2))), radiusCircle, 1, -1)
	cv2.circle(outlines, (int(int(resolution.x/2)),int(int(resolution.y/2))), radiusCircle, (255,0,0), outlineThickness)

# horizon area polygon
def drawHorizonArea(widthHorizonAreaDegrees, azimuth):
	global theta, horizonArea
	# angle from the east in stead of north
	azimuthFromEast = azimuth - 90
	# distance of the three of the four points from the center
	r = int(resolution.x/2)
	# angle from degrees to radians
	theta = azimuthFromEast * pi / 180
	# horizon width from degrees to radians
	width = widthHorizonAreaDegrees * pi / 180
	# four points at vertices of polygon
	p1 = [int(int(resolution.x/2)), int(int(resolution.y/2))]
	p2 = [int(int(resolution.x/2)) + r * cos(theta-width), int(int(resolution.y/2)) + r * sin(theta-width)]
	p3 = [int(int(resolution.x/2)) + r * cos(theta), int(int(resolution.y/2)) + r * sin(theta)]
	p4 = [int(int(resolution.x/2)) + r * cos(theta+width), int(int(resolution.y/2)) + r * sin(theta+width)]
	horizonArea = np.array([p1,p2,p3,p4],dtype = int)
	# draw the polygon
	cv2.fillConvexPoly(regions, horizonArea, color=(0,255,255))
	cv2.fillConvexPoly(labels, horizonArea, color=2)
	cv2.fillConvexPoly(outlines, horizonArea, color=(0,0,0))
	cv2.polylines(outlines, [horizonArea], True, (0,255,255), outlineThickness)

# inner circle
def innerCircle(radiusInnerCircle):
	cv2.circle(regions, (int(int(resolution.x/2)),int(int(resolution.y/2))), radiusInnerCircle, (0,255,0), -1)
	cv2.circle(labels, (int(int(resolution.x/2)),int(int(resolution.y/2))), radiusInnerCircle, 3, -1)
	cv2.circle(outlines, (int(int(resolution.x/2)),int(int(resolution.y/2))), radiusInnerCircle, (0,0,0), -1)
	cv2.circle(outlines, (int(int(resolution.x/2)),int(int(resolution.y/2))), radiusInnerCircle, (0,255,0), outlineThickness)

# sun circle area (circular)
def sunCircle(radiusSunCircle, radiusMirror, altitude):
	# altitude from degrees to radians
	altitudeRadians = altitude * pi /180
	a = -0.23
	b = -tan(altitudeRadians)
	c = 1.25
	d = b**2 - 4 * a * c
	r = radiusMirror * (-b - sqrt(d)) / (2 * a) / 2
	# x and y position of the sun
	xSun = int(int(resolution.x/2) + r * cos (theta))
	ySun = int(int(resolution.y/2) + r * sin (theta))
	# draw the circle
	cv2.circle(regions, (xSun,ySun), radiusSunCircle, (255,255,0), -1)
	cv2.circle(labels, (xSun,ySun), radiusSunCircle, 4, -1)
	cv2.circle(outlines, (xSun,ySun), radiusSunCircle, (0,0,0), -1)
	cv2.circle(outlines, (xSun,ySun), radiusSunCircle, (255,255,0), outlineThickness)

# the stencil is used to mask the outside of the circle
def createStencil(radiusCircle):
	cv2.circle(stencil, (int(int(resolution.x/2)), int(int(resolution.y/2))), radiusCircle, (255,255,255), -1)
	cv2.circle(stencilLabels, (int(int(resolution.x/2)), int(int(resolution.y/2))), radiusCircle, 1, -1)

# combine the stencil with arrays to mask them
def outerCircle():
	global regions, labels, outlines
	regions = cv2.bitwise_and(regions,stencil)
	labels = cv2.bitwise_and(labels,labels,mask=stencilLabels)
	outlines = cv2.bitwise_and(outlines,stencil)

# overlay outlines on image by converting to b/w and performing several operations
# got this from a website
def overlayOutlinesOnImage(img,outlines):
	global imageWithOutlines
	# create mask of outlines and create inverse mask
	img2gray = cv2.cvtColor(outlines,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)

	# black out area of outlines
	img_bg = cv2.bitwise_and(img[0:resolution.y,0:resolution.x], img[0:resolution.y,0:resolution.x], mask = mask_inv)

	# take only region of outlines from outlines image
	outlines_fg = cv2.bitwise_and(outlines, outlines, mask = mask)

	dst = cv2.add(img_bg,outlines_fg)

	imageWithOutlines = cv2. bitwise_and(dst,stencil)

# camera and camera arm
def drawArm():
	cv2.rectangle(regions, (141,190), (154,153), (0,0,0), -1)
	cv2.rectangle(regions, (145,154), (152,91) , (0,0,0), -1)
	cv2.rectangle(regions, (int(resolution.x/2),91) , (152,26) , (0,0,0), -1)
	cv2.rectangle(labels, (141,190), (154,153), 0, -1)
	cv2.rectangle(labels, (145,154), (152,91) , 0, -1)
	cv2.rectangle(labels, (int(resolution.x/2),91) , (152,26) , 0, -1)
	cv2.rectangle(imageWithOutlines, (141,190), (154,153), (0,0,0), -1)
	cv2.rectangle(imageWithOutlines, (145,154), (152,91) , (0,0,0), -1)
	cv2.rectangle(imageWithOutlines, (int(resolution.x/2),91) , (152,26) , (0,0,0), -1)

# draw the shadowband
def drawBand(bandThickness):
	rInner = 40
	rOuter = 140

	xInner = int(resolution.x / 2 + rInner * cos(theta))
	yInner = int(resolution.y / 2 + rInner * sin(theta))
	xOuter = int(resolution.x / 2 + rOuter * cos(theta))
	yOuter = int(resolution.y / 2 + rOuter * sin(theta))
	cv2.line(regions, (xInner,yInner), (xOuter,yOuter), (0,0,0), bandThickness)
	cv2.line(labels, (xInner,yInner), (xOuter,yOuter), 0, bandThickness)
	cv2.line(imageWithOutlines, (xInner,yInner), (xOuter,yOuter), 0, bandThickness)

def createRegions(img, imgTSI, azimuth, altitude, filename):
	# variable assignment
	global regions, stencil, labels, outlines, stencilLabels
	global outlineThickness
	labels = np.zeros((resolution.y,resolution.x))
	regions = np.zeros((resolution.y,resolution.x,resolution.nColors), dtype="uint8")
	outlines = np.zeros((resolution.y,resolution.x,resolution.nColors), dtype="uint8")
	stencil = np.zeros(regions.shape, dtype="uint8")
	stencilLabels = np.zeros(labels.shape, dtype="uint8")
	radiusSunCircle = 40
	radiusInnerCircle = 80
	radiusCircle = 130
	radiusMirror = 140
	outlineThickness = 3
	bandThickness = 35
	widthHorizonAreaDegrees = 50
	# convert from BGR -> RGB
	# conversion needs to be centralized in one place.
	img = img[...,::-1]

	# drawing the shapes on arrays
	largeCircle(radiusCircle)
	drawHorizonArea(widthHorizonAreaDegrees, azimuth)
	innerCircle(radiusInnerCircle)
	sunCircle(radiusSunCircle, radiusMirror, altitude)
	createStencil(radiusCircle)
	outerCircle()
	overlayOutlinesOnImage(img,outlines)
	drawArm()
	drawBand(bandThickness)

	return regions, outlines, labels, stencil, imageWithOutlines

def getAltitude(lines):
	for line in lines:
		if line.startswith('tsi.image.solar.altitude='):
			# extract altitude from the correct line
			tmp1, tmp2 = line.split('=')
			altitudeStr, tmp1 = tmp2.split('\n')

			# convert string to float
			altitude = float(altitudeStr)
		else:
			pass

	return altitude

def getAzimuth(lines):
	for line in lines:
		if line.startswith('tsi.image.solar.azimuth='):
			# extract azimuth from the correct line
			tmp1, tmp2 = line.split('=')
			azimuthStr, tmp1 = tmp2.split('\n')

			# convert string to float
			azimuth = float(azimuthStr)
		else:
			pass

	return azimuth
