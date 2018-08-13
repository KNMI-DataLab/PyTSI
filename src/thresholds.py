import numpy as np
import settings
from math import log10
import ratio
import skimage.filters
import resolution
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans
import scipy


def fixed():
    """Get the fixed thresholds from the settings file

    Returns:
        tuple: the fixed thresholds
    """
    # TODO: this is unnecessary
    fixed_sunny_threshold = settings.fixed_sunny_threshold
    fixed_thin_threshold = settings.fixed_thin_threshold

    if settings.use_single_threshold:
        return fixed_sunny_threshold, fixed_sunny_threshold
    else:
        return fixed_sunny_threshold, fixed_thin_threshold


def min_cross_entropy(data):
    """Minimum cross entropy algorithm to determine the minimum of a histogram

    Args:
        data (float): the image data (e.g. blue/red ratio) to be used in the histogram

    Returns:
        float: the MCE threshold
    """
    # create the histogram and determine length
    hist, bins = np.histogram(data, settings.nbins_hybrid)
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
        # print('histogram data:', hist)
        # print('ERROR threshold (', threshold, ') smaller or equal to 0')
        # print('minimum is in bin:',np.argmin(thresholdList))
        # print('bins:',bins)
        # print('******************************************************')
        # plt.hist(data, settings.nbins_hybrid)
        # plt.show()
        # raise Exception('Error in threshold')
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
    blue_red_ratio_1d_nz_norm = np.divide(blue_red_ratio_1d_nz - 1, blue_red_ratio_1d_nz + 1)

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

    threshold = threshold_mce = threshold_otsu = threshold_kmeans = 0

    # decide which thresholding needs to be used
    if st_dev <= settings.deviation_threshold:
        # fixed thresholding
        threshold_mce = threshold_otsu = threshold_kmeans = settings.fixed_threshold
    else:
        # MCE thresholding
        threshold_mce = min_cross_entropy(blue_red_ratio_norm_1d_nz)
        # Otsu thresholding
        #! threshold_otsu = otsu(blue_red_ratio_norm_1d_nz)
        # k-means thresholding
        threshold_kmeans = kmeans(blue_red_ratio_norm_1d_nz)

    return blue_red_ratio_norm_1d_nz, blue_red_ratio_norm_nz, st_dev, threshold_mce, threshold_otsu, threshold_kmeans


def kmeans(blue_red_ratio_norm_1d_nz):
    """calculate the threshold using k-means"""
    # sort and reshape the data
    blue_red_ratio_norm_1d_nz.sort()
    data = blue_red_ratio_norm_1d_nz.reshape(-1, 1)

    plt.figure(figsize=(7,4))
    plt.hist(data, bins=35, density=True, color='lightgrey', edgecolor='black', alpha=0.5)
    plt.xlim((-0.5, 0.5))

    # apply the kmeans
    result = KMeans(n_clusters=2, random_state=0).fit(data)

    # find the clusters
    clusters = result.cluster_centers_

    plt.axvline(min(clusters), color='tab:blue', label='k-means clusters', linewidth=4, linestyle='--')
    plt.axvline(max(clusters), color='tab:blue', linewidth=4, linestyle='--')

    # find the closest indices of the cluster centers
    arg1 = (np.abs(blue_red_ratio_norm_1d_nz - min(clusters))).argmin()
    arg2 = (np.abs(blue_red_ratio_norm_1d_nz - max(clusters))).argmin()

    data_to_plot = blue_red_ratio_norm_1d_nz[arg1:arg2]

    # calculate the threshold
    # threshold = sum(clusters)/len(result.cluster_centers_)
    threshold = min_cross_entropy(data_to_plot)

    plt.axvline(threshold, color='tab:orange', label='MCE threshold', linewidth=4, linestyle='--')

    plt.legend()
    plt.xlabel('Normalized R/B')
    plt.ylabel('Normalized frequency')
    plt.tight_layout()
    plt.savefig('/nobackup/users/mos/results/kmeans_mce_histogram.eps')
    plt.show()
    plt.close()

    return threshold


def otsu(blue_red_ratio_norm_1d_nz):
    """Calculate the threshold using the Otsu algorithm"""
    threshold = skimage.filters.threshold_otsu(blue_red_ratio_norm_1d_nz, nbins=settings.nbins_hybrid)

    return threshold


def otsu_for_crops(img, filename_no_ext):
    resolution.get_resolution(img)

    # r_rb = ratio.red_blue_v2(img)
    r_br = ratio.blue_red(img)

    # normalize the data
    r_br_normed = (r_br -1) / (r_br + 1)
    # r_br_normed = sklearn.preprocessing.normalize(r_br, norm='l1')
    # r_br_normed = r_br - np.min(r_br) / np.max(r_br) - np.min(r_br)

    # if np.std(r_br_normed.flatten()) < 0.045:
    # if np.std(r_br_normed.flatten()) < 0.08:
    #     thresh = 0.1
    # else:
    #     thresh = skimage.filters.threshold_otsu(r_br_normed, nbins=256)

    thresh = skimage.filters.threshold_otsu(r_br_normed, nbins=256)

    binary_otsu = r_br_normed > thresh

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10,5))

    ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    ax2.imshow(binary_otsu, cmap='Blues')
    ax3.hist(r_br_normed.flatten(), bins=50)
    # ax3.set_xlim(-1, 1)
    fig.suptitle('stdev='+str(np.std(r_br_normed.flatten())))
    plt.savefig(settings.results_folder + settings.data_type + '/thresholding_tests/' + filename_no_ext + '.png')
    plt.close()
