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
import read_properties_file
import resolution
import write_to_csv
import os
import math
from tqdm import tqdm
import gzip
import statistical_analysis
import ephem
import numpy as np
import matplotlib.pyplot as plt
import plot
import sys
import time


def type_TSI(writer):
    """Loop TSI data structure and features

    Args:
        writer: csv writing object
    """
    filecounter = 0

    for subdir, dirs, files in os.walk(settings.main_data):
        dirs.sort()
        files.sort()
        for filename in files:
            if filename.endswith(settings.properties_extension):
                # unzip the gzip file, open the file as rt=read text
                with gzip.open(os.path.join(subdir, filename), 'rt') as f:
                    lines = []
                    # read the file and store line per line
                    for line in f:
                        lines.append(line)
                    # get the altitude and azimuth from the defs
                    altitude = read_properties_file.get_altitude(lines)
                    azimuth = read_properties_file.get_azimuth(lines)

                    if altitude >= settings.minimum_altitude:
                        filecounter += 1
                        # get the fractional sky cover from 'old' TSI software
                        cover_thin_tsi, cover_opaque_tsi, cover_total_tsi = read_properties_file.get_fractional_sky_cover_tsi(
                            lines)

                        filename_jpg = filename.replace(settings.properties_extension, settings.jpg_extension)
                        filename_png = filename.replace(settings.properties_extension, settings.png_extension)
                        filename_no_ext = filename.replace(settings.properties_extension, '')

                        year = filename[0:4]
                        month = filename[4:6]
                        day = filename[6:8]
                        hour = filename[8:10]
                        minute = filename[10:12]
                        second = filename[12:13] + '0'

                        print(day + '/' + month + '/' + year + ' ' + hour + ':' + minute + ':' + second)

                        # read the image
                        img = cv2.imread(os.path.join(subdir, filename_jpg))
                        img_tsi = cv2.imread(os.path.join(subdir, filename_png))

                        # get the resolution of the image
                        resolution.get_resolution(img)

                        mask = createmask.create(img, azimuth)
                        masked_img = cv2.bitwise_and(img, mask)

                        fixed_sunny_threshold, fixed_thin_threshold = thresholds.fixed()
                        ratio_br_norm_1d_nz, blue_red_ratio_norm, st_dev, hybrid_threshold = thresholds.hybrid(
                            masked_img)

                        # calculate red/blue ratio per pixel
                        red_blue_ratio = ratio.red_blue_v2(masked_img)

                        if settings.use_postprocessing:
                            # create the segments for solar correction
                            regions, outlines, labels, stencil, image_with_outlines = createregions.create(img, azimuth,
                                                                                                           altitude)
                            # get some data before doing actual solar/horizon area corrections
                            outside_c, outside_s, horizon_c, horizon_s, inner_c, inner_s, sun_c, sun_s = labelled_image.calculate_pixels(
                                labels,
                                red_blue_ratio,
                                fixed_sunny_threshold)

                            # overlay outlines on image(s)
                            image_with_outlines_fixed = overlay.fixed(red_blue_ratio, outlines, stencil,
                                                                      fixed_sunny_threshold,
                                                                      fixed_thin_threshold)
                            image_with_outlines_hybrid = overlay.hybrid(masked_img, outlines, stencil, hybrid_threshold)

                            if settings.plot_overview:
                                # plot complete overview with 5 different images, histogram and cloud cover comparisons
                                overview.plot(img, img_tsi, regions, image_with_outlines_fixed,
                                              image_with_outlines_hybrid,
                                              azimuth,
                                              ratio_br_norm_1d_nz, hybrid_threshold, st_dev)

                            if settings.plot_poster_images:
                                # plot images for use in poster
                                poster_images.plot(filename_no_ext, img, img_tsi, image_with_outlines_fixed)
                        else:
                            outside_c = outside_s = horizon_c = horizon_s = inner_c = inner_s = sun_c = sun_s = None

                        # calculate fractional skycover
                        cover_thin_fixed, cover_opaque_fixed, cover_total_fixed = skycover.fixed(red_blue_ratio,
                                                                                                 fixed_sunny_threshold,
                                                                                                 fixed_thin_threshold)
                        cover_total_hybrid = skycover.hybrid(ratio_br_norm_1d_nz, hybrid_threshold)

                        # calculate statistical properties of the image
                        if settings.use_statistical_analysis:
                            energy, entropy, contrast, homogeneity = statistical_analysis.textural_features(img)
                        else:
                            energy = entropy = contrast = homogeneity = None

                        data_row = (filename_no_ext,
                                    altitude,
                                    azimuth,
                                    cover_thin_fixed, cover_opaque_fixed,
                                    cover_total_fixed,
                                    cover_total_hybrid,
                                    cover_thin_tsi,
                                    cover_opaque_tsi,
                                    cover_total_tsi,
                                    energy,
                                    entropy,
                                    contrast,
                                    homogeneity,
                                    outside_c,
                                    outside_s,
                                    horizon_c,
                                    horizon_s,
                                    inner_c,
                                    inner_s,
                                    sun_c,
                                    sun_s
                                    )

                        write_to_csv.output_data(writer, data_row)

    return filecounter


