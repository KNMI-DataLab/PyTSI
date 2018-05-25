# DESCRIPTION: main function. loops over files, calls other functionsand writes
#              data to file(s)

import cv2
import gzip
import os
import csv
from tqdm import tqdm
from processor import processor
import statistical_analysis
import plotskycover
import postprocessor
import resolution
import settings
import read_properties_file
from shutil import copyfile


def main():
    """Call processing functions and write output to file"""
    # initiate variables
    # directory in which the data is located
    directory_in_str = settings.main_data

    # converts the directory from string into 'bytes'
    directory = os.fsencode(directory_in_str)

    # alphabetically sort the files in the directory
    sorted_directory = sorted(os.listdir(directory))

    # the '0' is added to exclude some files in the directory
    properties_extension = '0.properties.gz'
    jpg_extension = '0.jpg'
    png_extension = '0.png'

    # open the data file
    with open('data.csv', 'w') as fd:
        writer = csv.writer(fd, delimiter='\t')
        # write headers to file
        writer.writerow(['filename', 'altitude', 'azimuth',
                         'thinSkyCover', 'opaqueSkyCover', 'fractionalSkyCover',
                         'fractionalSkyCoverHYTA',
                         'thinSkyCoverTSI', 'opaqueSkyCoverTSI', 'fractionalSkyCoverTSI',
                         'energy', 'entropy', 'contrast', 'homogeneity',
                         'outsideC', 'outsideS', 'horizonC', 'horizonS',
                         'innerC', 'innerS', 'sunC', 'sunS'])

        # look for the file names
        for file in tqdm(sorted_directory):
            # decode the filename from bytes to string
            filename = os.fsdecode(file)
            # search for all files ending with particular extension
            if filename.endswith(properties_extension):
                # unzip the gzip file, open the file as rt=read text
                with gzip.open(directory_in_str + '/' + filename, 'rt') as f:
                    lines = []
                    # read the file and store line per line
                    for line in f:
                        lines.append(line)
                    # get the altitude and azimuth from the defs
                    altitude = read_properties_file.get_altitude(lines)
                    azimuth = read_properties_file.get_azimuth(lines)

                    # only carry out calculations for solar angle > 10 degrees
                    # this strategy is proposed by Long et al
                    if altitude >= settings.minimum_altitude:
                        # get the fractional sky cover from 'old' TSI software
                        thin_sky_cover_tsi, opaque_sky_cover_tsi, fractional_sky_cover_tsi = read_properties_file.get_fractional_sky_cover_tsi(
                            lines)

                        # read the image
                        img = cv2.imread(
                            directory_in_str + '/' + filename.replace(properties_extension, jpg_extension))
                        img_tsi = cv2.imread(
                            directory_in_str + '/' + filename.replace(properties_extension, png_extension))

                        # get the resolution of the image
                        resolution.get_resolution(img)

                        # main processing function
                        (thin_sky_cover, opaque_sky_cover, fractionalSkyCover,
                         fractional_sky_cover_hybrid, maskedImg, outsideC,
                         outsideS, horizonC, horizonS,
                         innerC, innerS, sunC, sunS) = processor(img, img_tsi, azimuth, altitude,
                                                                 filename.replace(properties_extension, ''))

                        # calculate statistical properties of the image
                        if settings.use_statistical_analysis:
                            energy, entropy, contrast, homogeneity = statistical_analysis.calculate_features(
                                maskedImg)
                        else:
                            energy = entropy = contrast = homogeneity = 0

                        # write data to file
                        writer.writerow((filename.replace(properties_extension, ''),
                                         altitude, azimuth,
                                         thin_sky_cover, opaque_sky_cover, fractionalSkyCover,
                                         fractional_sky_cover_hybrid,
                                         thin_sky_cover_tsi, opaque_sky_cover_tsi, fractional_sky_cover_tsi,
                                         energy, entropy, contrast, homogeneity,
                                         outsideC, outsideS, horizonC, horizonS,
                                         innerC, innerS, sunC, sunS
                                         ))

    # rename file
    copyfile('data.csv', 'data_for_completeplot.csv')

    # postprocessing step which carries out corrections for solar/horizon area
    if settings.use_postprocessing:
        postprocessor.aerosol_correction()

    # plot the sky cover comparison
    if settings.plot_sky_cover_comparison:
        plotskycover.plot()


if __name__ == '__main__':
    main()
