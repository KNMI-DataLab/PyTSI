import numpy as np


def extract(scaler, masked_img):
    """Extract the red, green and blue bands from the masked image

    Args:
        scaler (int): Maximum number of color levels, used in GLCM matrix
        masked_img (int): The masked image

    Returns:
        tuple: Red, green and blue bands
    """

    blue_band = np.divide(masked_img[np.where(masked_img[:, :, 0] != 0)], scaler).astype(int)
    green_band = np.divide(masked_img[np.where(masked_img[:, :, 1] != 0)], scaler).astype(int)
    red_band = np.divide(masked_img[np.where(masked_img[:, :, 2] != 0)], scaler).astype(int)

    return blue_band, green_band, red_band
