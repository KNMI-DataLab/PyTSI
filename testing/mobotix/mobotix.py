import os as os
from tqdm import tqdm
from pysolar.solar import *
import datetime as datetime
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
import matplotlib.gridspec as gridspec
from sklearn import preprocessing

np.set_printoptions(threshold=np.nan)

# location of the Mobotix camera at Cabauw
lat = 51.968243
lon = 4.927675

#directory_in_str = '/nobackup/users/mos/bbc.knmi.nl/MEMBERS/knmi/datatransfer/mobotix/vectrontest/2018/05/02/allday/'
directory_in_str = '/nobackup/users/mos/mobotix_test_images/'

# load one test image to get resolution from and create static mask part
img = cv2.imread('/nobackup/users/mos/bbc.knmi.nl/MEMBERS/knmi/datatransfer/mobotix/vectrontest/2018/05/03/06/m180503065237523.jpg')

cropVal1 = 75
cropVal2 = 2047
cropVal3 = 210
cropVal4 = 2225

widthX = cropVal4-cropVal3
widthY = cropVal2-cropVal1

threshold = 0.9
radiusMask = 850
white = (255,255,255)
black = (0,0,0)

path = os.fsencode(directory_in_str)

for i,file in enumerate(tqdm(sorted(os.listdir(path)))):
	filename = os.fsdecode(file)
	if filename.endswith(".jpg"):
		img = cv2.imread(directory_in_str+filename)
		img = img[75:2047,210:2225,:]

		xres,yres,nColors = img.shape
		mask = np.zeros(img.shape, dtype='uint8')
		cv2.circle(mask, (int(xres/2),int(yres/2)), radiusMask, white, -1)

		img = img[...,::-1]

		masked = cv2.bitwise_and(img,mask)

		cv2.line(masked, (828,457), (693,96), black, 35)

		R = masked[:,:,0]
		G = masked[:,:,1]
		B = masked[:,:,2]
		B[B==0]=1

		RBRatio = np.zeros((xres,yres),dtype=float)
		RBRatio = np.where(B>0, R/B, 0)

		sunPixels = cloudPixels = 0

		skycoverimage = np.zeros((xres,yres,nColors),dtype='uint8')
		#1 is cloud, 0.5 is sun, 0 is mask
		skycoverimage = np.where(RBRatio>0,
							 	np.where(RBRatio>=threshold,1,0.5),0)

		# PLOTTING #############################################################
		plot = True
		if plot == True:
			gs = gridspec.GridSpec(1, 3)

			plt.figure(figsize=(16,7))

			ax1 = plt.subplot2grid((1,3), (0,0), rowspan=1, colspan=1)
			ax2 = plt.subplot2grid((1,3), (0,1), rowspan=1, colspan=1)
			ax3 = plt.subplot2grid((1,3), (0,2), rowspan=1, colspan=1)

			ax1.set_adjustable('box-forced')
			ax2.set_adjustable('box-forced')
			ax3.set_adjustable('box-forced')

			ax1.imshow(img)
			ax1.set_title('original')
			ax2.imshow(RBRatio)
			ax2.set_title('R/B ratio')
			ax3.imshow(skycoverimage)
			ax3.set_title('fixed')
			plt.tight_layout()
			#plt.savefig('/nobackup/users/mos/results/mobotix/'+filename)\
			plt.savefig('/nobackup/users/mos/results/mobotix_testing/'+filename)
			plt.close()
