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
from tqdm import tqdm
import gzip
import statistical_analysis


def type_TSI(writer):
    """Loop TSI data structure and features

    Args:
        writer: csv writing object

    Returns:

    """
    # converts the directory from string into 'bytes'
    directory = os.fsencode(settings.main_data)

    # alphabetically sort the files in the directory
    sorted_directory = sorted(os.listdir(directory))

    # look for the file names
    for file in tqdm(sorted_directory):
        # decode the filename from bytes to string
        filename = os.fsdecode(file)
        # search for all files ending with particular extension
        if filename.endswith(settings.properties_extension):
            # unzip the gzip file, open the file as rt=read text
            with gzip.open(settings.main_data + '/' + filename, 'rt') as f:
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

                    filename_jpg = filename.replace(settings.properties_extension, settings.jpg_extension)
                    filename_png = filename.replace(settings.properties_extension, settings.png_extension)
                    filename_no_ext = filename.replace(settings.properties_extension, '')

                    # read the image
                    img = cv2.imread(settings.main_data + '/' + filename_jpg)
                    img_tsi = cv2.imread(settings.main_data + '/' + filename_png)

                    # get the resolution of the image
                    resolution.get_resolution(img)

                    mask = createmask.create(img, azimuth)
                    masked_img = cv2.bitwise_and(img, mask)

                    fixed_sunny_threshold, fixed_thin_threshold = thresholds.fixed()
                    ratio_br_norm_1d_nz, st_dev, hybrid_threshold = thresholds.hybrid(masked_img)

                    # calculate red/blue ratio per pixel
                    red_blue_ratio = ratio.red_blue_v2(masked_img)

                    # create the segments for solar correction
                    regions, outlines, labels, stencil, image_with_outlines = createregions.create(img, azimuth,
                                                                                                   altitude)

                    # calculate fractional skycover
                    cover_thin_fixed, cover_opaque_fixed, cover_total_fixed = skycover.fixed(red_blue_ratio,
                                                                                             fixed_sunny_threshold,
                                                                                             fixed_thin_threshold)
                    cover_total_hybrid = skycover.hybrid(ratio_br_norm_1d_nz, hybrid_threshold)

                    # overlay outlines on image(s)
                    image_with_outlines_fixed = overlay.fixed(red_blue_ratio, outlines, stencil, fixed_sunny_threshold,
                                                              fixed_thin_threshold)
                    image_with_outlines_hybrid = overlay.hybrid(masked_img, outlines, stencil, hybrid_threshold)

                    # get some data before doing actual solar/horizon area corrections
                    outside_c, outside_s, horizon_c, horizon_s, inner_c, inner_s, sun_c, sun_s = labelled_image.calculate_pixels(
                        labels,
                        red_blue_ratio,
                        fixed_sunny_threshold)

                    # calculate statistical properties of the image
                    if settings.use_statistical_analysis:
                        energy, entropy, contrast, homogeneity = statistical_analysis.textural_features(img)
                    else:
                        energy = entropy = contrast = homogeneity = 0

                    if settings.plot_overview:
                        # plot complete overview with 5 different images, histogram and cloud cover comparisons
                        overview.plot(img, img_tsi, regions, image_with_outlines_fixed, image_with_outlines_hybrid,
                                      azimuth,
                                      ratio_br_norm_1d_nz, hybrid_threshold, st_dev)

                    if settings.plot_poster_images:
                        # plot images for use in poster
                        poster_images.plot(filename_no_ext, img, img_tsi, image_with_outlines_fixed)

                    data_row = (filename_no_ext,
                                altitude,
                                azimuth,
                                cover_thin_fixed,
                                cover_opaque_fixed,
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


def type_SEG(writer):
    """Loop SEG data structure and features

    Args:
        writer: csv writing object

    Returns:

    """
    dir_list = []
    dir_list.append(settings.main_data + 'A-sky/images')
    dir_list.append(settings.main_data + 'B-pattern/images/')
    # dir_list.append(settings.main_data + 'C-thick-dark/images/')
    dir_list.append(settings.main_data + 'D-thick-white/images/')
    dir_list.append(settings.main_data + 'E-veil/images/')

    for cloud_type, dir_name in enumerate(tqdm(dir_list)):
        dir_name = os.fsencode(dir_list[cloud_type])
        dir_name = os.listdir(dir_name)
        for file in tqdm(dir_name):
            filename = os.fsdecode(file)
            # absolute location of the file
            file_location = dir_list[cloud_type] + '/' + filename
            # read the image
            img = cv2.imread(file_location)

            resolution.get_resolution(img)

            # GLCM = statistical_analysis.calculate_greymatrix(img)
            energy, entropy, contrast, homogeneity = statistical_analysis.textural_features(img)
            mean_r, mean_g, mean_b, st_dev, skewness, diff_rg, diff_rb, diff_gb = statistical_analysis.spectral_features(
                img)

            if settings.use_hybrid_SEG:
                ratio_br_norm_1d_nz, st_dev, threshold = thresholds.hybrid(img)
                cloud_cover = skycover.hybrid(ratio_br_norm_1d_nz, threshold)
            else:
                red_blue_ratio = ratio.red_blue_v2(img)
                threshold = settings.fixed_SEG_threshold
                tmp, tmp, cloud_cover = skycover.fixed(red_blue_ratio, threshold, threshold)
                # print(filename)
                # ret, t1 = cv2.threshold(red_blue_ratio, threshold, 255, cv2.THRESH_BINARY)
                # plt.imshow(t1,cmap='Blues_r')
                # plt.show()

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


def structure(writer):
    """Determine and call loop for type of data

    Args:
        writer: csv writing object

    Returns:

    """
    if settings.data_type == 'TSI':
        type_TSI(writer)

    elif settings.data_type == 'SEG':
        type_SEG(writer)

    elif settings.data_type == '':
        pass
