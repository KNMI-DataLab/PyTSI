import os as os
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
import matplotlib.gridspec as gridspec
from sklearn import preprocessing
import sys
import timeit
from math import log10
from scipy.optimize import minimize
import time as time
import numpy.ma as ma # masked matrix operations
import ephem
import math
import csv


np.set_printoptions(threshold=np.nan)
np.seterr(divide='ignore', invalid='ignore')

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
	if threshold <= -0.5:
		print('histogram data:')
		print(hist)
		print('ERROR threshold smaller or equal to 0')
		sys.exit('MYSTOP')

	return threshold

def setHYTAThreshold(img,xres,yres):
	# set variable(s)
	# setups: 1) devThr: 0.065, fixThr: 0.20
	#         2) devThr: 0.03 , fixThr: 0.20
	#         2) devThr: 0.03 , fixThr: 0.25
	deviationThreshold = 0.04 # original was 0.03 , 'high:0.065'
	fixedThreshold = 0.2     # original was 0.250, 'high:0.20'
	nbins = 200

	maskValue = -1

	# extract blue and red bands
	R = np.zeros((xres,yres),dtype=int)
	B = np.zeros((xres,yres),dtype=int)

	R = img[:,:,0].astype(int)
	B = img[:,:,2].astype(int)

	R_m = ma.masked_equal(R,0,copy=True)
	B_m = ma.masked_equal(B,0,copy=True)

	ratioBR = np.zeros((xres,yres),dtype=np.float64)

	# for i in range(0,xres):
	# 	for j in range(0,yres):
	# 		if R[i,j]>0:
	# 			ratioBR[i,j] = B[i,j]/R[i,j]
	# 		else:
	# 			ratioBR[i,j] = maskValue

	ratioBR = np.divide(B_m,R_m)

	# normalized B/R ratio
	normalizedRatioBR = np.zeros((xres,yres),dtype=np.float64)
	# for i in range(0,xres):
	# 	for j in range(0,yres):
	# 		if ratioBR[i,j]!=maskValue:
	# 			normalizedRatioBR[i,j] = (ratioBR[i,j]-1) / (ratioBR[i,j]+1)
	# 		else:
	# 			normalizedRatioBR[i,j] = maskValue

	normalizedRatioBR = np.divide(ratioBR-1,ratioBR+1)

	# catch Nan
	if np.argwhere(np.isnan(normalizedRatioBR)).any() == True:
		print('NaN found in normalized B/R ratios')
		sys.exit('MYSTOP')

	# convert 2D array to 1D array
	flatNormalizedRatioBR = normalizedRatioBR.flatten()

	# remove zeros from 1D array
	flatNormalizedRatioBRNoZeros = flatNormalizedRatioBR[np.nonzero(flatNormalizedRatioBR)]

	# calculate standard deviation
	st_dev = np.std(flatNormalizedRatioBRNoZeros)

	# calculate mean
	mean = np.mean(flatNormalizedRatioBRNoZeros)

	# decide which thresholding needs to be used
	if st_dev <= deviationThreshold:
		# fixed thresholding
		threshold = fixedThreshold
	else:
		# MCE thresholding
		threshold = determineMCEThreshold(flatNormalizedRatioBRNoZeros,nbins)

	return maskValue,threshold,normalizedRatioBR,flatNormalizedRatioBRNoZeros,st_dev

directory_in_str = '/nobackup/users/mos/bbc.knmi.nl/MEMBERS/knmi/datatransfer/mobotix/vectrontest/2018/05/02/allday/'
#directory_in_str = '/nobackup/users/mos/mobotix_test_images/'

# load one test image to get resolution from and create static mask part
img = cv2.imread('/nobackup/users/mos/bbc.knmi.nl/MEMBERS/knmi/datatransfer/mobotix/vectrontest/2018/05/03/06/m180503065237523.jpg')

cropVal1 = 75
cropVal2 = 2047
cropVal3 = 210
cropVal4 = 2225

widthX = cropVal4-cropVal3
widthY = cropVal2-cropVal1

radiusMask = 850
white = (255,255,255)
black = (0,0,0)

path = os.fsencode(directory_in_str)

# only use file at each xth iteration
useFiles = 4

