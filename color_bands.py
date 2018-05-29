import numpy as np


def extract(scaler, img):
    """Extract the red, green and blue bands from the masked image

    Args:
        scaler (int): Maximum number of color levels, used in GLCM matrix
        img (int): The masked image

    Returns:
        tuple: Red, green and blue bands
    """

    print('mean blue is',np.mean(img[:,:,0]))

    blue_band = np.divide(img[np.where(img[:, :, 0] != 0)], scaler).astype(int)
    green_band = np.divide(img[np.where(img[:, :, 1] != 0)], scaler).astype(int)
    red_band = np.divide(img[np.where(img[:, :, 2] != 0)], scaler).astype(int)

    return blue_band, green_band, red_band
