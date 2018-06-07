# DESCRIPTION: sets the fixed thresholds
import numpy as np
import settings
import sys
from math import log10
import ratio
import matplotlib.pyplot as plt


def fixed():
    """Get the fixed thresholds from the settings file

    Returns:
        tuple: the fixed thresholds
    """
    # TODO: this might be unnecessary
    fixed_sunny_threshold = settings.fixed_sunny_threshold
    fixed_thin_threshold = settings.fixed_thin_threshold

    if settings.use_single_threshold:
        return fixed_sunny_threshold, fixed_sunny_threshold
    else:
        return fixed_sunny_threshold, fixed_thin_threshold

def min_cross_entropy(data, nbins):
    """Minimum cross entropy algorithm to determine the minimum of a histogram

    Args:
        data (foat): the image data (e.g. blue/red ratio) to be used in the histogram
        nbins (int): number of histogram bins

    Returns:
        float: the MCE threshold
    """
    # create the histogram and determine length
    hist, bins = np.histogram(data, nbins)
    L = len(hist)

    thresholdList = []

    # catch zeros which cause error if not changed to one
    if hist[1] == 0:
        hist[1] = 1
    if hist[L - 2] == 0:
        hist[L - 2] = 1

    for iThreshold in range(2, L):
        m1 = 0
        m2 = 0
        mu1 = 0
        mu2 = 0

        for i in range(1, iThreshold):
            m1 += i * hist[i]
            mu1 += hist[i]

        for i in range(iThreshold, L):
            m2 += i * hist[i]
            mu2 += hist[i]

        mu1 = m1 / mu1
        mu2 = m2 / mu2

        thresholdList.append(-m1 * log10(mu1) - m2 * log10(mu2))

    # minimum of the list is the threshold
    threshold = bins[np.argmin(thresholdList)]

    # catch miscalculation
    if threshold <= 0:
        pass
        #print('histogram data:', hist)
        #print('ERROR threshold (', threshold, ') smaller or equal to 0')
        #print('minimum is in bin:',np.argmin(thresholdList))
        #print('bins:',bins)
        #print('******************************************************')
        #plt.hist(data, settings.nbins_hybrid)
        #plt.show()
        #raise Exception('Error in threshold')
    return threshold


def flatten_clean_array(img):
    """Convert 2D masked image to 1D flattened array to be used in MCE algorithm

    Args:
        img: masked image

    Returns:
        tuple: 1D (only nonzeros) and 2D array of normalized blue/red ratios
    """
    blue_red_ratio = ratio.blue_red(img)

    # all values equal to zero black outsides + Cabauw tower
    mask_inv = blue_red_ratio == 0

    # normalized B/R ratio
    blue_red_ratio_norm = np.divide(blue_red_ratio - 1, blue_red_ratio + 1)
    blue_red_ratio_norm[mask_inv] = settings.mask_value

    blue_red_ratio_1d = blue_red_ratio.flatten()
    blue_red_ratio_1d_nz = blue_red_ratio_1d[blue_red_ratio_1d > 0]
    blue_red_ratio_1d_nz_norm = np.divide(blue_red_ratio_1d_nz -1, blue_red_ratio_1d_nz + 1)

    # catch Nan
    if np.argwhere(np.isnan(blue_red_ratio_norm)).any():
        raise Exception('NaN found in B/R ratios')

    return blue_red_ratio_1d_nz_norm, blue_red_ratio_norm


def hybrid(img):
    """Decide between fixed or MCE thresholding as part of hybrid thresholding algorithm

    Args:
        img (int): masked image

    Returns:
        tuple: normalized 1D flattened masked red/blue ratio array, standard deviation of the image and hybrid threshold
    """
    blue_red_ratio_norm_1d_nz, blue_red_ratio_norm_nz = flatten_clean_array(img)

    # calculate standard deviation
    st_dev = np.std(blue_red_ratio_norm_1d_nz)

    # decide which thresholding needs to be used
    if st_dev <= settings.deviation_threshold:
        # fixed thresholding
        threshold = settings.fixed_threshold
    else:
        # MCE thresholding
        threshold = min_cross_entropy(blue_red_ratio_norm_1d_nz, settings.nbins_hybrid)

    return blue_red_ratio_norm_1d_nz, blue_red_ratio_norm_nz, st_dev, threshold
