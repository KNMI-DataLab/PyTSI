import settings
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2


def histogram(ax, data, plot_title, x_label, y_label, st_dev, threshold):
    """

    Args:
        data: input data
        plot_title: title of the histogram
        x_label: x-axis label
        y_label: y-axis label
        st_dev: standard deviation, used in histogram title
        threshold: calculated threshold value, plotted as line in histogram
    """
    ax.set_title(str(plot_title) + ', st dev:' + str(st_dev))
    ax.axvline(threshold, color='k', linestyle='dashed', linewidth=2, label='threshold:' + str(round(threshold, 2)))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim([0, 10])
    out = ax.hist(data, settings.nbins_hybrid, range=[-1, 1], density=1)
    #f.savefig(settings.output_folder + plot_title + '_histogram.png')
    #plt.close()

    return out

def binary(ax,data, plot_title, threshold):
    """

    Args:
        data: input data (2D array)
        plot_title: title of the image
        threshold: threshold value, used in cloud/clear sky coloring
    """
    data_copy = data

    data[np.logical_and(data_copy >= threshold, data_copy != settings.mask_value)] = 2  # sun
    data[np.logical_and(data_copy < threshold, data_copy != settings.mask_value)] = 1  # clouds
    data[data_copy == settings.mask_value] = 0  # mask

    mynorm = plt.Normalize(vmin=1, vmax=2)

    ax.set_title(plot_title)
    out = ax.imshow(data, cmap='Blues', norm=mynorm)
    #f.savefig(settings.output_folder + plot_title + '.png')
    # plt.show()
    #plt.close()

    return out


def single_time_series(plot_title, x_label, y_label):
    if settings.data_type == 'mobotix':
        data = np.genfromtxt('data.csv', delimiter=settings.delimiter, names=True)
        plt.plot(data['azimuth'], data['cloud_cover'])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.savefig(settings.output_folder + plot_title + '_sky_cover_time_series.png')
        plt.show()
        plt.close()


def original_and_binary_and_histogram(img, filename, data1, title1, data2, title2, x_label2, y_label2,
                                      st_dev, threshold):
    plt.figure(figsize=(16, 5))

    ax1 = plt.subplot2grid((1, 3), (0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid((1, 3), (0, 1), rowspan=1, colspan=1)
    ax3 = plt.subplot2grid((1, 3), (0, 2), rowspan=1, colspan=1)

    ax1.set_adjustable('box-forced')
    ax2.set_adjustable('box-forced')
    ax3.set_adjustable('box-forced')

    ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    binary(ax2,data1, title1, threshold)
    histogram(ax3,data2, title2, x_label2, y_label2, st_dev, threshold)

    plt.tight_layout()
    plt.savefig(settings.output_folder+filename+'_comparison.png')
    plt.close()