# DESCRIPTION: creates the mask needed for processing

import resolution
import settings
from math import cos, sin, tan, pi
import numpy as np
import cv2 as cv2


# calculate the outer point of the shadow band position required for drawing
# the shadowband line. the formula of a circle is used: x=r*cos(t),y=r*sin(t)
def calculate_band_position(theta):
    # r_inner defines how many pixels from the center
    # the shadowband should be drawn
    # r_outer-r_inner is the line length

    x_inner = int(resolution.x / 2 + settings.r_inner * cos(theta))
    y_inner = int(resolution.y / 2 + settings.r_inner * sin(-theta))
    x_outer = int(resolution.x / 2 + settings.r_outer * cos(theta))
    y_outer = int(resolution.y / 2 + settings.r_outer * sin(-theta))

    return x_inner, y_inner, x_outer, y_outer


def create(img, azimuth):
    mask = np.zeros(img.shape, dtype="uint8")

    # HEMISPHERE
    # draw a white circle on the mask
    cv2.circle(mask, (int(resolution.x / 2), int(resolution.y / 2)), settings.radius_circle, settings.white, -1)

    # SHADOWBAND
    # first calculate the position of the shadow band
    # this is based on angle theta, this angle should directly be linked
    # to sun position
    # angle theta is given as "azimuth" in the properties file
    # this is the angle from the north=0, thus I need to add this to my
    # calculations as I calculate from east=0
    # thus, azimuth angle of 140degrees is ESE in the morning
    azimuth_degrees_east = azimuth - 90
    theta = -azimuth_degrees_east * pi / 180
    x_inner, y_inner, x_outer, y_outer = calculate_band_position(theta)

    # draw a black line on the mask
    cv2.line(mask, (x_inner, y_inner), (x_outer, y_outer), (0, 0, 0), 35)

    # ARM + CAMERA
    cv2.rectangle(mask, (141, 190), (154, 153), (0, 0, 0), -1)
    cv2.rectangle(mask, (145, 154), (152, 91), (0, 0, 0), -1)
    cv2.rectangle(mask, (int(resolution.x / 2), 91), (152, 26), (0, 0, 0), -1)

    return mask
