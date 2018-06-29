import csv
import settings
import plotskycover
import postprocessor
from shutil import copyfile
import write_to_csv
import loop
import machine_learning
import plot
import crop
import image_interface


def main():
    """Call mainn functions and write output to file.

    First is the call to the processing loop. Afterwards, postprocessing, machine learning and cropping functionality
    are carried out (specified in settings file). Finally, some plotting functions are called.
    """

    if settings.use_processing_loop:
        with open(settings.output_data, 'w') as fd:
            writer = csv.writer(fd, delimiter=settings.delimiter)

            write_to_csv.headers(writer)

            loop.structure(writer)

            # rename file
            copyfile(settings.output_data, settings.output_data_copy)

    # postprocessing step which carries out corrections for solar/horizon area
    if settings.use_postprocessing:
        postprocessor.aerosol_correction()

    if settings.use_machine_learning:
        if settings.use_knn:  # k nearest neighbor
            machine_learning.knn()
        elif settings.use_kmeans: # k means
            machine_learning.k_means()

    # recursively crop all the mobotix images within directory
    if settings.crop_mobotix_images:
        crop.mobotix()

    # plot the sky cover comparison
    if settings.plot_sky_cover_comparison:
        plotskycover.plot()

    # plot time series
    if settings.plot_sky_cover_time_series:
        plot.single_time_series('sky_cover_time_series', 'azimuth', 'cloud cover (%)')

    # scatter plot comparing ground truth/old software vs new software
    if settings.plot_comparison_scatter:
        plot.comparison_scatter()

    # histogram of the differences between ground truth/old software and new software
    if settings.plot_difference_histogram:
        plot.difference_histogram()


if __name__ == '__main__':
    main()
