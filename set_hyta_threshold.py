# DESCRIPTION: set the HYTA threshold. follows approach from Li et al

import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import sys
import timeit
from math import log10
from scipy.optimize import minimize

np.set_printoptions(threshold=np.nan)

def determineMCEThreshold(data,nbins):
	# create the histogram and determine length
	hist, bins = np.histogram(data,nbins)
	L = len(hist)

	thresholdList = []

	# catch zeros which cause error if not changed to one
	if hist[1]==0:
		hist[1]=1
	if hist[L-2]==0:
		hist[L-2]=1

	for iThreshold in range(2,L):
		m1 = 0
		m2 = 0
		mu1 = 0
		mu2 = 0

		for i in range(1,iThreshold):
			m1 += i * hist[i]
			mu1 += hist[i]

		for i in range(iThreshold,L):
			m2 += i * hist[i]
			mu2 += hist[i]

		mu1 = m1 / mu1
		mu2 = m2 / mu2

		thresholdList.append(-m1*log10(mu1)-m2*log10(mu2))

	# minimum of the list is the threshold
	threshold = bins[np.argmin(thresholdList)]

	# catch miscalculation
	if threshold <= 0:
		print('histogram data:',hist)
		print('ERROR threshold smaller or equal to 0')
		sys.exit('MYSTOP')

	return threshold

def setHYTAThreshold(img):
	# set variable(s)
	deviationThreshold = 0.065 # original was 0.03
	fixedThreshold = 0.20 # original was 0.250
	nbins = 100

	yres,xres,nColors = img.shape
	ratioBR = np.zeros([yres,xres],dtype=float)

	# extract blue and red bands
	B = np.zeros((xres,yres),dtype=int)
	R = np.zeros((xres,yres),dtype=int)
	B = img[:,:,0].astype(int)
	R = img[:,:,2].astype(int)

	# calculate the blue/red ratio
	for i in range (0,yres):
		for j in range (0,xres):
			if R[i,j]!=0 and B[i,j]!=0:
				ratioBR[i,j]=B[i,j]/R[i,j]

	# normalized B/R ratio
	normalizedRatioBR = np.zeros(ratioBR.shape,dtype=float)

	# catch Nan
	if np.argwhere(np.isnan(normalizedRatioBR)).any() == True:
		print('NaN found in B/R ratios')
		sys.exit('MYSTOP')

	for i in range(0,yres):
		for j in range(0,xres):
			if ratioBR[i,j]!=0:
				normalizedRatioBR[i,j] = (ratioBR[i,j]-1)/(ratioBR[i,j]+1)
	# catch Nan
	if np.argwhere(np.isnan(normalizedRatioBR)).any() == True:
		print('NaN found in normalized B/R ratios')
		sys.exit('MYSTOP')

	# convert 2D array to 1D array
	flatNormalizedRatioBR = normalizedRatioBR.flatten()

	# remove zeros from 1D array
	flatNormalizedRatioBRNoZeros = flatNormalizedRatioBR[np.nonzero(flatNormalizedRatioBR)]

	# calculate standard deviation
	stDev = np.std(flatNormalizedRatioBRNoZeros)

	# calculate mean
	mean = np.mean(flatNormalizedRatioBRNoZeros)

	# decide which thresholding needs to be used
	if stDev <= deviationThreshold:
		# fixed thresholding
		threshold = fixedThreshold
	else:
		# MCE thresholding
		threshold = determineMCEThreshold(flatNormalizedRatioBRNoZeros,nbins)

	# calculate the amount of sunny and cloudy pixels when using HYTA
	sunPixels =   (flatNormalizedRatioBRNoZeros > threshold).sum()
	cloudPixels = (flatNormalizedRatioBRNoZeros < threshold).sum()

	return threshold,cloudPixels,sunPixels,flatNormalizedRatioBRNoZeros,stDev
