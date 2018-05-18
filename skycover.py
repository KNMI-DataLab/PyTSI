import resolution
import numpy as np
import math

def fixed(red_blue_ratio, fixed_sunny_threshold, fixed_thin_threshold):
    # calculate number of sunny/thin and opaque pixels
    sunny_pixels = np.sum(np.logical_and(red_blue_ratio > 0.01, red_blue_ratio <= fixed_sunny_threshold))
    thin_pixels = np.sum(np.logical_and(red_blue_ratio > 0.01,
                                       np.logical_and(red_blue_ratio > fixed_sunny_threshold, red_blue_ratio <= fixed_thin_threshold)))
    opaque_pixels = np.sum(np.logical_and(red_blue_ratio > 0.01, red_blue_ratio > fixed_thin_threshold))

    cloudy_pixels = thin_pixels + opaque_pixels

    thin_sky_cover = thin_pixels / (sunny_pixels + cloudy_pixels)
    opaque_sky_cover = opaque_pixels / (sunny_pixels + cloudy_pixels)
    fractional_sky_cover = thin_sky_cover + opaque_sky_cover

    # check for NaN and odd values
    if math.isnan(np.min(red_blue_ratio)):
        print('R/B ratio NaN found')
        sys.exit('')

    if sunny_pixels + cloudy_pixels > resolution.y * resolution.x:
        print('Total amount of non-mask pixels error: ', sunny_pixels, cloudy_pixels)
        sys.exit('')

    return thin_sky_cover, opaque_sky_cover, fractional_sky_cover


def hybrid(flatNormalizedRatioBRNoZeros, hybrid_threshold):
    sun_pixels = np.sum(flatNormalizedRatioBRNoZeros > hybrid_threshold)
    cloud_pixels = np.sum(flatNormalizedRatioBRNoZeros < hybrid_threshold)

    fractional_sky_cover = cloud_pixels / (sun_pixels + cloud_pixels)

    return fractional_sky_cover
