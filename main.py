import csv
import settings
import plotskycover
import postprocessor
from shutil import copyfile
import write_to_csv
import loop
import machine_learning


def main():
    """Call processing functions and write output to file"""

    if settings.use_processing_loop:
        with open(settings.output_data, 'w') as fd:
            if settings.data_type == 'SEG':
                delimiter = ','
            else:
                delimiter = '\t'

            writer = csv.writer(fd, delimiter=delimiter)

            write_to_csv.headers(writer)

            loop.structure(writer)

    # rename file
    copyfile(settings.output_data, settings.output_data_for_movie)

    # postprocessing step which carries out corrections for solar/horizon area
    if settings.use_postprocessing:
        postprocessor.aerosol_correction()

    if settings.use_machine_learning:
        if settings.use_knn:
            machine_learning.knn()
        elif settings.use_kmeans:
            machine_learning.k_means()

    # plot the sky cover comparison
    if settings.plot_sky_cover_comparison:
        plotskycover.plot()


if __name__ == '__main__':
    main()
