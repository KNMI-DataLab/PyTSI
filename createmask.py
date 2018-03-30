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

# calculate the outer point of the shadow band position required for drawing 
# the shadowband line. the formula of a circle is used: x=r*cos(t),y=r*sin(t)
def calculateBandPosition(xres,yres,theta):
	r=140

	#for i in range (0,n):
	#theta=-i/(n-1)*3.1415
	x=int(xres/2+r*cos(theta))
	y=int(yres/2+r*sin(-theta))

	return x,y

def calculateSunPosition(xres,yres,theta,altitude,radiusCircle):
	# the 1.2 scaler is implemented to accomodate for the 
	# hemispheric mirror not being perfectly round and thus
	# the tracking of the sun is a bit harder

	# method 1
	#altitudeRadians = (altitude*1.2) * pi / 180
	#r = radiusCircle*cos(altitudeRadians)

	# method 2
	#altitudeRadians = (altitude) * pi / 180
	#r = radiusCircle - altitude / 90 * radiusCircle * cos(altitudeRadians)

	# method 3
	altitudeRadians = (altitude) * pi / 180
	r = radiusCircle * 2 * sqrt( 1 - sin(altitudeRadians))

	phi = (altitude)*pi/180
	x = int(xres/2 + r * cos (theta))
	y = int(yres/2 + r * sin (-theta))
	# x=int(xres/2+r*sin(phi)*cos(theta))
	# y=int(yres/2+r*sin(phi)*sin(-theta))

	return x,y

def createmask(img, azimuthDegrees, altitude):
	# calculate image properties (resolution of the image)
	# calculation doesn't work yet, setting manually
	#[xres,yres]=img.shape
	xres=288
	yres=352

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
	azimuthDegreesEast=azimuthDegrees-90
	theta=-azimuthDegreesEast*pi/180
	xBand,yBand=calculateBandPosition(xres,yres,theta)

	# draw a black line on the mask 
	# cv2.line(mask, point1 (midpoint is 144,176), point2, color, line thickness (in pixels?))
	cv2.line(mask, (144,176), (xBand,yBand), (0,0,0), 35)

	# ARM
	# draw a black line on the mask
	cv2.line(mask, (144,176), (144,0), (0,0,0), 17)

	# CAMERA
	# option to draw a black square where the camera is

	# SUN
	xSun,ySun = calculateSunPosition(xres,yres,theta,altitude,radiusCircle)
	cv2.circle(mask, (xSun,ySun), 40, (0,0,0), -1)

	# display constructed mask
	#cv2.imshow('test',mask)

	return mask
