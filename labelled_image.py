# DESCRIPTION: get amount of pixels in the four different areas to be used in
#              postprocessing corrections

import numpy as np


def calculate_pixels(labels, red_blue_ratio, threshold):
    # labels == 0 : mask
    # labels == 1 : outside circle
    # labels == 2 : horizon are
    # labels == 3 : inner circle
    # labels == 4 : sun circle

    # pixels sun circle
    sun_c = np.sum(((labels == 4) & (red_blue_ratio != 0) & (red_blue_ratio >= threshold)))
    sun_s = np.sum(((labels == 4) & (red_blue_ratio != 0) & (red_blue_ratio < threshold)))

    # pixels horizon area
    horizon_c = np.sum(((labels == 2) & (red_blue_ratio != 0) & (red_blue_ratio >= threshold)))
    horizon_s = np.sum(((labels == 2) & (red_blue_ratio != 0) & (red_blue_ratio < threshold)))

    # pixels inner circle
    inner_c = np.sum(((labels == 3) & (red_blue_ratio != 0) & (red_blue_ratio >= threshold)))
    inner_s = np.sum(((labels == 3) & (red_blue_ratio != 0) & (red_blue_ratio < threshold)))

    # pixels outside horizon area and inner circle
    outside_c = np.sum(((labels == 1) & (red_blue_ratio != 0) & (red_blue_ratio >= threshold)))
    outside_s = np.sum(((labels == 1) & (red_blue_ratio != 0) & (red_blue_ratio < threshold)))

    showNumberOfPixels = False
    if showNumberOfPixels:
        print('sun circle cloudy pixels', sun_c)
        print('sun circle sunny pixels ', sun_s)

        print('horizon area cloudy pixels', horizon_c)
        print('horizon area sunny pixels ', horizon_s)

        print('inner circle cloudy pixels', inner_c)
        print('inner circle sunny pixels ', inner_s)

        print('outside cloudy pixels', outside_c)
        print('outside sunny pixels ', outside_s)

    return outside_c, outside_s, horizon_c, horizon_s, inner_c, inner_s, sun_c, sun_s
