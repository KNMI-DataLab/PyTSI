# DESCRIPTION: calculates various statistical properties of the image.
#              the statistical features provide information about the type
#              of cloud (texture). these properties are used in the
#              machine learning algorithm to examine accuracy

import numpy as np
import settings
from math import log10
from skimage.feature import greycomatrix
import color_bands


# TODO: mask GLCM matrices properly with NumPy

def calculate_greymatrix(masked_img):
    """Calculate the Grey Level Co-occurence Matrix (GLCM)

    Args:
        masked_img (int): masked RGB image (NumPy array)

    Returns:
        float: grey level co-occurrence matrix
    """
    # set the number of grey levels used in the GLCM calculation
    scaler = int(settings.max_color_value / settings.grey_levels)

    # extract the individual color bands as greyscale
    blue_band, green_band, red_band = color_bands.extract(scaler, masked_img)

    blue_band = blue_band.astype(int)
    # Grey Level Co-occurrence Matrices (GLCM)

    GLCM = greycomatrix(blue_band, [settings.dx, settings.dy],
                        [0, np.pi / 2, np.pi, 3 * np.pi / 2], levels=settings.grey_levels)

    # convert 4D array to 2D array
    GLCM2D = GLCM[:, :, 0, 0]

    return GLCM2D


def calculate_features(masked_img):
    """Determine statistical features from grey level co-occurrence matrix

    Args:
         masked_img (int): masked RGB image (NumPy array)

    Returns:
        tuple: energy, entropy, contrast, homogeneity
    """

    GLCM = calculate_greymatrix(masked_img)

    energy = entropy = contrast = homogeneity = 0

    for i in range(0, settings.grey_levels):
        for j in range(0, settings.grey_levels):
            if GLCM[i, j] != 0:
                # Energy (B)
                energy += np.power(GLCM[i, j], 2)
                # Entropy (B)
                entropy += GLCM[i, j] * log10(GLCM[i, j])
                # Contrast (B)
                contrast += GLCM[i, j] * (i - j) ** 2
                # Homogeneity (B)
                homogeneity += GLCM[i, j] / (1 + abs(i - j))
            else:
                pass

    return energy, entropy, contrast, homogeneity
