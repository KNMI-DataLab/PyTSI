import numpy as np
from matplotlib import pyplot as plt
import settings


def plot(img, imgTSI, regions, imageWithOutlines, imageWithOutlinesHYTA, azimuth, flatNormalizedRatioBRNoZeros,
         threshold, st_dev, filename):
    current_azimuth = azimuth

    data = np.genfromtxt('output_data/dataTSI.csv', delimiter=settings.delimiter, names=True)
    corrections = np.genfromtxt('output_data/corrections.csv', delimiter=settings.delimiter, names=True)
    # mobotix = np.genfromtxt('/nobackup/users/mos/testing/mobotix/mobotix_cloud_cover.csv', delimiter='\t')

    plt.figure(figsize=(16, 9))

    ax1 = plt.subplot2grid((3, 10), (0, 0), rowspan=1, colspan=2)
    ax2 = plt.subplot2grid((3, 10), (0, 2), rowspan=1, colspan=2)
    ax3 = plt.subplot2grid((3, 10), (0, 4), rowspan=1, colspan=2)
    ax4 = plt.subplot2grid((3, 10), (0, 6), rowspan=1, colspan=2)
    ax5 = plt.subplot2grid((3, 10), (0, 8), rowspan=1, colspan=2)
    ax6 = plt.subplot2grid((3, 10), (1, 0), rowspan=2, colspan=3)
    ax7 = plt.subplot2grid((3, 10), (1, 3), rowspan=1, colspan=6)
    ax8 = plt.subplot2grid((3, 10), (2, 3), rowspan=1, colspan=6)

    ax1.set_adjustable('box-forced')
    ax2.set_adjustable('box-forced')
    ax3.set_adjustable('box-forced')
    ax4.set_adjustable('box-forced')
    ax5.set_adjustable('box-forced')

    img = img[..., ::-1]  # convert from BGR -> RGB
    imgTSI = imgTSI[..., ::-1]  # convert from BGR -> RGB

    ax1.tick_params(axis='both', which='both', bottom='off', top='off',
                    left='off', right='off', labelbottom='off', labelleft='off')
    ax1.set_title('Original image')
    ax1.imshow(img)

    ax2.tick_params(axis='both', which='both', bottom='off', top='off',
                    left='off', right='off', labelbottom='off', labelleft='off')
    ax2.set_title('Old software')
    ax2.imshow(imgTSI)

    ax3.tick_params(axis='both', which='both', bottom='off', top='off',
                    left='off', right='off', labelbottom='off', labelleft='off')
    ax3.set_title('New segments')
    ax3.imshow(regions)

    ax4.tick_params(axis='both', which='both', bottom='off', top='off',
                    left='off', right='off', labelbottom='off', labelleft='off')
    ax4.set_title('Fixed')
    ax4.imshow(imageWithOutlines)

    ax5.tick_params(axis='both', which='both', bottom='off', top='off',
                    left='off', right='off', labelbottom='off', labelleft='off')
    ax5.set_title('HYTA')
    ax5.imshow(imageWithOutlinesHYTA)

    nbins = 100
    ax6.set_title('Histogram st_dev=' + str(st_dev))
    ax6.set_ylabel('Frequency')
    ax6.set_xlabel('Normalized B/R Ratio')
    ax6.set_ylim([0, 30])
    ax6.axvline(threshold, color='k', linestyle='dashed', linewidth=2, label='threshold:' + str(round(threshold, 2)))
    ax6.hist(flatNormalizedRatioBRNoZeros, nbins, range=[0, 1], density=1)
    ax6.legend()

    ax7.plot(data['azimuth'], data['cloud_cover_TSI'] * 100,
             color='tab:red', label='Old', linewidth=2.0)
    ax7.plot(data['azimuth'], data['cloud_cover_fixed'] * 100,
             color='tab:green', label='New', linewidth=2.0)
    ax7.plot(data['azimuth'], data['cloud_cover_hybrid'] * 100,
             color='tab:purple', label='HYTA', linewidth=2.0)
    ax7.plot(data['azimuth'], corrections['corrected_sky_cover'] * 100,
             color='tab:blue', label='Corrected', linewidth=2.0)
    ax7.plot(data['azimuth'], corrections['smooth_corrected_sky_cover'] * 100,
             color='tab:orange', label='Smoothened', linewidth=2.0)
    # ax7.plot(mobotix[:, 0], mobotix[:, 2] * 100,
    #          color='tab:pink', label='Mobotix', linewidth=2.0)
    ax7.axvline(current_azimuth, color='k', linestyle='dashed', linewidth=2, label='azimuth')
    ax7.set_title('Cloud cover. Current azimuth=' + str(current_azimuth))
    ax7.legend(bbox_to_anchor=(1.005, 0.9), loc=2, borderaxespad=0.)

    ax7.set_ylabel('absolute (%)')
    ax7.set_ylim([-5, 105])
    ax7.grid()

    ax8.plot(data['azimuth'], abs((data['cloud_cover_TSI'] - data['cloud_cover_fixed']) * 100),
             color='tab:green', label='Old-new', linewidth=2.0)
    ax8.plot(data['azimuth'], abs((data['cloud_cover_TSI'] - data['cloud_cover_hybrid']) * 100),
             color='tab:purple', label='Old-HYTA', linewidth=2.0)
    ax8.plot(data['azimuth'], abs((data['cloud_cover_TSI'] - corrections['corrected_sky_cover']) * 100),
             color='tab:blue', label='Old-corrected', linewidth=2.0)
    ax8.plot(data['azimuth'], abs((data['cloud_cover_TSI'] - corrections['smooth_corrected_sky_cover']) * 100),
             color='tab:orange', label='Old-smoothened', linewidth=2.0)
    ax8.axvline(current_azimuth, color='k', linestyle='dashed', linewidth=2, label='azimuth')
    ax8.legend(bbox_to_anchor=(1.005, 0.7), loc=2, borderaxespad=0.)

    ax8.set_ylabel('difference (%)')
    ax8.set_xlabel('azimuth (deg)')
    ax8.set_ylim([-5, 105])
    ax8.grid()

    plt.tight_layout()

    plt.savefig(settings.results_folder + 'TSI/movie_images/' + filename)
    plt.close()
