# DESCRIPTION: main processing function containing calls to many functions

from createmask import createmask
import ratio
from project3d import project3d
from createregions import createRegions
from presolarcorrection import preSolarCorrection
from plotposterimages import plotPosterImages
import skycover
import thresholds
import settings
import cv2
import overlay
import sys


def processor(img, img_tsi, azimuth, altitude, filename):
    mask = createmask(img, azimuth, altitude)
    masked_img = cv2.bitwise_and(img, mask)

    if settings.use_project_3d:
        project3d(masked_img)

    fixed_sunny_threshold, fixed_thin_threshold = thresholds.fixed()
    flatNormalizedRatioBRNoZeros, stDev, hybrid_threshold = thresholds.hybrid(masked_img)

    # calculate red/blue ratio per pixel
    red_blue_ratio = ratio.red_blue(masked_img)

    # create the segments for solar correction
    regions, outlines, labels, stencil, image_with_outlines = createRegions(img, img_tsi, azimuth, altitude, filename)

    # calculate fractional skycover
    cover_thin_fixed, cover_opaque_fixed, cover_total_fixed = skycover.fixed(red_blue_ratio, fixed_sunny_threshold,
                                                                             fixed_thin_threshold)
    cover_total_hybrid = skycover.hybrid(flatNormalizedRatioBRNoZeros, hybrid_threshold)

    # overlay outlines on image(s)
    image_with_outlines_fixed = overlay.fixed(red_blue_ratio, outlines, stencil, fixed_sunny_threshold,
                                              fixed_thin_threshold)
    image_with_outlines_hybrid = overlay.hybrid(masked_img, outlines, stencil, hybrid_threshold)

    # get some data before doing actual solar/horizon area corrections
    outsideC, outsideS, horizonC, horizonS, innerC, innerS, sunC, sunS = preSolarCorrection(labels, red_blue_ratio,
                                                                                            fixed_sunny_threshold)

    # plot overview with outlines
    # saveOutputToFigures(filename,img,img_tsi,regions,image_with_outlines_fixed,image_with_outlines_hybrid)

    # plot complete overview with 5 different images, histogram and cloud cover comparisons
    # completeplot(filename,img,img_tsi,regions,image_with_outlines_fixed,image_with_outlines_hybrid,azimuth,flatNormalizedRatioBRNoZeros,HYTAThreshold,stDev)

    # plot images for use in poster
    plotPosterImages(filename, img, img_tsi, regions, image_with_outlines_fixed, image_with_outlines_hybrid)

    return cover_thin_fixed, cover_opaque_fixed, cover_total_fixed, cover_total_hybrid, masked_img, outsideC, outsideS, horizonC, horizonS, innerC, innerS, sunC, sunS
