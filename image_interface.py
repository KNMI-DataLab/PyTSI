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


def save_image(data, fn):
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


def single(filename):
    properties_file = filename + '.properties.gz'
    # unzip the gzip file, open the file as rt=read text
    with gzip.open(settings.main_data + properties_file, 'rt') as f:
        lines = []
        # read the file and store line per line
        for line in f:
            lines.append(line)
        # get the altitude and azimuth from the defs
        altitude = read_properties_file.get_altitude(lines)
        azimuth = read_properties_file.get_azimuth(lines)

        if altitude >= settings.minimum_altitude:
            # get the fractional sky cover from 'old' TSI software
            cover_thin_tsi, cover_opaque_tsi, cover_total_tsi = read_properties_file.get_fractional_sky_cover_tsi(
                lines)

            # filename variables
            filename_jpg = filename + '.jpg'
            filename_png = filename + '.png'

            # extract date/time information from the filename
            year = filename[0:4]
            month = filename[4:6]
            day = filename[6:8]
            hour = filename[8:10]
            minute = filename[10:12]
            second = filename[12:13] + '0'

            print(day + '/' + month + '/' + year + ' ' + hour + ':' + minute + ':' + second, end='\r')

            # read the image
            img = cv2.imread(settings.main_data + filename_jpg)
            img_tsi = cv2.imread(settings.main_data + filename_png)

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

            save_image(image_with_outlines_fixed, filename + '_processed.png')

            return azimuth, altitude, cover_total_hybrid
