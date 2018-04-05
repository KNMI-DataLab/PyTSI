import numpy as np 
from sklearn import preprocessing, model_selectrion, neighbors
import pandas as pd
import cv2 as cv2
from math import log, sqrt
import sys as sys
import csv
import os
from tqdm import tqdm

# five folders: data/swimcat/(A-sky,B-pattern,C-thick-dark,D-thick-white,E-veil)/images/*.png

# load the image and file name

# extract the bands
def extractBands(img,scaler):
	# extract R and B band individually from image
	# the arrays are set up in [y,x] orientation because the image
	# has some 'special' metadata which shows opposite resolution/geometry
	# view with: "$ identify -verbose data/20170419133000.jpg"
	blueBand  = np.zeros([yres,xres])
	greenBand = np.zeros([yres,xres])
	redBand   = np.zeros([yres,xres])

	for i in range (0,yres):
		for j in range (0,xres):
			# i = ypixel, j = xpixel, 0,2 = blue, red
			blueBand[i,j]  = int(img[i,j,0]/scaler)
			greenBand[i,j] = int(img[i,j,1]/scaler)
			redBand[i,j]   = int(img[i,j,2]/scaler)

	return blueBand, greenBand, redBand

# calculate the GLCM matrix
def calculateGLCM(blueBand, greyLevels):
	# matrix elements represent relative frequence that two pixels occur
	# separated in a defined direction by distance dx,dy (A. Heinle et al., 2010)
	GLCM1 = np.zeros([greyLevels,greyLevels], dtype = 'int')
	GLCM2 = np.zeros([greyLevels,greyLevels], dtype = 'int')
	GLCM3 = np.zeros([greyLevels,greyLevels], dtype = 'int')
	GLCM4 = np.zeros([greyLevels,greyLevels], dtype = 'int')

	# pixel distance
	dx = 1
	dy = 1

	# calculate min and max grey values of the blue band
	greyMin = int(np.amin(blueBand[np.nonzero(blueBand)]))
	greyMax = int(np.amax(blueBand[np.nonzero(blueBand)]))

	# specify if an average of 4 matrices should be used
	# if false: only 2 matrices are used
	use4 = True

	# compute 4 GLCM matrices, bottom right, bottom left, top left, top right
	# loop over GLCM matrix elements
	for i in range (greyMin,greyMax):
		for j in range (greyMin,greyMax):
			# loop over image pixels
			for x in range (1, yres-1):
				for y in range (1, xres-1):
					# when two pixels 'match' add +1 to GLCM matrix element
					if blueBand[x,y] != i:
						continue
					else:
						if blueBand[x+dx,y+dy] == j:
							GLCM1[i,j] += 1
						if blueBand[x-dx,y-dy] == j:
							GLCM4[i,j] += 1
						if use4:
							if blueBand[x-dx,y+dy] == j:
								GLCM2[i,j] += 1
							if blueBand[x+dx,y-dy] == j:
								GLCM3[i,j] += 1												

	# calculate average of the four matrices
	# GLCM is the matrix used in textural feature analysis
	if use4:
		GLCM = (GLCM1+GLCM2+GLCM3+GLCM4)/4
	else:
		GLCM = (GLCM1+GLCM2+GLCM3+GLCM4)/2

	np.savetxt('GLCM.txt', GLCM, fmt='%3d')

	return GLCM

def calculateSpectralFeatures(redBand,greenBand,blueBand):
	N = xres*yres
	meanR = np.sum(redBand) / N
	meanG = np.sum(greenBand) / N
	meanB = np.sum(blueBand) / N
	stDev = sqrt(np.sum(np.square(np.subtract(blueBand,meanB)))/(N-1))
	skewness = np.sum(np.power(np.divide(np.subtract(blueBand,meanB),stDev),3)) / N
	diffRG = meanR - meanG
	diffRB = meanR - meanB
	diffGB = meanG - meanB

	return meanR,meanG,meanB,stDev,skewness,diffRG,diffRB,diffGB

