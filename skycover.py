import settings
import numpy as np
import math


def fixed(red_blue_ratio, fixed_sunny_threshold, fixed_thin_threshold):
    """Calculate the fractional sky cover based on fixed thresholding.

    Args:
        red_blue_ratio (float): Pixel per pixel representation of the red/blue ratio
        fixed_sunny_threshold (float): clear sky/cloudy fixed threshold
        fixed_thin_threshold (float): thin/opaque fixed threshold

    Returns:
        tuple: thin sky cover, opaque sky cover and fractional sky cover
    """
    # TODO: replace red_blue ratio with masked numpy version to clean up code below this comment, similar to hybrid below
    # calculate number of sunny/thin and opaque pixels
    sunny_pixels = np.sum(np.logical_and(red_blue_ratio > 0.01, red_blue_ratio <= fixed_sunny_threshold))
    thin_pixels = np.sum(np.logical_and(red_blue_ratio > 0.01,
                                        np.logical_and(red_blue_ratio > fixed_sunny_threshold,
                                                       red_blue_ratio <= fixed_thin_threshold)))
    opaque_pixels = np.sum(np.logical_and(red_blue_ratio > 0.01, red_blue_ratio > fixed_thin_threshold))

    cloudy_pixels = thin_pixels + opaque_pixels

    thin_sky_cover = thin_pixels / (sunny_pixels + cloudy_pixels)
    opaque_sky_cover = opaque_pixels / (sunny_pixels + cloudy_pixels)
    fractional_sky_cover = thin_sky_cover + opaque_sky_cover

    # check for NaN and odd values
    if math.isnan(np.min(red_blue_ratio)):
        print('R/B ratio NaN found')
        sys.exit('')

    if sunny_pixels + cloudy_pixels > settings.y * settings.x:
        print('Total amount of non-mask pixels error: ', sunny_pixels, cloudy_pixels)
        sys.exit('')

    return thin_sky_cover, opaque_sky_cover, fractional_sky_cover


def hybrid(ratioBR_norm_1d_nz, hybrid_threshold):
    """Calculate the fractional sky cover based on hybrid thresholding.

    Args:
        ratioBR_norm_1d_nz (float): normalized, masked, flattened red/blue ratio
        hybrid_threshold (float): clear sky/cloud threshold determined by the hybrid algorithm

    Returns:
        float: fractional sky cover as determined by the hybrid thresholding algorithm
    """
    sun_pixels = np.sum(ratioBR_norm_1d_nz > hybrid_threshold)
    cloud_pixels = np.sum(ratioBR_norm_1d_nz < hybrid_threshold)

    fractional_sky_cover = cloud_pixels / (sun_pixels + cloud_pixels)

    return fractional_sky_cover
