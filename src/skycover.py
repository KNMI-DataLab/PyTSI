import settings
import numpy as np
import math


def fixed(red_blue_ratio, fixed_sunny_threshold, fixed_thin_threshold):
    """Calculate the fractional sky cover based on fixed thresholding.

    Args:
        red_blue_ratio: Pixel per pixel representation of the red/blue ratio
        fixed_sunny_threshold (float): clear sky/cloudy fixed threshold
        fixed_thin_threshold (float): thin/opaque fixed threshold

    Returns:
        tuple: thin sky cover, opaque sky cover and fractional sky cover
    """
    # TODO: replace red_blue ratio with masked numpy version to clean up code below this comment, similar to hybrid below
    # calculate number of sunny/thin and opaque pixels
    clear_sky = np.sum(np.logical_and(red_blue_ratio > 0.01, red_blue_ratio <= fixed_sunny_threshold))
    thin = np.sum(np.logical_and(red_blue_ratio > 0.01,
                                        np.logical_and(red_blue_ratio > fixed_sunny_threshold,
                                                       red_blue_ratio <= fixed_thin_threshold)))
    opaque = np.sum(np.logical_and(red_blue_ratio > 0.01, red_blue_ratio > fixed_thin_threshold))

    cloud = thin + opaque

    cloud_cover_thin = thin / (clear_sky + cloud)
    cloud_cover_opaque = opaque / (clear_sky + cloud)
    cloud_cover_total = cloud_cover_thin + cloud_cover_opaque

    # check for NaN and odd values
    if math.isnan(np.min(red_blue_ratio)):
        raise Exception('R/B ratio NaN found')

    if clear_sky + cloud > settings.y * settings.x:
        raise Exception('Total amount of non-mask pixels error: ', clear_sky, cloud)

    return cloud_cover_thin, cloud_cover_opaque, cloud_cover_total


def hybrid(ratioBR_norm_1d_nz, hybrid_threshold):
    """Calculate the fractional sky cover based on hybrid thresholding.

    Args:
        ratioBR_norm_1d_nz: normalized, masked, flattened red/blue ratio
        hybrid_threshold (float): clear sky/cloud threshold determined by the hybrid algorithm

    Returns:
        float: fractional sky cover as determined by the hybrid thresholding algorithm
    """

    clear_sky = np.sum(ratioBR_norm_1d_nz > hybrid_threshold)
    cloud = np.sum(ratioBR_norm_1d_nz < hybrid_threshold)

    cloud_cover_total = cloud / (clear_sky + cloud)

    return cloud_cover_total
