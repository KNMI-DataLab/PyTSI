import resolution
import numpy as np
import cv2
import settings


def outlines_over_image(img, outlines, stencil):
    """Overlay outlines on image by converting to BW and performing several other operations

    Args:
        img (int): image in NumPy format
        outlines (int): RGB array of the segment outlines
        stencil (int): stencil array in RGB format

    Returns:
        int: image with outlines as overlay
    """
    # TODO: there is now a duplicate that does the exact same thing both here and in createregions.py. FIX
    # create mask of outlines and create inverse mask
    img2gray = cv2.cvtColor(outlines, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # black out area of outlines
    img_bg = cv2.bitwise_and(img[0:resolution.y, 0:resolution.x], img[0:resolution.y, 0:resolution.x],
                             mask=mask_inv)

    # take only region of outlines from outlines image
    outlines_fg = cv2.bitwise_and(outlines, outlines, mask=mask)

    dst = cv2.add(img_bg, outlines_fg)

    img_with_outlines = cv2.bitwise_and(dst, stencil)

    return img_with_outlines


def fixed(img, outlines, stencil, fixed_sunny_threshold, fixed_thin_threshold):
    """Preprocess image to be compatible with :meth:`overlay.outlines_over_image` using fixed thresholding

    Args:
        img (int): image in NumPy format
        outlines (int): RGB array of the segment outlines
        stencil (int): stencil array in RGB format
        fixed_sunny_threshold (float): threshold for sun/cloud
        fixed_thin_threshold (float): threshold for thin/opaque cloud

    Returns:
        int: image with outlines
    """
    imgRGB = np.zeros(outlines.shape, np.uint8)

    # convert greyscale image to RGB image
    # sunny
    imgRGB[np.where(np.logical_and(img > 0, img <= fixed_sunny_threshold))] = settings.blue
    # thin
    imgRGB[np.where(np.logical_and(img >= fixed_sunny_threshold, img <= fixed_thin_threshold))] = settings.gray
    # opaque
    imgRGB[np.where(img >= fixed_thin_threshold)] = settings.white
    # mask
    imgRGB[np.where(img == 0)] = settings.black

    img_with_outlines = outlines_over_image(imgRGB, outlines, stencil)

    return img_with_outlines


def hybrid(img, outlines, stencil, threshold):
    """Preprocess image to be compatible with :meth:`overlay.outlines_over_image` using the hybrid threshold

    Args:
        img (int): image in NumPy format
        outlines (int): RGB array of the segment outlines
        stencil (int): stencil array in RGB format
        threshold (float): threshold for sun/cloud determined by HYbrid Thresholding Algorithm (HYTA)

    Returns:
        int: image with outlines
    """
    # TODO clean this up (a.k.a. remove double cacluations of ratio etc)
    imgRGB = np.zeros(outlines.shape, np.uint8)

    ratioBR = np.zeros([resolution.y, resolution.x], dtype=float)
    # extract blue and red bands
    B = np.zeros((resolution.x, resolution.y), dtype=int)
    R = np.zeros((resolution.x, resolution.y), dtype=int)
    B = img[:, :, 0].astype(int)
    R = img[:, :, 2].astype(int)

    # set all zeros (a.k.a. mask)to large negative
    B[B == 0] = settings.mask_value
    R[R == 0] = settings.mask_value

    # calculate the blue/red ratio
    for i in range(0, resolution.y):
        for j in range(0, resolution.x):
            if R[i, j] != settings.mask_value and B[i, j] != settings.mask_value:
                ratioBR[i, j] = B[i, j] / R[i, j]
            else:
                ratioBR[i, j] = settings.mask_value

    # catch Nan
    if np.argwhere(np.isnan(ratioBR)).any():
        sys.exit('NaN found in B/R ratios')

    for i in range(0, resolution.y):
        for j in range(0, resolution.x):
            if ratioBR[i, j] != settings.mask_value:
                ratioBR[i, j] = (ratioBR[i, j] - 1) / (ratioBR[i, j] + 1)

    # convert greyscale image to RGB image
    # sun (blue)
    imgRGB[np.where(np.logical_and(ratioBR >= threshold, ratioBR != settings.mask_value))] = (0, 0, 255)
    # cloud (white)
    imgRGB[np.where(np.logical_and(ratioBR < threshold, ratioBR != settings.mask_value))] = (255, 255, 255)
    # mask (black)
    imgRGB[np.where(ratioBR == settings.mask_value)] = (0, 0, 0)

    img_with_outlines = outlines_over_image(imgRGB, outlines, stencil)

    return img_with_outlines
