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
import labelled_image
import overlay
import gzip
import matplotlib.pyplot as plt
import tarfile
import os


def save_original_image(data, fn):
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

    img = cv2.imread(jpg_loc)
    img_tsi_processed = cv2.imread(png_loc)

    return img, img_tsi_processed, lines, filename_jpg, filename_png


def single(filename):
    img, img_tsi_processed, properties_file, filename_jpg, filename_png = read_from_tar(filename)

    # get the altitude and azimuth from the defs
    altitude = read_properties_file.get_altitude(properties_file)
    azimuth = read_properties_file.get_azimuth(properties_file)

    if altitude >= settings.minimum_altitude:
        # get the fractional sky cover from 'old' TSI software
        cover_thin_tsi, cover_opaque_tsi, cover_total_tsi = read_properties_file.get_fractional_sky_cover_tsi(properties_file)

        # read the image
        # img = cv2.imread(settings.main_data + filename_jpg)
        # img_tsi = cv2.imread(settings.main_data + filename_png)

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
        ratio_br_norm_1d_nz, blue_red_ratio_norm, st_dev, hybrid_threshold = thresholds.hybrid(
            masked_img)
        cover_total_hybrid = skycover.hybrid(ratio_br_norm_1d_nz, hybrid_threshold)

        # create the segments for solar correction
        regions, outlines, labels, stencil, image_with_outlines = createregions.create(img, azimuth,
                                                                                           altitude,
                                                                                           mask_array)
        # get some data before doing actual solar/horizon area corrections
        outside_c, outside_s, horizon_c, horizon_s, \
        inner_c, inner_s, sun_c, sun_s = labelled_image.calculate_pixels(labels, red_blue_ratio,
                                                                             fixed_sunny_threshold)

        # overlay outlines on image(s)
        image_with_outlines_fixed = overlay.fixed(red_blue_ratio, outlines, stencil,
                                                      fixed_sunny_threshold,
                                                      fixed_thin_threshold)
        image_with_outlines_hybrid = overlay.hybrid(masked_img, outlines, stencil, hybrid_threshold)

        save_processed_image(image_with_outlines_hybrid, settings.tmp + filename + '_hybrid.png')
        save_processed_image(image_with_outlines_fixed, settings.tmp + filename + '_fixed.png')
        save_original_image(img_tsi_processed, settings.tmp + filename + '_fixed_old.png')
        save_original_image(img, settings.tmp + filename + '_original.png')

        return azimuth, altitude, cover_total_fixed, cover_total_hybrid, cover_total_tsi
