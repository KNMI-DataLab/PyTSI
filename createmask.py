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
from myimports import *
from cv2show import cv2show
import scipy as scipy
from math import tan

# calculate the outer point of the shadow band position required for drawing 
# the shadowband line. the formula of a circle is used: x=r*cos(t),y=r*sin(t)
def calculateBandPosition(theta):
	# rInner defines how many pixels from the center 
	# the shadowband should be drawn
	# rOuter 
	rInner = 40
	rOuter = 140

	#for i in range (0,n):
	#theta=-i/(n-1)*3.1415
	xInner = int(settings.xres / 2 + rInner * cos(theta))
	yInner = int(settings.yres / 2 + rInner * sin(-theta))
	xOuter = int(settings.xres / 2 + rOuter * cos(theta))
	yOuter = int(settings.yres / 2 + rOuter * sin(-theta))

	return xInner,yInner,xOuter,yOuter

def calculateSunPosition(theta,altitude,radiusCircle):
	radiusMirror = 140
	altitudeRadians = (altitude) * pi / 180

	# the 1.2 scaler is implemented to accomodate for the 
	# hemispheric mirror not being perfectly round and thus
	# the tracking of the sun is a bit harder

	# method 1
	#r = radiusCircle*cos(altitudeRadians)

	# method 2
	#r = radiusCircle - altitude / 90 * radiusCircle * cos(altitudeRadians)

	# method 3 (paraboly approximation)
	#r = radiusCircle * sqrt( 1 - sin(altitudeRadians))

	# method 4 (slightly different parabola approximation)
	#r = radiusMirror * sqrt( 1 / 0.23 ) * ( 1 - sin(altitudeRadians)) / 2

	# method 5 (intersect between altitude line and parabola)
	# intersection between:
	# y1 = sin(alt)/cos(alt)x+0 (y=ax+b, linear line)
	# y2 = -0.23x**2+1 (parabola that describes the geometry of mirror)
	# the second order function that needs to be solved (y1=y2):
	# -0.23x**2-sin(alt)/cos(alt)x+1=0
	# solution x is the distance of the sun from the zenith in pixels
	# x = (-b + sqrt(b **2 - 4 * a * c))/(2*a)
	a = -0.23
	b = -tan(altitudeRadians)
	c = 1.25
	d = b**2 - 4 * a * c
	r = radiusMirror * (-b - sqrt(d)) / (2 * a) / 2

	x = int(settings.xres/2 + r * cos (theta))
	y = int(settings.yres/2 + r * sin (-theta))

	# x=int(xres/2+r*sin(phi)*cos(theta))
	# y=int(yres/2+r*sin(phi)*sin(-theta))

	return x,y

def createmask(img, azimuthDegrees, altitude):
	# calculate image properties (resolution of the image)
	# calculation doesn't work yet, setting manually
	#[xres,yres]=img.shape

	# define radius circle mask
	radiusCircle=120

	# create the mask
	mask = np.zeros(img.shape, dtype="uint8")

	# HEMISPHERE
	# draw a white circle on the mask
	# resolution of the image ( 352x288(x3) ) 
	cv2.circle(mask, (144,176), radiusCircle, (255,255,255), -1)

	# SHADOWBAND
	# first calculate the position of the shadow band
	# this is based on angle theta, this angle should directly be linked 
	# to sun position
	
	# angle theta is given as "azimuth" in the properties file
	# this is the angle from the north=0, thus I need to add this to my
	# calculations as I calculate from east=0
	# thus, azimuth angle of 140degrees is ESE in the morning
	# rain: 211.92586033556788
	# semi_clouds: 187.40266748658414
	# broken_clouds: 218.77307228422038
	# thin_clouds: 244.1381726946926
	azimuthDegreesEast = azimuthDegrees - 90
	theta = -azimuthDegreesEast * pi / 180
	xInner,yInner,xOuter,yOuter = calculateBandPosition(theta)

	# draw a black line on the mask 
	# cv2.line(mask, point1 (midpoint is 144,176), point2, color, line thickness (in pixels?))
	cv2.line(mask, (xInner,yInner), (xOuter,yOuter), (0,0,0), 35)

	# ARM
	# draw a black line on the mask
	#cv2.line(mask, (144,176), (144,0), (0,0,0), 17)
	cv2.rectangle(mask, (141,190), (154,153), (0,0,0), -1)
	cv2.rectangle(mask, (145,154), (152,91) , (0,0,0), -1)
	cv2.rectangle(mask, (144,91) , (152,26) , (0,0,0), -1)

	# CAMERA
	# option to draw a black square where the camera is

	# SUN
	xSun,ySun = calculateSunPosition(theta,altitude,radiusCircle)
	cv2.circle(mask, (xSun,ySun), 40, (0,0,0), -1)

	# display constructed mask
	#cv2.imshow('test',mask)

	return mask
