import settings
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
from sklearn.metrics import r2_score
from math import ceil
from scipy.stats import gaussian_kde
from matplotlib import colors
import os
from matplotlib.mlab import bivariate_normal


def histogram_obj(ax, data, plot_title, x_label, y_label, st_dev, threshold):
    """Histogram object used in :meth:`plot.orignal_and_binary_and_histogram`.

    Args:
        data: input data
        plot_title: title of the histogram
        x_label: x-axis label
        y_label: y-axis label
        st_dev: standard deviation, used in histogram title
        threshold: calculated threshold value, plotted as line in histogram
    """
    ax.set_title(str(plot_title) + ', st dev:' + str(round(st_dev, 4)))
    ax.axvline(threshold, color='k', linestyle='dashed', linewidth=2, label='threshold:' + str(round(threshold, 2)))
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim([0, 10])
    out = ax.hist(data, settings.nbins_hybrid, range=[-1, 1], density=1)
    # f.savefig(settings.output_folder + plot_title + '_histogram.png')
    # plt.close()

    return out


def difference_histogram():
    data = np.genfromtxt(settings.output_data_copy, delimiter=settings.delimiter, names=True, dtype=None)

    nbins = 25

    plt.figure(figsize=(6, 4))

    # plt.xticks(np.arange(-1.1,1.1, step=0.1))

    x = data['cloud_cover_TSI']
    y = data['cloud_cover_fixed']
    diff1 = (y - x) * 100
    y = data['cloud_cover_hybrid']
    diff2 = (y - x) * 100
    plt.hist([diff1, diff2], bins=nbins, label=['Fixed', 'Hybrid'], range=(-100, 100), histtype='bar')

    plt.ylabel('Frequency')
    plt.xlabel('Difference (%)')

    plt.title('Differences between model and grount truth/TSI')
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.close()


def binary_obj(ax, data, plot_title, threshold):
    """Binary image object

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
    # f.savefig(settings.output_folder + plot_title + '.png')
    # plt.show()
    # plt.close()

    return out


def single_time_series(plot_title, x_label, y_label):
    """Plot a time series."""
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
    """Plot the original RGB image, the binary image (blue sky/cloud) and the histogram

    Args:
        img: RGB original image
        filename (str): filename
        data1: r/b or b/r grayscale image
        title1: title of the binary image
        data2: 1d array of r/b or b/r ratios
        title2: title of the histogram
        x_label2: x-axis label of histogram
        y_label2: y-axis label of histogram
        st_dev (float): stdev of histogram
        threshold (float): threshold (as determined by the hybrid algorithm
    """
    plt.figure(figsize=(16, 5))

    ax1 = plt.subplot2grid((1, 3), (0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid((1, 3), (0, 1), rowspan=1, colspan=1)
    ax3 = plt.subplot2grid((1, 3), (0, 2), rowspan=1, colspan=1)

    ax1.set_adjustable('box-forced')
    ax2.set_adjustable('box-forced')
    ax3.set_adjustable('box-forced')

    ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    binary_obj(ax2, data1, title1, threshold)
    histogram_obj(ax3, data2, title2, x_label2, y_label2, st_dev, threshold)

    plt.tight_layout()
    plt.savefig(settings.output_folder + filename + '_comparison.png')
    plt.close()


def comparison_scatter():
    """Plot the scatter of two datasets against each other with a 1:1 line, best fit and r2 score."""
    data = np.genfromtxt(settings.output_data_copy, delimiter=settings.delimiter, names=True, dtype=None)

    x_name = 'cloud_cover_hybrid_mce'
    y_name = 'cloud_cover_hybrid_otsu'
    n_name = 'filename'

    x = data[x_name]
    y = data[y_name]
    names = data[n_name]

    # convert 1D filename array to string
    # if there is an extension (.jpg/.png etc.) or the file name consists of a combination between letters and numbers
    # the filenames are read as 'byte' type. In this case, a conversion ('decode') has to be carried out.
    # in the case of an integer filename type (0001, 0002, 201805021645 etc.) a more simple conversion is applied
    names_str = []
    if names.dtype == np.dtype(int):
        for name in names:
            names_str.append(str(name))
    else:
        for name in names:
            names_str.append(name.decode('UTF-8'))
    names = names_str

    # Calculate the point density
    xy = np.vstack([x, y])
    c = gaussian_kde(xy)(xy)

    norm = colors.Normalize(0, 2)
    cmap = plt.cm.viridis

    a, b = np.polyfit(x, y, 1)

    a = ceil(a * 100) / 100
    b = ceil(b * 100) / 100

    x_fit = np.array([-1, 2])
    y_fit = a * x_fit + b

    fig, ax = plt.subplots(figsize=(6, 6))
    sc = ax.scatter(x, y, c=c, cmap=cmap, norm=norm, s=10)

    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):

        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}".format(" ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])

    ax.plot(x_fit, y_fit, c='black', linewidth=3, label='y=' + str(a) + 'x+' + str(b), linestyle='--')
    ax.plot([-1, 2], [-1, 2], c='tab:red', linewidth=3, label='y=x')
    ax.legend()
    ax.set_title('$r^2$ score:' + str(round(r2_score(x, y), 2)))
    plt.grid()
    plt.xlabel('Ground truth/TSI cloud cover')
    plt.ylabel('Model cloud cover')
    plt.show()
    plt.close()

    # plt.figure(figsize=(4,4))
    #
    #
    # plt.xlim([0, 1])
    # plt.ylim([0, 1])
    # plt.gca().set_aspect('equal', adjustable='box')
    #
    # plt.scatter(x, y, c=z, cmap=cmap, norm=norm, s=5)
    # # plt.hist2d(x,y, (100,100), cmap='jet', norm=normalize)
    # plt.grid()
    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    # plt.close()
