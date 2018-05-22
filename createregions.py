# DESCRIPTION: subdivides the iamge into four regions. these regions are used
#              to carry out horizon/sun area corrections

import cv2 as cv2
from math import cos, sin, sqrt, tan, pi
import numpy as np
import resolution
import settings


# outer circle
def large_circle(regions, labels, outlines):
    cv2.circle(regions, (int(int(resolution.x / 2)), int(int(resolution.y / 2))), settings.radius_circle, settings.red, -1)
    cv2.circle(labels, (int(int(resolution.x / 2)), int(int(resolution.y / 2))), settings.radius_circle, 1, -1)
    cv2.circle(outlines, (int(int(resolution.x / 2)), int(int(resolution.y / 2))), settings.radius_circle, settings.red,
               settings.outline_thickness)

    return regions, labels, outlines


# horizon area polygon
def draw_horizon_area(azimuth, regions, labels, outlines):
    # angle from the east in stead of north
    azimuth_from_east = azimuth - 90
    # distance of the three of the four points from the center
    r = int(resolution.x / 2)
    # angle from degrees to radians
    theta = azimuth_from_east * pi / 180
    # horizon width from degrees to radians
    width = settings.width_horizon_area_degrees * pi / 180
    # four points at vertices of polygon
    p1 = [int(int(resolution.x / 2)), int(int(resolution.y / 2))]
    p2 = [int(int(resolution.x / 2)) + r * cos(theta - width), int(int(resolution.y / 2)) + r * sin(theta - width)]
    p3 = [int(int(resolution.x / 2)) + r * cos(theta), int(int(resolution.y / 2)) + r * sin(theta)]
    p4 = [int(int(resolution.x / 2)) + r * cos(theta + width), int(int(resolution.y / 2)) + r * sin(theta + width)]
    horizon_area = np.array([p1, p2, p3, p4], dtype=int)
    # draw the polygon
    cv2.fillConvexPoly(regions, horizon_area, color=settings.cyan)
    cv2.fillConvexPoly(labels, horizon_area, color=2)
    cv2.fillConvexPoly(outlines, horizon_area, color=settings.black)
    cv2.polylines(outlines, [horizon_area], True, settings.cyan, settings.outline_thickness)

    return regions, labels, outlines, theta


# inner circle
def inner_circle(regions, labels, outlines):
    cv2.circle(regions, (int(int(resolution.x / 2)), int(int(resolution.y / 2))), settings.radius_inner_circle, settings.green, -1)
    cv2.circle(labels, (int(int(resolution.x / 2)), int(int(resolution.y / 2))), settings.radius_inner_circle, 3, -1)
    cv2.circle(outlines, (int(int(resolution.x / 2)), int(int(resolution.y / 2))), settings.radius_inner_circle, (0, 0, 0), -1)
    cv2.circle(outlines, (int(int(resolution.x / 2)), int(int(resolution.y / 2))), settings.radius_inner_circle, settings.green,
               settings.outline_thickness)

    return regions, labels, outlines


# sun circle area (circular)
def sun_circle(altitude, regions, labels, outlines, theta):
    # altitude from degrees to radians
    altitude_radians = altitude * pi / 180
    a = -0.23
    b = -tan(altitude_radians)
    c = 1.25
    d = b ** 2 - 4 * a * c
    r = settings.radius_mirror * (-b - sqrt(d)) / (2 * a) / 2
    # x and y position of the sun
    x_sun = int(int(resolution.x / 2) + r * cos(theta))
    y_sun = int(int(resolution.y / 2) + r * sin(theta))
    # draw the circle
    cv2.circle(regions, (x_sun, y_sun), settings.radius_sun_circle, settings.yellow, -1)
    cv2.circle(labels, (x_sun, y_sun), settings.radius_sun_circle, 4, -1)
    cv2.circle(outlines, (x_sun, y_sun), settings.radius_sun_circle, (0, 0, 0), -1)
    cv2.circle(outlines, (x_sun, y_sun), settings.radius_sun_circle, settings.yellow, settings.outline_thickness)

    return regions, labels, outlines


# the stencil is used to mask the outside of the circle
def create_stencil(stencil, stencil_labels):
    cv2.circle(stencil, (int(int(resolution.x / 2)), int(int(resolution.y / 2))), settings.radius_circle, settings.white, -1)
    cv2.circle(stencil_labels, (int(int(resolution.x / 2)), int(int(resolution.y / 2))), settings.radius_circle, 1, -1)

    return stencil, stencil_labels