def type_swimcat(writer):
    """Loop swimcat data structure and features

    Args:
        writer: csv writing object
    """
    dir_list = (settings.main_data + 'A-sky/images/',
                # settings.main_data + 'B-pattern/images/',
                # settings.main_data + 'C-thick-dark/images/',
                settings.main_data + 'D-thick-white/images/')
                # settings.main_data + 'E-veil/images/')

    filecounter = 0

    for cloud_type, dir_name in enumerate(tqdm(dir_list)):
        dir_name = os.fsencode(dir_list[cloud_type])
        dir_name = os.listdir(dir_name)
        for file in tqdm(dir_name):
            filecounter += 1

            filename = os.fsdecode(file)
            # absolute location of the file
            file_location = dir_list[cloud_type] + filename
            # read the image
            img = cv2.imread(file_location)

            resolution.get_resolution(img)

            # GLCM = statistical_analysis.calculate_greymatrix(img)
            energy, entropy, contrast, homogeneity = statistical_analysis.textural_features(img)
            mean_r, mean_g, mean_b, st_dev, skewness, diff_rg, diff_rb, diff_gb = statistical_analysis.spectral_features(
                img)

            if settings.use_hybrid_SEG:
                ratio_br_norm_1d_nz, blue_red_ratio_norm, st_dev, threshold = thresholds.hybrid(img)
                cloud_cover = skycover.hybrid(ratio_br_norm_1d_nz, threshold)
            else:
                red_blue_ratio = ratio.red_blue_v2(img)
                threshold = settings.fixed_threshold_swim
                tmp, tmp, cloud_cover = skycover.fixed(red_blue_ratio, threshold, threshold)

            data_row = (filename,
                        mean_r,
                        mean_g,
                        mean_b,
                        st_dev,
                        skewness,
                        diff_rg,
                        diff_rb,
                        diff_gb,
                        energy,
                        entropy,
                        contrast,
                        homogeneity,
                        cloud_cover,
                        cloud_type
                        )

            write_to_csv.output_data(writer, data_row)

    return filecounter


def type_swimseg(writer):
    """Loop swimseg data structure and features

    Args:
        writer: csv writing object
    """
    cloud_cover_GT = []

    filecounter = 0

    for subdir, dirs, files in os.walk(settings.main_data):
        dirs.sort()
        files.sort()
        for i, filename in enumerate(files):
            if filename.endswith(settings.png_extension):
                filecounter += 1
                if filename.find('GT', 0, len(filename)) != -1:
                    img = cv2.imread(os.path.join(subdir, filename))

                    resolution.get_resolution(img)


                    # Calculate counts of cloudy and clear sky pixels. In this case, the images that are loaded are
                    # black/white (bw). Thus the only occurring RGB values are (255,255,255) and (0,0,0) for white and
                    # black respectively. Checking if one of the bands is equal to either 255 or 0 is enough to
                    # determine white or black pixel and subsequently if the ground truth map indicates clear sky
                    # or clouds.

                    cloud = np.sum(img[:, :, 0] == 255) # when one of the bands is 255, pixel is white
                    clear_sky = np.sum(img[:, :, 0] == 0) # when one of the bands is 0, pixel is black

                    cloud_cover_GT.append(cloud / (cloud + clear_sky))

                else:
                    filename_no_ext = filename.replace(settings.png_extension, '')

                    img = cv2.imread(os.path.join(subdir, filename))

                    resolution.get_resolution(img)

                    # fixed sky cover
                    red_blue_ratio = ratio.red_blue_v2(img)
                    cloud = np.sum(red_blue_ratio >= settings.fixed_threshold_swim)
                    clear_sky = np.sum(red_blue_ratio < settings.fixed_threshold_swim)

                    img_bw = np.empty((settings.x, settings.y))
                    img_bw[red_blue_ratio >= settings.fixed_threshold_swim] = 1
                    img_bw[red_blue_ratio < settings.fixed_threshold_swim] = 0

                    cloud_cover_fixed = cloud / (cloud + clear_sky)

                    # hybrid sky cover
                    ratio_br_norm_1d_nz, blue_red_ratio_norm, st_dev, threshold = thresholds.hybrid(img)
                    cloud_cover_hybrid = skycover.hybrid(ratio_br_norm_1d_nz, threshold)

                    data_row = (filename_no_ext, cloud_cover_GT[i], cloud_cover_fixed, cloud_cover_hybrid)
                    print(filename_no_ext, cloud_cover_GT[i], cloud_cover_fixed, cloud_cover_hybrid)

                    #plot.original_and_binary_and_histogram(img, filename,
                    #                                       blue_red_ratio_norm, 'blue/red ratio',
                    #                                       ratio_br_norm_1d_nz, 'blue/red norm histogram',
                    #                                      'Normalized B/R', 'Frequency',
                    #                                       st_dev, threshold)

                    write_to_csv.output_data(writer, data_row)

    return filecounter


