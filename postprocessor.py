# DESCRIPTION: cperform sun circle/horizon area corrections as postprocessing
#              the approach by Long is used

from myimports import *
from numpy import genfromtxt
from plotcorrectionresult import plot_correction_results
import csv as csv


def aerosol_correction():
    # read columns of file
    df = genfromtxt('/usr/people/mos/Documents/cloudDetection/data.csv', skip_header=1, delimiter='\t')

    azimuth = df[:, 2]
    outside_c = df[:, 14]
    outside_s = df[:, 15]
    horizon_c = df[:, 16]
    horizon_s = df[:, 17]
    inner_c = df[:, 18]
    inner_s = df[:, 19]
    sun_c = df[:, 20]
    sun_s = df[:, 21]

    n_samples = len(df[:, 0])

    # total amount of sun and cloud pixels
    sun = np.add(sun_s, np.add(horizon_s, np.add(inner_s, outside_s)))
    cloud = np.add(sun_c, np.add(horizon_c, np.add(inner_c, outside_c)))

    # total sky cover before corrections
    original_sky_cover = np.divide(cloud, (sun + cloud))

    # individual sky covers of different parts
    sun_sky_cover_indiv = np.divide(sun_c, (sun_s + sun_c))
    horizon_sky_cover_indiv = np.divide(horizon_c, (horizon_s + horizon_c))

    # what part of the total sky cover is made up of sun and horizon areas
    sun_sky_cover_partial = np.divide(sun_c, (sun + cloud))
    horizon_sky_cover_partial = np.divide(horizon_c, (sun + cloud))

    # first guess
    remainder_sky_cover = np.subtract(original_sky_cover, np.add(sun_sky_cover_partial, horizon_sky_cover_partial))

    initial_adjustment_factor = np.subtract(1, remainder_sky_cover)

    initial_adjustment_factor = np.where(initial_adjustment_factor > settings.initial_adjustment_factor_limit,
                                         settings.initial_adjustment_factor_limit,
                                         initial_adjustment_factor)

    first_guess = np.multiply(sun_c, initial_adjustment_factor)

    # calculate standard deviations
    sun_st_dev = np.zeros(n_samples)
    remainder_st_dev = np.zeros(n_samples)
    horizon_st_dev = np.zeros(n_samples)
    for i in range(0 + settings.st_dev_width, n_samples - settings.st_dev_width):
        sun_st_dev[i] = np.std(sun_sky_cover_indiv[i - settings.st_dev_width:i + settings.st_dev_width])
        remainder_st_dev[i] = np.std(remainder_sky_cover[i - settings.st_dev_width:i + settings.st_dev_width])
        horizon_st_dev[i] = np.std(horizon_sky_cover_indiv[i - settings.st_dev_width:i + settings.st_dev_width])

    cloud_corrected = np.copy(cloud)
    sun_corrected = np.copy(sun)

    # carry out corrections if criteria match
    # sun circle
    cloud_corrected = np.where(np.logical_and(sun_st_dev < settings.st_dev_limit,
                                              np.logical_and(sun_sky_cover_indiv > settings.sun_sky_cover_limit,
                                                             np.logical_and(
                                                                 remainder_sky_cover < settings.remainder_limit,
                                                                 remainder_st_dev < settings.remainder_st_dev_limit))),
                               cloud_corrected - sun_c, cloud_corrected - first_guess)

    sun_corrected = np.where(np.logical_and(sun_st_dev < settings.st_dev_limit,
                                            np.logical_and(sun_sky_cover_indiv > settings.sun_sky_cover_limit,
                                                           np.logical_and(
                                                               remainder_sky_cover < settings.remainder_limit,
                                                               remainder_st_dev < settings.remainder_st_dev_limit))),
                             sun_corrected + sun_c, sun_corrected + first_guess)

    # horizon area
    cloud_corrected = np.where(np.logical_and(horizon_st_dev < settings.st_dev_limit,
                                              np.logical_and(horizon_sky_cover_indiv > settings.horizon_sky_cover_limit,
                                                             np.logical_and(
                                                                 remainder_sky_cover < settings.remainder_limit,
                                                                 remainder_st_dev < settings.remainder_st_dev_limit))),
                               cloud_corrected - horizon_c, cloud_corrected)

    sun_corrected = np.where(np.logical_and(horizon_st_dev < settings.st_dev_limit,
                                            np.logical_and(horizon_sky_cover_indiv > settings.horizon_sky_cover_limit,
                                                           np.logical_and(
                                                               remainder_sky_cover < settings.remainder_limit,
                                                               remainder_st_dev < settings.remainder_st_dev_limit))),
                             sun_corrected + horizon_c, sun_corrected)

    # corrected sky cover
    corrected_sky_cover = np.divide(cloud_corrected, (sun_corrected + cloud_corrected))

    difference = np.subtract(original_sky_cover, corrected_sky_cover)

    # smoothing
    running_mean = np.copy(difference)

    for i in range(0 + settings.smoothing_width, n_samples - settings.smoothing_width):
        running_mean[i] = np.mean(difference[i - settings.smoothing_width:i + settings.smoothing_width])

    smooth_corrected_sky_cover = original_sky_cover - running_mean

    smooth_corrected_sky_cover[smooth_corrected_sky_cover < 0] = 0

    # plot
    if settings.plot_correction_result:
        plot_correction_results(corrected_sky_cover, smooth_corrected_sky_cover)

    # zip data and put into file
    rows = zip(azimuth, corrected_sky_cover, smooth_corrected_sky_cover)

    with open('corrections.csv', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['azimuth', 'corrected_sky_cover', 'smooth_corrected_sky_cover'])
        for row in rows:
            writer.writerow(row)
