###############################################################################
# DESCRIPTION: calculates various statistical properties of the image.
#              the statistical features provide information about the type
#              of cloud (texture)
#              these properties are used in the machine learning algorithm to
#              examine accuracy
# AUTHOR: Job Mos			            # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *

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

	# reset resolutions for GLCM calculation
	xres = 352
	yres = 288

	# calculate min and max grey values of the blue band
	greyMin = int(np.amin(blueBand[np.nonzero(blueBand)]))
	greyMax = int(np.amax(blueBand[np.nonzero(blueBand)]))

	# FOLLOWING CALCULATION TAKES A LARGE AMOUNT OF TIME
	# 'scaler' is used to decrease amount of grey levels and thus
	# reduces computation time
	# scaler=1 is full 256 grey levels

	# calculate the GLCM matrix
	# loop over GLCM matrix elements
	for i in range (greyMin,greyMax):
		for j in range (greyMin,greyMax):
			print(i,j)
			# loop over image pixels
			for x in range (0, xres):
				for y in range (0, yres):
					# GLCM1
					# check whether on pixel is part of mask
					# if pixel is masked, do nothing
					if blueBand[x,y] == 0 or blueBand[x+dx,y+dy] == 0:
						pass
					else:
						# when two pixels 'match' add +1 to GLCM matrix element
						if blueBand[x,y] == i and blueBand[x+dx,y+dy] == j:
							GLCM1[i,j] += 1
							#print(GLCM[i,j])
						else:
							pass
					# GLCM2
					# check whether on pixel is part of mask
					# if pixel is masked, do nothing
					if blueBand[x,y] == 0 or blueBand[x-dx,y+dy] == 0:
						pass
					else:
						# when two pixels 'match' add +1 to GLCM matrix element
						if blueBand[x,y] == i and blueBand[x-dx,y+dy] == j:
							GLCM2[i,j] += 1
							#print(GLCM[i,j])
						else:
							pass
					# GLCM3
					# check whether on pixel is part of mask
					# if pixel is masked, do nothing
					if blueBand[x,y] == 0 or blueBand[x+dx,y-dy] == 0:
						pass
					else:
						# when two pixels 'match' add +1 to GLCM matrix element
						if blueBand[x,y] == i and blueBand[x+dx,y-dy] == j:
							GLCM3[i,j] += 1
							#print(GLCM[i,j])
						else:
							pass
					# GLCM4
					# check whether on pixel is part of mask
					# if pixel is masked, do nothing
					if blueBand[x,y] == 0 or blueBand[x-dx,y-dy] == 0:
						pass
					else:
						# when two pixels 'match' add +1 to GLCM matrix element
						if blueBand[x,y] == i and blueBand[x-dx,y-dy] == j:
							GLCM4[i,j] += 1
							#print(GLCM[i,j])
						else:
							pass														

	GLCM = (GLCM1+GLCM2+GLCM3+GLCM4)/4
	
	np.savetxt('GLCM1.txt', GLCM1, fmt='%3d')
	np.savetxt('GLCM2.txt', GLCM2, fmt='%3d')
	np.savetxt('GLCM3.txt', GLCM3, fmt='%3d')
	np.savetxt('GLCM4.txt', GLCM4, fmt='%3d')

	np.savetxt('GLCM.txt', GLCM, fmt='%3d')

	return 0

def performStatisticalAnalysis(maskedImg):

	#set the number of grey levels used in the GLCM calculation
	greyLevels = 16
	scaler = int(256/greyLevels)

	xres = 288
	yres = 352

	# extract R and B band individually from image
	blueBand  = np.zeros([yres,xres])
	greenBand = np.zeros([yres,xres])
	redBand   = np.zeros([yres,xres])

	for i in range (0,yres):
		for j in range (0,xres):
			# check whether on pixel is part of mask
			# if pixel is masked, do nothing
			if maskedImg[i,j,0] == 0 and maskedImg[i,j,1] == 0 and maskedImg[i,j,2] == 0:
				pass
			else:
				# i = ypixel, j = xpixel, 0,2 = blue, red
				blueBand[i,j]  = int(maskedImg[i,j,0]/scaler)
				greenBand[i,j] = int(maskedImg[i,j,1]/scaler)
				redBand[i,j]   = int(maskedImg[i,j,2]/scaler)

	# SPECTRAL FEATURES

	# mean (R and B)

	# standard deviation (B)

	# skewness (B)

	# difference (R-G, R-B and G-B)

	# TEXTURAL FEATURES

	# Grey Level Co-occurrence Matrices (GLCM)
	GLCM = calculateGLCM(blueBand, greyLevels)

	# Energy (B)

	# Entropy (B)

	# Contrast (B)

	# Homogeneity (B)