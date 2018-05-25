# DESCRIPTION: calculates the Red/Blue ratio of every image pixel by dividing
#              the red by the blue band pixelwise while avoiding the mask

import numpy as np
import resolution


def red_blue(maskedImg):
    """Calculate the red/blue ratio per image pixel

    Args:
        maskedImg (int): masked image

    Returns:
        float: red/blue ratio per image pixel
    """
    red_blue_ratio = np.zeros([resolution.y, resolution.x])

    blue_band = maskedImg[:, :, 0].astype(int)
    red_band = maskedImg[:, :, 2].astype(int)

    # TODO improve this loop by replacing it with matrix operation, make sure it does not crash the code

    for i in range(0, resolution.y):
        for j in range(0, resolution.x):
            if blue_band[i, j] != 0:
                red_blue_ratio[i, j] = red_band[i, j] / blue_band[i, j]

    if np.average(red_blue_ratio) < 0 or np.average(red_blue_ratio) > 100:
        sys.exit('Unexpected average red_blue_ratio found')

    return red_blue_ratio
