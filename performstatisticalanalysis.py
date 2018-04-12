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
from tqdm import tqdm

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
	use4 = False

	# FOLLOWING CALCULATION TAKES A LARGE AMOUNT OF TIME
	# 'greyLevels' is used to decrease amount of grey levels and thus
	# reduces computation time

	# compute 4 GLCM matrices, bottom right, bottom left, top left, top right
	# loop over GLCM matrix elements
	for i in range (greyMin,greyMax):
		for j in range (greyMin,greyMax):
			# loop over image pixels
			for x in range (0, settings.yres):
				for y in range (0, settings.xres):
					# GLCM1
					# check whether on pixel is part of mask
					# if pixel is masked, skip to next iteration
					if blueBand[x,y] == 0:
						continue
					else:
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

def extractBands(scaler, maskedImg):
	# extract R and B band individually from image
	# the arrays are set up in [y,x] orientation because the image
	# has some 'special' metadata which shows opposite resolution/geometry
	# view with: "$ identify -verbose data/20170419133000.jpg"
	blueBand  = np.zeros([settings.yres,settings.xres])
	greenBand = np.zeros([settings.yres,settings.xres])
	redBand   = np.zeros([settings.yres,settings.xres])

	for i in range (0,settings.yres):
		for j in range (0,settings.xres):
			# check whether on pixel is part of mask
			# if pixel is masked, do nothing
			if maskedImg[i,j,0] == 0 and maskedImg[i,j,1] == 0 and maskedImg[i,j,2] == 0:
				continue
			else:
				# i = ypixel, j = xpixel, 0,2 = blue, red
				blueBand[i,j]  = int(maskedImg[i,j,0]/scaler)
				greenBand[i,j] = int(maskedImg[i,j,1]/scaler)
				redBand[i,j]   = int(maskedImg[i,j,2]/scaler)

	return blueBand, greenBand, redBand

def performStatisticalAnalysis(maskedImg):

	#set the number of grey levels used in the GLCM calculation
	greyLevels = 8
	scaler = int(256/greyLevels)

	# extract the individual color bands as greyscale
	blueBand, greenBand, redBand = extractBands(scaler, maskedImg)

	# SPECTRAL FEATURES

	# mean (R and B)

	# standard deviation (B)

	# skewness (B)

	# difference (R-G, R-B and G-B)

	# TEXTURAL FEATURES

	# Grey Level Co-occurrence Matrices (GLCM)
	GLCM = calculateGLCM(blueBand, greyLevels)
	#GLCM = np.loadtxt('GLCM.txt')

	energy = entropy = contrast = homogeneity = 0

	for i in range (0, greyLevels):
		for j in range(0, greyLevels):
			if GLCM[i,j] != 0:
				# Energy (B)
				energy      += GLCM[i,j]**2

				# Entropy (B)
				entropy     += GLCM[i,j] * log10(GLCM[i,j],2)

				# Contrast (B)
				contrast    += GLCM[i,j] * (i-j)**2

				# Homogeneity (B)
				homogeneity += GLCM[i,j] / (1 + abs(i-j))
			else:
				pass

	return energy, entropy, contrast, homogeneity
