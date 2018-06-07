import settings
import matplotlib.pyplot as plt
import numpy as np

def histogram(data,plot_title,x_label,y_label,st_dev,threshold):
    """

    Args:
        data: input data
        plot_title: title of the histogram
        x_label: x-axis label
        y_label: y-axis label
        st_dev: standard deviation, used in histogram title
        threshold: calculated threshold value, plotted as line in histogram
    """
    plt.hist(data, settings.nbins_hybrid, density=1)
    plt.title(str(plot_title)+', st dev:'+str(st_dev))
    plt.axvline(threshold, color='k', linestyle='dashed', linewidth=2, label='threshold:' + str(round(threshold, 2)))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(settings.output_folder + '/' + plot_title + '_histogram.png')
    plt.close()

def binary(data, plot_title, threshold):
    """

    Args:
        data: input data (2D array)
        plot_title: title of the image
        threshold: threshold value, used in cloud/clear sky coloring
    """
    data_copy = data

    data[np.logical_and(data_copy >= threshold, data_copy != settings.mask_value)] = 2 #sun
    data[np.logical_and(data_copy < threshold, data_copy != settings.mask_value)] = 1 #clouds
    data[data_copy == settings.mask_value] = 0 #mask

    mynorm = plt.Normalize(vmin=0, vmax=2)

    plt.imshow(data, cmap='magma', norm=mynorm)
    plt.colorbar()
    plt.title(plot_title)
    plt.savefig(settings.output_folder+'/'+plot_title+'.png')
    plt.close()