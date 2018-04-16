import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import sys
from math import log10
from scipy.optimize import minimize

np.set_printoptions(threshold=np.nan)

# select cropped images
# sky
# stratus
# cumulus
# cirrus

imageFolder = 'data_images/'
file = 'cirrus6.jpg'
img = cv2.imread(imageFolder+file)

# extract the bands
B = img[:,:,0]
G = img[:,:,1]
R = img[:,:,2]

# catch red zeros
R[R == 0] = 1

# normalized B/R
ratioBR = np.divide(B,R)
normalizedRatioBR = np.divide(ratioBR-1,ratioBR+1)

# StdDev
stDev = np.std(normalizedRatioBR)
deviationThreshold = 0.03
print('Standard deviation of the image', file,'is',stDev)
print('The deviation threshold is set to', deviationThreshold)

mean = np.mean(normalizedRatioBR)

def determineMCEThreshold(normalizedRatioBR):
    hist, bins = np.histogram(normalizedRatioBR,bins=100)
    L = len(hist)
    thresholdList = []
    for iThreshold in range(2,L):
        m1 = 0
        m2 = 0
        mu1 = 0
        mu2 = 0

        for i in range(1,iThreshold):
            m1 += i * hist[i]
            mu1 += hist[i]
        mu1 = m1 / mu1

        for i in range(iThreshold,L):
            m2 += i * hist[i]
            mu2 += hist[i]
        mu2 = m2 / mu2

        thresholdList.append(-m1*log10(mu1)-m2*log10(mu2))

    threshold = bins[np.argmin(thresholdList)]
    return threshold

if stDev <= deviationThreshold:
    # fixed thresholding
    threshold = 0.250
    print('Threshold type: fixed')
else:
    # MCE thresholding
    threshold = determineMCEThreshold(normalizedRatioBR)
    print('Threshold type: MCE')
print('The threshold is set to:',threshold)
x = (np.less(normalizedRatioBR, threshold)).astype(int)
#x = np.where(normalizedRatioBR < fixedThreshold, normalizedRatioBR, -1)

# plot
# make colormap
cmapName = 'myColorMap' ; nBins = 100
colorsBlueGrey = ['tab:blue','white'] ; colorsGreyBlue = ['white','tab:blue','#247afd']
blueToGrey = LinearSegmentedColormap.from_list(cmapName, colorsBlueGrey, N=nBins)
greyToBlue = LinearSegmentedColormap.from_list(cmapName, colorsGreyBlue, N=nBins)

gs = gridspec.GridSpec(2, 2)

ax = plt.subplot(gs[0,0])
plt.title('Original image')
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

ax = plt.subplot(gs[0,1])
plt.title('Normalized B/R image')
plt.imshow(normalizedRatioBR, cmap=greyToBlue)
plt.colorbar()
plt.clim(0,1)

ax = plt.subplot(gs[1,0])
plt.title('Segmented image')
plt.imshow(x, cmap=blueToGrey)

flatNormalizedRatioBR = normalizedRatioBR.flatten()

# flatNormalizedRatioBR = normalizedRatioBR.flatten()
# cloudHistoData = np.where(flatNormalizedRatioBR < threshold)
# skyHistoData = np.where(flatNormalizedRatioBR > threshold)
cloudHistoData = flatNormalizedRatioBR[np.where(flatNormalizedRatioBR <= threshold)]
skyHistoData = flatNormalizedRatioBR[np.where(flatNormalizedRatioBR >= threshold)]

ax = plt.subplot(gs[1,1])
plt.title('Histogram')
plt.ylabel('Frequency')
plt.xlabel('Normalized B/R Ratio')
plt.axvline(threshold, color='k', linestyle='dashed', linewidth=2, label='threshold:'+str(round(threshold, 2)))
#plt.hist(normalizedRatioBR.flatten(),100, range=[0,1])
plt.hist(cloudHistoData.flatten(),100, range=[0,1], label='cloud', normed=1, color='tab:grey')
plt.hist(skyHistoData.flatten(),100, range=[0,1], label='sky', histtype='bar', normed=1, color='tab:blue')
plt.legend()

plt.show()
plt.close()

# view image
