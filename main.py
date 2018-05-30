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
import write_to_csv
import sys
import loop


def main():
    """Call processing functions and write output to file"""
    with open(settings.output_data, 'w') as fd:
        # TODO: make delimiter a variable, set it in the if/else and delcare writer only one time underneath it
        if settings.data_type == 'SWIMSEG':
            writer = csv.writer(fd, delimiter=',')
        else:
            writer = csv.writer(fd, delimiter='\t')
        write_to_csv.headers(writer)

        loop.structure(writer)

    # rename file
    copyfile(settings.output_data, settings.output_data_for_movie)

    # postprocessing step which carries out corrections for solar/horizon area
    if settings.use_postprocessing:
        postprocessor.aerosol_correction()

    # plot the sky cover comparison
    if settings.plot_sky_cover_comparison:
        plotskycover.plot()


if __name__ == '__main__':
    main()
