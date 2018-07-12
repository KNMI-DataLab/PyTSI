import numpy as np


def extract(scaler, img):
    """Extract the red, green and blue bands from the masked image

    Args:
        scaler (int): Maximum number of color levels, used in GLCM matrix
        img: input image

    Returns:
        tuple: Red, green and blue bands
    """

    blue_band = img[:,:,0]
    green_band = img[:,:,1]
    red_band = img[:,:,2]

    # rule out zeros
    mask = np.logical_and(blue_band > 0, np.logical_and(green_band > 0, red_band > 0))

    blue_band[mask] = blue_band[mask] / scaler
    green_band[mask] = green_band[mask] / scaler
    red_band[mask] = red_band[mask] / scaler

    return blue_band, green_band, red_band
