import settings
import os
import ephem
import math
import numpy as np
import resolution
import cv2
import matplotlib.pyplot as plt
import thresholds
import statistical_analysis
import write_to_csv
import image_interface
import skycover
import ratio


def mobotix(writer):
    """Crop mobotix images to rectangular shape and process for machine learning part

    The shape is dependent on the solar location. If the sun is east, then a crop in the west is made. If the sun is
    south (for the Northern Hemisphere), the crop region spans the north from east to west. If the sun is in the west,
    the crop region is in the east. This is to avoid solar interference with the image.
    """

    settings.data_type = 'mobotix_crop_ml'

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

                # read image
                img = cv2.imread(os.path.join(subdir, filename))

                # get resolution of the image
                resolution.get_resolution(img)

                print(camera.date, 'azimuth:', azimuth, 'altitude:', altitude)

                # solar position dependent crop regions
                if azimuth <= 135:
                    crop = img[520:1350, 670:1400, :]
                elif 135 < azimuth < 225:
                    crop = img[520:1000, 670:2035, :]
                else:
                    crop = img[520:1350, 1305:2035, :]

                cv2.rectangle(img, (680, 530), (1400, 1360), (0, 255, 0), 20)
                cv2.rectangle(img, (670, 520), (2035, 1000), (255, 0, 0), 20)
                cv2.rectangle(img, (1305, 530), (2025, 1350), (0, 0, 255), 20)

                img = img[...,::-1]
                image_interface.save_processed_image(img,'/nobackup/users/mos/results/mobotix_crop_regions.png')
                plt.close()
                quit()

                # convert from bgr to rgb
                #crop = crop[...,::-1]

                resolution.get_resolution(crop)

                energy, entropy, contrast, homogeneity = statistical_analysis.textural_features(crop)
                mean_r, mean_g, mean_b, st_dev, skewness, diff_rg, diff_rb, diff_gb = \
                    statistical_analysis.spectral_features(crop)

                red_blue_ratio = ratio.red_blue_v2(crop)

                t_swimcat = 0.9

                tmp, tmp, cloud_cover = skycover.fixed(red_blue_ratio, t_swimcat, t_swimcat)

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
                            cloud_cover
                            )

                # imgRGB = np.zeros((settings.x, settings.y, 3), np.uint8)
                # # sun
                # imgRGB[np.where(red_blue_ratio <= t_swimcat)] = settings.blue
                # # cloud
                # imgRGB[np.where(red_blue_ratio > t_swimcat)] = settings.white
                #
                # fig, (ax1, ax2) = plt.subplots(2, 1)
                # ax1.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
                # ax2.imshow(imgRGB)
                # plt.savefig('/nobackup/users/mos/results/mobotix/thresholding_tests/'+filename)
                # plt.close()
                #
                # image_interface.save_original_image(crop, '/nobackup/users/mos/data/mobotix/machine_learning/crops/'+filename+'_crop.png')

                write_to_csv.output_data(writer, data_row)


def single_RGB_image(img, corner1, corner2, corner3, corner4):
    """Crop a single Red Green Blue (RGB) image using the four corner points of a rectangle

    Args:
        img: RGB image
        corner1: first corner of the rectangle
        corner2: second corner of the rectangle
        corner3: third corner of the rectangle
        corner4: fourth corner of the rectangle

    Returns:
        Cropped image
    """
    crop = img[corner1:corner2, corner3:corner4, :]

    return crop
