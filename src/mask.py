import settings
from math import cos, sin, pi
import numpy as np
import cv2 as cv2


def calculate_band_position(theta):
    """Calculate the inner and outer position of the shadow band, required for drawing the shadow band mask line.

    The formula of a circle is used: :math:`x = r \\cos{\\theta} \wedge y = r \\sin{\\theta}`.

    Args:
       theta (float): Azimuth of the sun with respect to the East. Normally, azimuth is measured from the North.
       However, to simplify calculations, the east was used.

    Returns:
       tuple: X and y locations of the inner and outer points of the shadow band
    """

    x_inner = int(settings.x / 2 + settings.r_inner * cos(theta))
    y_inner = int(settings.y / 2 + settings.r_inner * sin(-theta))
    x_outer = int(settings.x / 2 + settings.r_outer * cos(theta))
    y_outer = int(settings.y / 2 + settings.r_outer * sin(-theta))

    return x_inner, y_inner, x_outer, y_outer


def create(img, azimuth):
    """Create the mask using the original image and the azimuth.

    The mask consists of three parts:

    * The circle bordering the hemispherical mirror.
    * The shadow band.
    * The camera and camera arm.

    Args:
        img: Image in NumPy format
        azimuth (float): Azimuth of the sun, taken from the properties file

    Returns:
        int: The masked image of shape (x_resolution,y_resolution,3) for an RGB image
    """
    mask_array = np.zeros(img.shape, dtype="uint8")

    # HEMISPHERE
    # draw a white circle on the mask
    cv2.circle(mask_array, (int(settings.x / 2), int(settings.y / 2)), settings.radius_circle, settings.white, -1)

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
    cv2.line(mask_array, (x_inner, y_inner), (x_outer, y_outer), settings.black, 35)

    # ARM + CAMERA
    cv2.rectangle(mask_array, (141, 190), (154, 153), settings.black, -1)
    cv2.rectangle(mask_array, (145, 154), (152, 91), settings.black, -1)
    cv2.rectangle(mask_array, (int(settings.x / 2), 91), (152, 26), settings.black, -1)

    return mask_array


def apply(img, mask_array):
    """Apply mask to image

    Args:
        img: image to be masked
        mask_array: array of masking values

    Returns:
        masked image
    """
    masked_img = cv2.bitwise_and(img, mask_array)

    return masked_img
