# extract the blue green and red bands

import numpy as np


def extract(scaler, maskedImg):
    # the arrays are set up in [y,x] orientation because the image
    # has some 'special' metadata which shows opposite resolution/geometry
    # view with: "$ identify -verbose data/20170419133000.jpg"

    blue_band = np.divide(maskedImg[np.where(maskedImg[:, :, 0] != 0)], scaler).astype(int)
    green_band = np.divide(maskedImg[np.where(maskedImg[:, :, 1] != 0)], scaler).astype(int)
    red_band = np.divide(maskedImg[np.where(maskedImg[:, :, 2] != 0)], scaler).astype(int)

    return blue_band, green_band, red_band
