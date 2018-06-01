import numpy as np
import settings
from math import log10, sqrt
from skimage.feature import greycomatrix
import color_bands
import resolution


# TODO: mask GLCM matrices properly with NumPy
# TODO: color_bands.extract and scaler calc is called two times separately in fucntions, can i avoid this?

def calculate_greymatrix(img):
    """Calculate the Grey Level Co-occurence Matrix (GLCM)

    Args:
        img (int): masked RGB image (NumPy array)

    Returns:
        float: grey level co-occurrence matrix
    """
    # set the number of grey levels used in the GLCM calculation
    scaler = int(settings.max_color_value / settings.grey_levels)

    # extract the individual color bands as greyscale
    blue_band, green_band, red_band = color_bands.extract(scaler, img)

    blue_band = blue_band.astype(int)
    # Grey Level Co-occurrence Matrices (GLCM)

    GLCM = greycomatrix(blue_band, [settings.dx, settings.dy],
                        [0, np.pi / 2, np.pi, 3 * np.pi / 2], levels=settings.grey_levels)

    # convert 4D array to 2D array
    GLCM2D = GLCM[:, :, 0, 0]

    return GLCM2D


def textural_features(img):
    """Determine statistical features from grey level co-occurrence matrix

    Args:
         img (int): masked RGB image (NumPy array)

    Returns:
        tuple: energy, entropy, contrast, homogeneity
    """

    GLCM = calculate_greymatrix(img)

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


def spectral_features(img):
    """Calculate spectral features from image

    Args:
        img: input image

    Returns:
        tuple: spectral features
    """
    # set the number of grey levels used in the GLCM calculation
    scaler = int(settings.max_color_value / settings.grey_levels)

    # extract the individual color bands as greyscale
    blue_band, green_band, red_band = color_bands.extract(scaler, img)

    n = settings.x * settings.y
    mean_r = np.sum(red_band) / n
    mean_g = np.sum(green_band) / n
    mean_b = np.sum(blue_band) / n
    st_dev = sqrt(np.sum(np.square(np.subtract(blue_band, mean_b))) / (n - 1))
    skewness = np.sum(np.power(np.divide(np.subtract(blue_band, mean_b), st_dev), 3)) / n
    diff_rg = mean_r - mean_g
    diff_rb = mean_r - mean_b
    diff_gb = mean_g - mean_b

    return mean_r, mean_g, mean_b, st_dev, skewness, diff_rg, diff_rb, diff_gb
