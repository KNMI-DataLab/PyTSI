"""Underlying processing module of the user interface."""

import settings
import read_properties_file
import cv2
import resolution
import mask
import thresholds
import skycover
import createregions
import numpy as np
import ratio
import overlay
import gzip
import matplotlib.pyplot as plt
import tarfile


def save_original_image(data, fn):
    """Save image, converting it from BGR to RGB.

    Args:
        data: image in array format to be saved (BGR)
        fn: filename
    """
    sizes = np.shape(data)
    height = float(sizes[0])
    width = float(sizes[1])

    fig = plt.figure()
    fig.set_size_inches(width / height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(cv2.cvtColor(data, cv2.COLOR_BGR2RGB))
    plt.savefig(fn, dpi=height)
    plt.close()


def save_processed_image(data, fn):
    """Save image as RGB.

    Args:
        data: image in array format to be saved (RGB)
        fn: filename
    """
    sizes = np.shape(data)
    height = float(sizes[0])
    width = float(sizes[1])

    fig = plt.figure()
    fig.set_size_inches(width / height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(data)
    plt.savefig(fn, dpi=height)
    plt.close()


def read_from_tar(filename_no_ext):
    """Temporarily open source tar file, extracting any information out of it and saving to tmp folder.

    Args:
        filename_no_ext: filename without any extension

    Returns:
        tuple: imgages and additional information required for processing
    """
    # filename variables
    filename_jpg = filename_no_ext + '.jpg'
    filename_png = filename_no_ext + '.png'
    properties_file = filename_no_ext + '.properties.gz'

    settings.year = filename_no_ext[0:4]
    settings.month = filename_no_ext[4:6]
    settings.day = filename_no_ext[6:8]
    settings.hour = filename_no_ext[8:10]
    settings.minute = filename_no_ext[10:12]

    path = settings.tsi_database + settings.year + '/' + settings.month + '/DBASE/' + settings.year + settings.month + \
           settings.day + '_tsi-cabauw_realtime.tar'

    tar = tarfile.open(path)

    tar.extract(filename_jpg, 'tmp')
    tar.extract(filename_png, 'tmp')
    tar.extract(properties_file, 'tmp')

    tar.close()

    jpg_loc = 'tmp/' + filename_jpg
    png_loc = 'tmp/' + filename_png
    properties_loc = 'tmp/' + properties_file

    # unzip the gzip file, open the file as rt=read text
    with gzip.open(properties_loc, 'rt') as f:
        lines = []
        # read the file and store line per line
        for line in f:
            lines.append(line)

    # get the altitude and azimuth from the defs
    altitude = read_properties_file.get_altitude(lines)
    azimuth = read_properties_file.get_azimuth(lines)

    img = cv2.imread(jpg_loc)
    img_tsi_processed = cv2.imread(png_loc)

    return img, img_tsi_processed, lines, filename_jpg, filename_png, azimuth, altitude


def single(filename):
    """Process a single image

    Args:
        filename: filename without an extension

    Returns:
        tuple: information about the processed images
    """
    img, img_tsi_processed, properties_file, filename_jpg, filename_png, azimuth, altitude = read_from_tar(filename)

    if altitude >= settings.minimum_altitude:
        # get the fractional sky cover from 'old' TSI software
        cover_thin_tsi, cover_opaque_tsi, cover_total_tsi = read_properties_file.get_fractional_sky_cover_tsi(properties_file)

        # get the resolution of the image
        resolution.get_resolution(img)

        # create and apply the mask
        mask_array = mask.create(img, azimuth)
        masked_img = mask.apply(img, mask_array)

        # calculate red/blue ratio per pixel
        red_blue_ratio = ratio.red_blue_v2(masked_img)

        # calculate fixed fractional skycover
        fixed_sunny_threshold, fixed_thin_threshold = thresholds.fixed()
        cover_thin_fixed, cover_opaque_fixed, cover_total_fixed = skycover.fixed(red_blue_ratio,
                                                                                 fixed_sunny_threshold,
                                                                                 fixed_thin_threshold)

        # calculate hybrid sky cover
        ratio_br_norm_1d_nz, blue_red_ratio_norm, st_dev, hybrid_threshold_mce, hybrid_threshold_otsu = \
            thresholds.hybrid(masked_img)
        cover_total_hybrid_mce = skycover.hybrid(ratio_br_norm_1d_nz, hybrid_threshold_mce)
        cover_total_hybrid_otsu = skycover.hybrid(ratio_br_norm_1d_nz, hybrid_threshold_otsu)

        # create the segments for solar correction
        regions, outlines, labels, stencil, image_with_outlines = createregions.create(img, azimuth,
                                                                                           altitude,
                                                                                           mask_array)

        # overlay outlines on image(s)
        image_with_outlines_fixed = overlay.fixed(red_blue_ratio, outlines, stencil,
                                                      fixed_sunny_threshold,
                                                      fixed_thin_threshold)
        image_with_outlines_hybrid = overlay.hybrid(masked_img, outlines, stencil, hybrid_threshold_mce)

        save_processed_image(image_with_outlines_hybrid, settings.tmp + filename + '_hybrid.png')
        save_processed_image(image_with_outlines_fixed, settings.tmp + filename + '_fixed.png')
        save_original_image(img_tsi_processed, settings.tmp + filename + '_fixed_old.png')
        save_original_image(img, settings.tmp + filename + '_original.png')

        azimuth = round(azimuth, 3)
        altitude = round(altitude , 3)
        cover_total_fixed= round(cover_total_fixed, 3)
        cover_total_hybrid = round(cover_total_hybrid_mce, 3)
        cover_total_tsi = round(cover_total_tsi, 3)


        return azimuth, altitude, cover_total_fixed, cover_total_hybrid, cover_total_tsi