# initialize the observer object
camera = ephem.Observer()

# location and elevation of the Mobotix camera at Cabauw
camera.lat = '51.968243'
camera.lon = '4.927675'
camera.elevation = 1 # meter

azimuthL = []
altitudeL = []
cloudCoverL = []

for i,file in enumerate(tqdm(sorted(os.listdir(path)))):
	filename = os.fsdecode(file)
	if i%useFiles !=0:
		continue

	# solar position calculations
	year   = int('20'+filename[1:3])
	month  = int(filename[3:5])
	day    = int(filename[5:7])
	hour   = int(filename[7:9])
	minute = int(filename[9:11])
	second = int(filename[11:13])
	#micrsc = int(filename[13:16])*1000

	camera.date= str(year)+'/'+str(month)+'/'+str(day)+' '+str(hour-2)+':'+str(minute)+':'+str(second)

	v = ephem.Sun(camera)

	azimuth = math.degrees(float(repr(v.az)))
	altitude = math.degrees(float(repr(v.alt)))

	if altitude < 10:
		continue

	if filename.endswith(".jpg"):
		azimuthL.append(azimuth)
		altitudeL.append(altitude)

		img = cv2.imread(directory_in_str+filename)
		img = img[75:2047,210:2225,:]

		xres,yres,n_colors = img.shape
		mask = np.zeros(img.shape, dtype='uint8')
		cv2.circle(mask, (int(xres/2),int(yres/2)), radiusMask, white, -1)

		img = img[...,::-1]

		masked = cv2.bitwise_and(img,mask)

		cv2.line(masked, (828,457), (693,96), black, 35)

		maskValue,threshold,normalizedRatioBR,flatNormalizedRatioBRNoZeros,st_dev = setHYTAThreshold(masked,xres,yres)

		sunpixels = ma.masked_less(normalizedRatioBR,threshold,copy=True).count()
		cldpixels = ma.masked_greater_equal(normalizedRatioBR,threshold,copy=True).count()

		cloudCover = cldpixels / (sunpixels + cldpixels)
		cloudCoverL.append(cloudCover)

		skycoverimage = np.zeros((xres,yres))
		#2 is cloud, 1 is sun, 0 is mask
		skycoverimage = np.where(normalizedRatioBR!=maskValue,
						np.where(normalizedRatioBR>=threshold,2,1),0)

		print('azimuth:',azimuth,'altitude:',altitude,'date',camera.date,'cloud cover:',cloudCover)

		# PLOTTING #############################################################
		plot = True
		if plot == True:

			gs = gridspec.GridSpec(1, 4)

			plt.figure(figsize=(16,5))

			ax1 = plt.subplot2grid((1,4), (0,0), rowspan=1, colspan=1)
			ax2 = plt.subplot2grid((1,4), (0,1), rowspan=1, colspan=1)
			ax3 = plt.subplot2grid((1,4), (0,2), rowspan=1, colspan=1)
			ax4 = plt.subplot2grid((1,4), (0,3), rowspan=1, colspan=1)

			ax2.set_facecolor('black')
			ax3.set_facecolor('black')

			ax1.set_adjustable('box-forced')
			ax2.set_adjustable('box-forced')
			ax3.set_adjustable('box-forced')
			ax4.set_adjustable('box-forced')

			ax4.axvline(threshold,label='threshold,'+str(threshold),color='black')
			ax4.axvline(threshold,label='st_dev,'+str(st_dev),color='black')

			ax4.legend()

			ax1.imshow(img)
			ax1.set_title('original')
			ax2.imshow(normalizedRatioBR)
			ax2.set_title('normalized R/B ratio')
			ax3.imshow(skycoverimage)
			ax3.set_title('HYTA,'+str(st_dev))
			ax4.hist(flatNormalizedRatioBRNoZeros,bins=200,range=(-0.5,1),normed=True)
			plt.tight_layout()
			plt.savefig('/nobackup/users/mos/results/mobotix_hyta/'+filename)
			plt.close()

res = zip(azimuthL,altitudeL,cloudCoverL)

with open('mobotix_cloud_cover.csv', 'w') as f:
	writer = csv.writer(f, lineterminator='\n',delimiter='\t')
	for val in res:
		writer.writerow(val)
