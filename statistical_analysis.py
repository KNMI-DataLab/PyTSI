# DESCRIPTION: calculates various statistical properties of the image.
#              the statistical features provide information about the type
#              of cloud (texture). these properties are used in the
#              machine learning algorithm to examine accuracy

import numpy as np
import settings
from math import log10
from skimage.feature import greycomatrix
import color_bands


def work(maskedImg):
    # set the number of grey levels used in the GLCM calculation
    scaler = int(settings.max_color_value / settings.grey_levels)

    # extract the individual color bands as greyscale
    blue_band, green_band, red_band = color_bands.extract(scaler, maskedImg)

    blue_band = blue_band.astype(int)
    # Grey Level Co-occurrence Matrices (GLCM)

    GLCM = greycomatrix(blue_band, [settings.dx, settings.dy],
                        [0, np.pi / 2, np.pi, 3 * np.pi / 2], levels=settings.grey_levels)

    # convert 4D array to 2D array
    GLCM2D = GLCM[:, :, 0, 0]

    energy = entropy = contrast = homogeneity = 0

    for i in range(0, settings.grey_levels):
        for j in range(0, settings.grey_levels):
            if GLCM2D[i, j] != 0:
                # Energy (B)
                energy += np.power(GLCM2D[i, j], 2)
                # Entropy (B)
                entropy += GLCM2D[i, j] * log10(GLCM2D[i, j])
                # Contrast (B)
                contrast += GLCM2D[i, j] * (i - j) ** 2
                # Homogeneity (B)
                homogeneity += GLCM2D[i, j] / (1 + abs(i - j))
            else:
                pass

    return energy, entropy, contrast, homogeneity