def type_mobotix(writer):
    """Processing loop for mobotix type images/data structure

    Args:
        writer: csv writing object
    """
    # initialize the observer object
    camera = ephem.Observer()

    # location and elevation of the Mobotix camera at Cabauw
    camera.lat = settings.camera_latitude
    camera.lon = settings.camera_longitude
    camera.elevation = settings.camera_elevation

    n_increment = 0
    filecounter = 0

    for subdir, dirs, files in os.walk(settings.main_data):
        dirs.sort()
        files.sort()

        for filename in files:
            year = int('20' + filename[1:3])
            month = int(filename[3:5])
            day = int(filename[5:7])
            hour = int(filename[7:9])
            minute = int(filename[9:11])
            second = int(filename[11:13])

            # TODO: things WILL go wrong with UTC/CEST time zones
            # set time of observer object
            camera.date = str(year) + '/' + \
                          str(month) + '/' + \
                          str(day) + ' ' + \
                          str(hour) + ':' + \
                          str(minute) + ':' + \
                          str(second)

            # make sun object
            solar_position = ephem.Sun(camera)

            azimuth = math.degrees(float(repr(solar_position.az)))
            altitude = math.degrees(float(repr(solar_position.alt)))

            n_increment += 1

            if altitude < settings.minimum_altitude:
                continue

            if filename.endswith(settings.jpg_extension) and not n_increment % settings.skip_loops:
                filecounter += 1
                filename_no_ext = filename.replace(settings.jpg_extension, '')

                img = cv2.imread(os.path.join(subdir, filename))

                img = img[105:2000, 335:2375, :]

                resolution.get_resolution(img)

                mask = np.zeros(img.shape, dtype='uint8')
                cv2.circle(mask, (int(settings.y / 2), int(settings.x / 2)), settings.radius_mobotix_circle,
                           settings.white, -1)

                # img = img[..., ::-1]

                masked = cv2.bitwise_and(img, mask)

                cv2.line(masked, (840, 475), (720, 70), settings.black, 35)

                blue_red_ratio_norm_1d_nz, blue_red_ratio_norm, st_dev, threshold = thresholds.hybrid(masked)

                # plot.histogram(blue_red_ratio_norm_1d_nz, filename, 'Normalized B/R', 'Frequency', st_dev, threshold)
                # plot.binary(blue_red_ratio_norm, filename, threshold)

                # plot.original_and_binary_and_histogram(img, filename_no_ext,
                #                                        blue_red_ratio_norm, 'normalized blue/red ratio',
                #                                        blue_red_ratio_norm_1d_nz, 'blue/red norm histogram',
                #                                        'Normalized B/R', 'Frequency',
                #                                        st_dev, threshold)

                cloud_cover = skycover.hybrid(blue_red_ratio_norm_1d_nz, threshold)

                print(camera.date, 'azimuth:', azimuth, 'altitude:', altitude, 'cloud cover:', cloud_cover)

                if settings.use_statistical_analysis:
                    energy, entropy, contrast, homogeneity = statistical_analysis.textural_features(img)
                else:
                    energy = entropy = contrast = homogeneity = 0

                data_row = (filename_no_ext,
                            azimuth,
                            altitude,
                            energy,
                            entropy,
                            contrast,
                            homogeneity,
                            cloud_cover
                            )

                write_to_csv.output_data(writer, data_row)

    return filecounter


def structure(writer):
    """Determine and call loop for type of data

    Args:
        writer: csv writing object
    """
    start_time = time.time()

    if settings.data_type == settings.tsi_str:
        n_files = type_TSI(writer)

    elif settings.data_type == settings.cat_str:
        n_files = type_swimcat(writer)

    elif settings.data_type == settings.seg_str:
        n_files = type_swimseg(writer)

    elif settings.data_type == settings.mob_str:
        n_files = type_mobotix(writer)

    print("Main loop time: %s seconds" % round((time.time() - start_time), 10))
    print("Average time per image: %s seconds" % round((time.time() - start_time) / n_files, 10))