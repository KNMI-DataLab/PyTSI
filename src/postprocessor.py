import numpy as np
import matplotlib.pyplot as plt
import csv as csv
import settings


def aerosol_correction():
    """Perform the horizon area/sun circle correction.

    The data from the main processing loop is used which is then subjected to a few steps. The approach by Long 2010
    is used. Several statistical features of the segmetns are tested against a set of thresholds defined in
    :meth:`settings`. Subsequently, the corrected sky cover percentages are written to a file.
    """
    # read columns of file
    df = np.genfromtxt(settings.output_data_copy, skip_header=1, delimiter=settings.delimiter)

    azimuth = df[:, 3]
    outside_c = df[:, 17]
    outside_s = df[:, 18]
    horizon_c = df[:, 19]
    horizon_s = df[:, 20]
    inner_c = df[:, 21]
    inner_s = df[:, 22]
    sun_c = df[:, 23]
    sun_s = df[:, 24]

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

    # zip data and put into file
    rows = zip(azimuth, original_sky_cover, corrected_sky_cover, smooth_corrected_sky_cover)

    with open(settings.project_folder + 'cloud_detection/cloudDetection/output_data/corrections.csv', 'w') as f:
        writer = csv.writer(f, delimiter=settings.delimiter)
        writer.writerow(['azimuth', 'original_sky_cover', 'corrected_sky_cover', 'smooth_corrected_sky_cover'])
        for row in rows:
            writer.writerow(row)

    plt.figure(figsize=(8,3))
    plt.ylim((-0.01,0.15))
    plt.ylabel('Cloud cover')
    plt.xlabel('Azimuth (deg)')
    plt.grid()
    plt.plot(azimuth, original_sky_cover, label='Original cloud cover')
    plt.plot(azimuth, smooth_corrected_sky_cover, label='Corrected cloud cover')
    plt.legend(loc= 'upper center',ncol=2)
    plt.tight_layout()
    #plt.savefig('/usr/people/mos')
    plt.show()
    plt.close()