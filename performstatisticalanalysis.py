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

def performStatisticalAnalysis(maskedImg):

	greyLevels = 256

	xres = 288
	yres = 352

	# extract R and B band individually from image
	blueBand = np.zeros([yres,xres])
	redBand = np.zeros([yres,xres])

	for i in range (0,yres):
		for j in range (0,xres):
			# check whether on pixel is part of mask
			# if pixel is masked, do nothing
			if maskedImg[i,j,0] == 0 and maskedImg[i,j,1] == 0 and maskedImg[i,j,2] == 0:
				pass
			else:
				# i = ypixel, j = xpixel, 0,2 = blue, red
				blueBand[i,j] = maskedImg[i,j,0]
				redBand[i,j]  = maskedImg[i,j,2]

	# SPECTRAL FEATURES

	# mean (R and B)

	# standard deviation (B)

	# skewness (B)

	# difference (R-G, R-B and G-B)

	# TEXTURAL FEATURES

	# Grey Level Co-occurrence Matrices (GLCM)
	# matrix elements represent relative frequence that two pixels occur
	# separated in a defined direction by distance dx,dy (A. Heinle et al., 2010)
	GLCM = np.zeros([greyLevels,greyLevels], dtype = 'int')

	# pixel distance
	dx = 1
	dy = 1

	# reset resolutions for GLCM calculation
	xres = 352
	yres = 288

	# calculate min and max grey values of the blue band
	greyMin = int(np.amin(blueBand[np.nonzero(blueBand)]))
	greyMax = int(np.amax(blueBand[np.nonzero(blueBand)]))

	# calculate the GLCM matrix
	# loop over GLCM matrix elements
	for i in range (greyMin,greyMax):
		for j in range (greyMin,greyMax):
			print(i,j)
			# loop over image pixels
			for x in range (0, xres):
				for y in range (0, yres):
					# check whether on pixel is part of mask
					# if pixel is masked, do nothing
					if blueBand[x,y] == 0 or blueBand[x+dx,y+dy] == 0:
						pass
					else:
						# when two pixels 'match' add +1 to GLCM matrix element
						if blueBand[x,y] == i and blueBand[x+dx,y+dy] == j:
							GLCM[i,j] += 1
							print(GLCM[i,j])
						else:
							pass

	np.savetxt('test.txt', GLCM, fmt='%3d')

	# Energy (B)

	# Entropy (B)

	# Contrast (B)

	# Homogeneity (B)