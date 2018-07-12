import numpy as np
import settings
import sys


def red_blue(img):
    """Calculate the red/blue ratio per image pixel

    Args:
        img (int): input image

    Returns:
        float: red/blue ratio per image pixel
    """
    red_blue_ratio = np.zeros([settings.y, settings.x])

    blue_band = img[:, :, 0].astype(int)
    red_band = img[:, :, 2].astype(int)

    # TODO improve this loop by replacing it with matrix operation, make sure it does not crash the code

    for i in range(0, settings.y):
        for j in range(0, settings.x):
            if blue_band[i, j] != 0:
                red_blue_ratio[i, j] = red_band[i, j] / blue_band[i, j]

    if np.average(red_blue_ratio) < 0 or np.average(red_blue_ratio) > 100:
        sys.exit('Unexpected average red_blue_ratio found')

    return red_blue_ratio


def red_blue_v2(img):
    """Second version (maybe a better one) of the v1 algorithm

    Args:
        img: input image

    Returns:
        float: red/blue ratio per image pixel
    """
    blue_band = img[:, :, 0]
    red_band = img[:, :, 2]

    # rule out zeros
    mask = np.logical_and(blue_band > 0, red_band > 0)

    if settings.data_type == settings.tsi_str:
        red_blue_ratio = np.zeros([settings.y, settings.x])
    else:
        red_blue_ratio = np.zeros([settings.x, settings.y])
    red_blue_ratio[mask] = np.divide(red_band[mask], blue_band[mask])

    return red_blue_ratio


def blue_red(img):
    """Calculate the blue/red ratio per image pixel

    Args:
        img: input image

    Returns:
        blue/red ratio per image pixel
    """
    blue_band = img[:, :, 0]
    red_band = img[:, :, 2]

    # rule out zeros
    mask = np.logical_and(blue_band > 0, red_band > 0)

    if settings.data_type == settings.tsi_str:
        blue_red_ratio = np.zeros([settings.y, settings.x])
    else:
        blue_red_ratio = np.zeros([settings.x, settings.y])
    blue_red_ratio[mask] = np.divide(blue_band[mask], red_band[mask])

    return blue_red_ratio