# energy,entropy,contrast,homogeneity
def calculateTexturalFeatures(GLCM, greyLevels):
	energy = entropy = contrast = homogeneity = 0
	for i in range (0, greyLevels):
		for j in range(0, greyLevels):
			if GLCM[i,j] != 0:
				# Energy (B)
				energy      += GLCM[i,j]**2
				# Entropy (B)
				entropy     += GLCM[i,j] * log(GLCM[i,j],2)
				# Contrast (B)
				contrast    += GLCM[i,j] * (i-j)**2
				# Homogeneity (B)
				homogeneity += GLCM[i,j] / (1 + abs(i-j))
			else:
				pass

	return energy, entropy, contrast, homogeneity

# cloud cover
	# setup the numpy array, fill it with zeros
def calculateSkyCover(img, sunnyThreshold, thinThreshold):
	redBlueRatio = np.zeros([yres,xres])

	# blue red ratio calculation for each pixel in the image
	for i in range (0,yres):
		for j in range (0,xres):
			# i = ypixel, j = xpixel, 0,2 = blue, red
			redBlueRatio[i,j] = img[i,j,2] / img[i,j,0]

	sunnyPixels = 0
	thinPixels = 0
	opaquePixels = 0

	# classify each pixel as cloudy/clear
	for i in range (0,yres):
		for j in range (0,xres):
			# avoid mask
			if redBlueRatio[i,j] != 0:
				if redBlueRatio[i,j] <= sunnyThreshold:
					sunnyPixels += 1
				elif redBlueRatio[i,j] <= thinThreshold:
					thinPixels += 1
				else:
					opaquePixels += 1

	cloudyPixels = thinPixels + opaquePixels

	thinSkyCover = thinPixels / (sunnyPixels+cloudyPixels)
	opaqueSkyCover = opaquePixels / (sunnyPixels+cloudyPixels)
	fractionalSkyCover = thinSkyCover + opaqueSkyCover

	return fractionalSkyCover

# write to file: id,mean,stdev,skew,diff,energy,entropy,contrast,homogeneity,cloudcover,class
# classes:
#	- 0: sky
#	- 1: pattern
#	- 2: thick dark
#	- 3: thick white
#	- 4: veil

def main():
	global xres, yres
	xres = yres = 125

	greyLevels = 32
	scaler = int(256/greyLevels)

	sunnyThreshold = 0.795
	thinThreshold = 0.9

	dataFolder = '/home/mos/Documents/TSI/machinelearning/data/swimcat/'

	dirList = []
	dirList.append(dataFolder + 'A-sky/images')
	dirList.append(dataFolder + 'B-pattern/images/')
	dirList.append(dataFolder + 'C-thick-dark/images/')
	dirList.append(dataFolder + 'D-thick-white/images/')
	dirList.append(dataFolder + 'E-veil/images/')

	with open('data.csv', 'w', newline ='') as csvfile:
		# set up csv writing environment
		writer = csv.writer(csvfile, delimiter=',')
		for cloudClass, dirName in enumerate(dirList):
			dirName = os.fsencode(dirList[cloudClass])
			dirName = os.listdir(dirName)
			for file in tqdm(dirName):
				filename = os.fsdecode(file)
				# absolute location of the file
				fileLocation = dirList[cloudClass] + '/' + filename
				# read the image
				img = cv2.imread(fileLocation)
				# extract the bands
				blueBand, greenBand, redBand = extractBands(img,scaler)
				# calculate the GLCM
				GLCM = calculateGLCM(blueBand,greyLevels)
				# calculate the spectral features
				meanR,meanG,meanB,stDev,skewness,diffRG,diffRB,diffGB = calculateSpectralFeatures(redBand,greenBand,blueBand)
				# calculate the textural features
				energy, entropy, contrast, homogeneity = calculateTexturalFeatures(GLCM,greyLevels)
				#calculate the cloud cover
				cloudCover = calculateSkyCover(img, sunnyThreshold, thinThreshold)
				#write the data to a file
				writer.writerow((filename,meanR,meanG,meanB,stDev,skewness,diffRG,diffRB,diffGB,energy,entropy,contrast,homogeneity,cloudClass))

if __name__ == '__main__':
	main()