# combine the stencil with arrays to mask them
def outer_circle(regions, labels, outlines, stencil, stencil_labels):
    regions = cv2.bitwise_and(regions, stencil)
    labels = cv2.bitwise_and(labels, labels, mask=stencil_labels)
    outlines = cv2.bitwise_and(outlines, stencil)

    return regions, labels, outlines


# overlay outlines on image by converting to b/w and performing several operations
# got this from a website
def overlay_outlines_on_image(img, outlines, stencil):
    # create mask of outlines and create inverse mask
    img2gray = cv2.cvtColor(outlines, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, settings.max_color_value-1, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # black out area of outlines
    img_bg = cv2.bitwise_and(img[0:resolution.y, 0:resolution.x], img[0:resolution.y, 0:resolution.x], mask=mask_inv)

    # take only region of outlines from outlines image
    outlines_fg = cv2.bitwise_and(outlines, outlines, mask=mask)

    dst = cv2.add(img_bg, outlines_fg)

    image_with_outlines = cv2.bitwise_and(dst, stencil)

    return image_with_outlines


# camera and camera arm
def draw_arm(regions, labels, image_with_outlines):
    cv2.rectangle(regions, (141, 190), (154, 153), settings.black, -1)
    cv2.rectangle(regions, (145, 154), (152, 91), settings.black, -1)
    cv2.rectangle(regions, (int(resolution.x / 2), 91), (152, 26), settings.black, -1)
    cv2.rectangle(labels, (141, 190), (154, 153), 0, -1)
    cv2.rectangle(labels, (145, 154), (152, 91), 0, -1)
    cv2.rectangle(labels, (int(resolution.x / 2), 91), (152, 26), 0, -1)
    cv2.rectangle(image_with_outlines, (141, 190), (154, 153), settings.black, -1)
    cv2.rectangle(image_with_outlines, (145, 154), (152, 91), settings.black, -1)
    cv2.rectangle(image_with_outlines, (int(resolution.x / 2), 91), (152, 26), settings.black, -1)

    return regions, labels, image_with_outlines


# draw the shadowband
def draw_band(regions, labels, image_with_outlines, theta):
    x_inner = int(resolution.x / 2 + settings.r_inner * cos(theta))
    y_inner = int(resolution.y / 2 + settings.r_inner * sin(theta))
    x_outer = int(resolution.x / 2 + settings.r_outer * cos(theta))
    y_outer = int(resolution.y / 2 + settings.r_outer * sin(theta))
    cv2.line(regions, (x_inner, y_inner), (x_outer, y_outer), settings.black, settings.band_thickness)
    cv2.line(labels, (x_inner, y_inner), (x_outer, y_outer), 0, settings.band_thickness)
    cv2.line(image_with_outlines, (x_inner, y_inner), (x_outer, y_outer), 0, settings.band_thickness)

    return regions, labels, image_with_outlines


def create(img, azimuth, altitude):
    # variable assignment
    labels = np.zeros((resolution.y, resolution.x))
    regions = np.zeros((resolution.y, resolution.x, resolution.nColors), dtype="uint8")
    outlines = np.zeros((resolution.y, resolution.x, resolution.nColors), dtype="uint8")
    stencil = np.zeros(regions.shape, dtype="uint8")
    stencil_labels = np.zeros(labels.shape, dtype="uint8")
    # convert from BGR -> RGB
    # conversion needs to be centralized in one place.
    img = img[..., ::-1]

    # drawing the shapes on arrays
    regions, labels, outlines = large_circle(regions, labels, outlines)
    regions, labels, outlines, theta = draw_horizon_area(azimuth, regions, labels, outlines)
    regions, labels, outlines = inner_circle(regions, labels, outlines)
    regions, labels, outlines = sun_circle(altitude, regions, labels, outlines, theta)
    stencil, stencil_labels = create_stencil(stencil, stencil_labels)
    regions, labels, outlines = outer_circle(regions, labels, outlines, stencil, stencil_labels)
    image_with_outlines = overlay_outlines_on_image(img, outlines, stencil)
    regions, labels, image_with_outlines = draw_arm(regions, labels, image_with_outlines)
    regions, labels, image_with_outlines = draw_band(regions, labels, image_with_outlines, theta)

    return regions, outlines, labels, stencil, image_with_outlines
