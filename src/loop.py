import mask
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
import gzip
import statistical_analysis
import ephem
import numpy as np
import time
from tqdm import tqdm
import crop
import solar_position


def type_TSI(writer):
    """Loop TSI data structure and features

    Args:
        writer: csv writing object

    Returns:
        n_files: amount of files processed (integer)
    """
    filecounter = 0
    n_increment = 0

    obs, solar_body = solar_position.setup_objects()

    for subdir, dirs, files in os.walk(settings.main_data):
        dirs.sort()
        files.sort()
        for filename in files:
            n_increment += 1
            if filename.endswith(settings.properties_extension) and not n_increment % settings.skip_loops:
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

                        # filename variables
                        filename_jpg = filename.replace(settings.properties_extension, settings.jpg_extension)
                        filename_png = filename.replace(settings.properties_extension, settings.png_extension)
                        filename_no_ext = filename.replace(settings.properties_extension, '')

                        # extract date/time information from the filename
                        year = filename[0:4]
                        month = filename[4:6]
                        day = filename[6:8]
                        hour = filename[8:10]
                        minute = filename[10:12]
                        second = filename[12:13] + '0'

                        print(day + '/' + month + '/' + year + ' ' + hour + ':' + minute + ':' + second, end='\r')

                        # maximum solar altitude on current day
                        transit_alt = solar_position.transit(year, month, day, obs, solar_body)

                        # relative current solar altitude
                        relative_alt = 0
                        relative_alt = altitude / transit_alt

                        # read the image
                        img = cv2.imread(os.path.join(subdir, filename_jpg))
                        # img_tsi = cv2.imread(os.path.join(subdir, filename_png))

                        # get the resolution of the image
                        resolution.get_resolution(img)

                        # create and apply the mask
                        mask_array = mask.create(img, azimuth)
                        masked_img = mask.apply(img, mask_array)

                        # calculate red/blue ratio per pixel
                        red_blue_ratio = ratio.red_blue_v2(masked_img)

                        # calculate fixed fractional skycover
                        cover_thin_fixed = cover_opaque_fixed = cover_total_fixed = 0
                        fixed_sunny_threshold, fixed_thin_threshold = thresholds.fixed()
                        cover_thin_fixed, cover_opaque_fixed, cover_total_fixed = skycover.fixed(red_blue_ratio,
                                                                                                 fixed_sunny_threshold,
                                                                                                 fixed_thin_threshold)

                        # calculate hybrid sky cover
                        cover_total_hybrid_mce = cover_total_hybrid_otsu = cover_total_hybrid_kmeans = 0
                        #ratio_br_norm_1d_nz, blue_red_ratio_norm, st_dev, hybrid_threshold_mce, hybrid_threshold_otsu, \
                        #    hybrid_threshold_kmeans = thresholds.hybrid(masked_img)
                        #cover_total_hybrid_mce = skycover.hybrid(ratio_br_norm_1d_nz, hybrid_threshold_mce)
                        #cover_total_hybrid_otsu = skycover.hybrid(ratio_br_norm_1d_nz, hybrid_threshold_otsu)
                        #cover_total_hybrid_kmeans = skycover.hybrid(ratio_br_norm_1d_nz, hybrid_threshold_kmeans)

                        if settings.use_postprocessing:
                            # create the segments for solar correction
                            regions, outlines, labels, stencil, image_with_outlines = createregions.create(img, azimuth,
                                                                                                           altitude,
                                                                                                           mask_array)
                            # get some data before doing actual solar/horizon area corrections
                            outside_c, outside_s, horizon_c, horizon_s, \
                            inner_c, inner_s, sun_c, sun_s = labelled_image.calculate_pixels(labels, red_blue_ratio,
                                                                                             fixed_sunny_threshold)

                            # overlay outlines on image(s)
                            #image_with_outlines_fixed = overlay.fixed(red_blue_ratio, outlines, stencil,
                            #                                          fixed_sunny_threshold,
                            #                                          fixed_thin_threshold)
                            #image_with_outlines_hybrid = overlay.hybrid(masked_img, outlines, stencil, hybrid_threshold_mce)
                        else:
                            outside_c = outside_s = horizon_c = horizon_s = inner_c = inner_s = sun_c = sun_s = None

                        # calculate statistical properties of the image
                        if settings.use_statistical_analysis:
                            energy, entropy, contrast, homogeneity = statistical_analysis.textural_features(img)
                        else:
                            energy = entropy = contrast = homogeneity = None

                        # prepare data for writing to csv
                        data_row = (filename_no_ext,
                                    altitude,
                                    relative_alt,
                                    azimuth,
                                    cover_thin_fixed, cover_opaque_fixed,
                                    cover_total_fixed,
                                    cover_total_hybrid_mce,
                                    cover_total_hybrid_otsu,
                                    cover_total_hybrid_kmeans,
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

    Returns:
        n_files: amount of files processed (integer)
    """
    filecounter = 0

    for cloud_type, dir_name in enumerate(tqdm(settings.swim_dirs)):
        dir_name = os.fsencode(settings.swim_dirs[cloud_type])
        dir_name = os.listdir(dir_name)
        for file in tqdm(dir_name):
            filecounter += 1

            filename = os.fsdecode(file)
            # absolute location of the file
            file_location = settings.swim_dirs[cloud_type] + filename
            # read the image
            img = cv2.imread(file_location)

            resolution.get_resolution(img)

            energy, entropy, contrast, homogeneity = statistical_analysis.textural_features(img)
            mean_r, mean_g, mean_b, st_dev, skewness, diff_rg, diff_rb, diff_gb = statistical_analysis.spectral_features(
                img)

            # fixed cloud cover
            red_blue_ratio = ratio.red_blue_v2(img)
            threshold = settings.fixed_threshold_swim
            tmp, tmp, cloud_cover_fixed = skycover.fixed(red_blue_ratio, threshold, threshold)

            # decide whether to use hybrid thresholding for this database
            if settings.use_hybrid_SEG:
                # hybrid cloud cover cloud cover
                ratio_br_norm_1d_nz, blue_red_ratio_norm, st_dev, threshold = thresholds.hybrid(img)
                cloud_cover_hybrid = skycover.hybrid(ratio_br_norm_1d_nz, threshold)
            else:
                cloud_cover_hybrid = None

            # prepare data for writing to csv
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
                        cloud_cover_fixed,
                        cloud_type
                        )

            write_to_csv.output_data(writer, data_row)

    return filecounter


def type_swimseg(writer):
    """Loop swimseg data structure and features

    Args:
        writer: csv writing object

    Returns:
        n_files: amount of files processed (integer)
    """
    # create empty list for ground truth values
    cloud_cover_GT = []

    filecounter = 0

    for subdir, dirs, files in os.walk(settings.main_data):
        dirs.sort()
        files.sort()
        for i, filename in enumerate(files):
            if filename.endswith(settings.png_extension):
                # check if we are dealing with ground truth maps or RGB images
                if filename.find('GT', 0, len(filename)) != -1:
                    img = cv2.imread(os.path.join(subdir, filename))

                    # get the resolution of the image
                    resolution.get_resolution(img)

                    # Calculate counts of cloudy and clear sky pixels. In this case, the images that are loaded are
                    # black/white (bw). Thus the only occurring RGB values are (255,255,255) and (0,0,0) for white and
                    # black respectively. Checking if one of the bands is equal to either 255 or 0 is enough to
                    # determine white or black pixel and subsequently if the ground truth map indicates clear sky
                    # or clouds.

                    cloud = np.sum(img[:, :, 0] == 255)  # when one of the bands is 255, pixel is white
                    clear_sky = np.sum(img[:, :, 0] == 0)  # when one of the bands is 0, pixel is black

                    # append the cloud cover to the ground truth list
                    cloud_cover_GT.append(cloud / (cloud + clear_sky))

                else:
                    filecounter += 1

                    filename_no_ext = filename.replace(settings.png_extension, '')

                    img = cv2.imread(os.path.join(subdir, filename))

                    resolution.get_resolution(img)

                    # fixed cloud cover
                    red_blue_ratio = ratio.red_blue_v2(img)
                    cloud = np.sum(red_blue_ratio >= settings.fixed_threshold_swim)
                    clear_sky = np.sum(red_blue_ratio < settings.fixed_threshold_swim)

                    cloud_cover_fixed = cloud / (cloud + clear_sky)

                    # hybrid cloud cover
                    ratio_br_norm_1d_nz, blue_red_ratio_norm, st_dev, threshold = thresholds.hybrid(img)
                    cloud_cover_hybrid = skycover.hybrid(ratio_br_norm_1d_nz, threshold)

                    # prepare data for writing to csv
                    data_row = (filename_no_ext, cloud_cover_GT[i], cloud_cover_fixed, cloud_cover_hybrid)
                    print(filename_no_ext, cloud_cover_GT[i], cloud_cover_fixed, cloud_cover_hybrid)

                    # plot.original_and_binary_and_histogram(img, filename,
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

    Returns:
        int: amount of files processed
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
            # extract the dat/time information from the file name
            year = int('20' + filename[1:3])
            month = int(filename[3:5])
            day = int(filename[5:7])
            hour = int(filename[7:9])
            minute = int(filename[9:11])
            second = int(filename[11:13])

            # TODO: things WILL go wrong with UTC/CEST time zones
            # set time of observer object (in this case, the camera is the observer)
            camera.date = str(year) + '/' + str(month) + '/' + str(day) + ' ' + str(hour) + ':' + \
                          str(minute) + ':' + str(second)

            # create and read position of sun object
            solar_position = ephem.Sun(camera)

            azimuth = math.degrees(float(repr(solar_position.az)))
            altitude = math.degrees(float(repr(solar_position.alt)))

            # used for skipping files (see settings.py)
            n_increment += 1

            if altitude < settings.minimum_altitude:
                continue

            if filename.endswith(settings.jpg_extension) and not n_increment % settings.skip_loops:
                filecounter += 1
                filename_no_ext = filename.replace(settings.jpg_extension, '')

                img = cv2.imread(os.path.join(subdir, filename))

                # crop image
                img = crop.single_RGB_image(img, 105, 2000, 335, 2375)

                # get resolution of the image
                resolution.get_resolution(img)

                # create and apply mask
                mask = np.zeros(img.shape, dtype='uint8')
                cv2.circle(mask, (int(settings.y / 2), int(settings.x / 2)), settings.radius_mobotix_circle,
                           settings.white, -1)

                masked = cv2.bitwise_and(img, mask)

                cv2.line(masked, (840, 475), (720, 70), settings.black, 35)

                # hybrid cloud cover
                blue_red_ratio_norm_1d_nz, blue_red_ratio_norm, st_dev, threshold = thresholds.hybrid(masked)
                cloud_cover = skycover.hybrid(blue_red_ratio_norm_1d_nz, threshold)

                # plot.histogram(blue_red_ratio_norm_1d_nz, filename, 'Normalized B/R', 'Frequency', st_dev, threshold)
                # plot.binary(blue_red_ratio_norm, filename, threshold)

                # plot.original_and_binary_and_histogram(img, filename_no_ext,
                #                                        blue_red_ratio_norm, 'normalized blue/red ratio',
                #                                        blue_red_ratio_norm_1d_nz, 'blue/red norm histogram',
                #                                        'Normalized B/R', 'Frequency',
                #                                        st_dev, threshold)

                print(camera.date, 'azimuth:', azimuth, 'altitude:', altitude, 'cloud cover:', cloud_cover)

                if settings.use_statistical_analysis:
                    energy, entropy, contrast, homogeneity = statistical_analysis.textural_features(img)
                else:
                    energy = entropy = contrast = homogeneity = None

                # prepare data for writing to csv
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
    print('Amount of file processed: %s' % n_files)
    print("Average time per image: %s seconds" % round((time.time() - start_time) / n_files, 10))
