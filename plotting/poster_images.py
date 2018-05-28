import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


def plot(filename, img, img_tsi, imageWithOutlines):
    img = img[..., ::-1]  # convert from BGR -> RGB
    img_tsi = img_tsi[..., ::-1]  # convert from BGR -> RGB

    gs = gridspec.GridSpec(1, 2)

    plt.figure(figsize=(10, 6))

    ax1 = plt.subplot2grid((1, 2), (0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid((1, 2), (0, 1), rowspan=1, colspan=1)

    ax1.set_adjustable('box-forced')
    ax2.set_adjustable('box-forced')

    ax1.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelbottom='off',
                    labelleft='off')
    ax1.imshow(img)

    ax2.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelbottom='off',
                    labelleft='off')
    ax2.imshow(imageWithOutlines)

    plt.tight_layout()
    plt.savefig('results/poster_' + filename + '_original_TSI.png')
    plt.close()

    # HISTOGRAM
    gs = gridspec.GridSpec(1, 1)

    plt.figure(figsize=(5, 3))

    R = img[:, :, 0].flatten()
    B = img[:, :, 2].flatten()

    # convert R and B to masked numpy arrays
    R = np.ma.masked_where(R == 0.0, R)
    B = np.ma.masked_where(B == 0.0, B)

    ratioRB = R / B

    ax1 = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
    ax1.hist(ratioRB[np.nonzero(ratioRB)], 100, range=[0, 1], normed=1)

    ax1.set_ylabel('Frequency')
    ax1.set_xlabel('R/B Ratio')

    plt.tight_layout()

    plt.savefig('results/poster_' + filename + '_histogram.eps')
    plt.close()
