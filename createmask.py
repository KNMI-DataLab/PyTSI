# DESCRIPTION: creates the mask needed for processing

from myimports import *
import scipy as scipy
from math import tan


# calculate the outer point of the shadow band position required for drawing
# the shadowband line. the formula of a circle is used: x=r*cos(t),y=r*sin(t)
def calculateBandPosition(theta):
    # rInner defines how many pixels from the center
    # the shadowband should be drawn
    # rOuter-rInner is the line length
    rInner = 40
    rOuter = 140

    #
    xInner = int(resolution.x / 2 + rInner * cos(theta))
    yInner = int(resolution.y / 2 + rInner * sin(-theta))
    xOuter = int(resolution.x / 2 + rOuter * cos(theta))
    yOuter = int(resolution.y / 2 + rOuter * sin(-theta))

    return xInner, yInner, xOuter, yOuter


# x,y location of the sun position
def calculateSunPosition(theta, altitude, radiusCircle):
    radiusMirror = 140
    altitudeRadians = (altitude) * pi / 180

    # method: (intersect between altitude line and parabola)
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
    d = b ** 2 - 4 * a * c
    r = radiusMirror * (-b - sqrt(d)) / (2 * a) / 2

    x = int(int(resolution.x / 2) + r * cos(theta))
    y = int(int(resolution.y / 2) + r * sin(-theta))

    return x, y


def createmask(img, azimuthDegrees, altitude):
    # define radius circle mask
    radiusCircle = 130

    mask = np.zeros(img.shape, dtype="uint8")

    # HEMISPHERE
    # draw a white circle on the mask
    cv2.circle(mask, (int(resolution.x / 2), int(resolution.y / 2)), radiusCircle, (255, 255, 255), -1)

    # SHADOWBAND
    # first calculate the position of the shadow band
    # this is based on angle theta, this angle should directly be linked
    # to sun position
    # angle theta is given as "azimuth" in the properties file
    # this is the angle from the north=0, thus I need to add this to my
    # calculations as I calculate from east=0
    # thus, azimuth angle of 140degrees is ESE in the morning
    azimuthDegreesEast = azimuthDegrees - 90
    theta = -azimuthDegreesEast * pi / 180
    xInner, yInner, xOuter, yOuter = calculateBandPosition(theta)

    # draw a black line on the mask
    cv2.line(mask, (xInner, yInner), (xOuter, yOuter), (0, 0, 0), 35)

    # ARM + CAMERA
    cv2.rectangle(mask, (141, 190), (154, 153), (0, 0, 0), -1)
    cv2.rectangle(mask, (145, 154), (152, 91), (0, 0, 0), -1)
    cv2.rectangle(mask, (int(resolution.x / 2), 91), (152, 26), (0, 0, 0), -1)

    return mask
