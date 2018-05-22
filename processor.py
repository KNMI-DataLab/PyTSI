# DESCRIPTION: main processing function containing calls to many functions

import createmask
import ratio
import createregions
import poster_images
import skycover
import thresholds
import settings
import cv2
import overlay
import labelled_image
import overview


def processor(img, img_tsi, azimuth, altitude, filename):
    mask = createmask.create(img, azimuth)
    masked_img = cv2.bitwise_and(img, mask)

    fixed_sunny_threshold, fixed_thin_threshold = thresholds.fixed()
    ratioBR_norm_1d_nz, st_dev, hybrid_threshold = thresholds.hybrid(masked_img)

    # calculate red/blue ratio per pixel
    red_blue_ratio = ratio.red_blue(masked_img)

    # create the segments for solar correction
    regions, outlines, labels, stencil, image_with_outlines = createregions.create(img, azimuth, altitude)

    # calculate fractional skycover
    cover_thin_fixed, cover_opaque_fixed, cover_total_fixed = skycover.fixed(red_blue_ratio, fixed_sunny_threshold,
                                                                             fixed_thin_threshold)
    cover_total_hybrid = skycover.hybrid(ratioBR_norm_1d_nz, hybrid_threshold)

    # overlay outlines on image(s)
    image_with_outlines_fixed = overlay.fixed(red_blue_ratio, outlines, stencil, fixed_sunny_threshold,
                                              fixed_thin_threshold)
    image_with_outlines_hybrid = overlay.hybrid(masked_img, outlines, stencil, hybrid_threshold)

    # get some data before doing actual solar/horizon area corrections
    outside_c, outside_s, horizon_c, horizon_s, inner_c, inner_s, sun_c, sun_s = labelled_image.calculate_pixels(labels,
                                                                                                                 red_blue_ratio,
                                                                                                                 fixed_sunny_threshold)

    # plot overview with outlines
    # saveOutputToFigures(filename,img,img_tsi,regions,image_with_outlines_fixed,image_with_outlines_hybrid)

    if settings.plot_overview:
        # plot complete overview with 5 different images, histogram and cloud cover comparisons
        overview.plot(img, img_tsi, regions, image_with_outlines_fixed, image_with_outlines_hybrid, azimuth,
                      ratioBR_norm_1d_nz, hybrid_threshold, st_dev)

    if settings.plot_poster_images:
        # plot images for use in poster
        poster_images.plot(filename, img, img_tsi, image_with_outlines_fixed)

    return cover_thin_fixed, cover_opaque_fixed, cover_total_fixed, cover_total_hybrid, masked_img, outside_c, outside_s, horizon_c, horizon_s, inner_c, inner_s, sun_c, sun_s
