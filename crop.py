import settings
import os
import ephem
import math
import numpy as np
import resolution
import cv2
import matplotlib.pyplot as plt


def mobotix():
    """Crop mobotix images to rectangular shape.

    The shape is dependent on the solar location. If the sun is east, then a crop in the west is made. If the sun is
    south (for the Northern Hemisphere), the crop region spans the north from east to west. If the sun is in the west,
    the crop region is in the east. This is to avoid solar interference with the image.
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

                # read image
                img = cv2.imread(os.path.join(subdir, filename))

                # get resolution of the image
                resolution.get_resolution(img)

                print(camera.date, 'azimuth:', azimuth, 'altitude:', altitude)

                # solar position dependent crop regions
                if azimuth <= 135:
                    crop = img[520:1350, 670:1400, :]
                elif azimuth > 135 and azimuth < 225:
                    crop = img[520:1000, 670:2035, :]
                elif azimuth >= 225:
                    crop = img[520:1350, 1305:2035, :]

                plt.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
                plt.savefig(settings.results_folder + settings.data_type + '/crops/' + filename_no_ext + '_crop.png')
                plt.close()

                # cv2.rectangle(img, (670, 520), (1400, 1350), (0, 255, 0), 10)
                # cv2.rectangle(img, (680, 530), (2045, 1010), (0, 0, 255), 10)
                # cv2.rectangle(img, (1295, 510), (2025, 1340), (255, 0, 0), 10)
                #
                # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                # plt.savefig(settings.results_folder + settings.data_type + '/' + filename_no_ext + '_crop_regions.png')
                # plt.close()
                # quit()


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
