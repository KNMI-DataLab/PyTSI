import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
from math import log10
from scipy.optimize import minimize

# select cropped images
# sky
# stratus
# cumulus
# cirrus

imageFolder = 'data_images/'
file = 'stratus3.jpg'
img = cv2.imread(imageFolder+file)

# extract the bands
B = img[:,:,0]
G = img[:,:,1]
R = img[:,:,2]

# normalized B/R
ratioBR = np.divide(B,R)
normalizedRatioBR = np.divide(ratioBR-1,ratioBR+1)

# plot
plt.imshow(normalizedRatioBR)
plt.colorbar()
plt.show()
plt.close()

# StdDev
stDev = np.std(normalizedRatioBR)
deviationThreshold = 0.03
print('Standard deviation of the image', file,'is',stDev)
print('The deviation threshold is set to', deviationThreshold)

mean = np.mean(normalizedRatioBR)

def determineMCEThreshold(normalizedRatioBR):
    hist, bins = np.histogram(normalizedRatioBR,bins=50)
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
    hist,bin_edges = np.histogram(normalizedRatioBR, bins = 50)
    #h2,bin_edges = np.histogram(normalizedRatioBR, bins = 50)
    x0 = np.arange(0,len(hist),1)
    x0 = x0.astype(int)
    threshold = determineMCEThreshold(normalizedRatioBR)
    print('Threshold type: MCE')
print('The threshold is set to:',threshold)
x = (np.less(normalizedRatioBR, threshold)).astype(int)
#x = np.where(normalizedRatioBR < fixedThreshold, normalizedRatioBR, -1)
plt.imshow(x)
plt.colorbar()
plt.show()

# view image
