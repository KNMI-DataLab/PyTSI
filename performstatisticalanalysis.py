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
from skimage.feature import greycomatrix

def extractBands(scaler, maskedImg):
	# extract R and B band individually from image
	# the arrays are set up in [y,x] orientation because the image
	# has some 'special' metadata which shows opposite resolution/geometry
	# view with: "$ identify -verbose data/20170419133000.jpg"
	blueBand  = np.zeros([settings.yres,settings.xres])
	greenBand = np.zeros([settings.yres,settings.xres])
	redBand   = np.zeros([settings.yres,settings.xres])

	blueBand = np.divide(maskedImg[np.where(maskedImg[:,:,0]!=0)],scaler).astype(int)
	greenBand = np.divide(maskedImg[np.where(maskedImg[:,:,1]!=0)],scaler).astype(int)
	redBand = np.divide(maskedImg[np.where(maskedImg[:,:,2]!=0)],scaler).astype(int)

	return blueBand, greenBand, redBand

def performStatisticalAnalysis(maskedImg):

	#set the number of grey levels used in the GLCM calculation
	greyLevels = 8
	scaler = int(256/greyLevels)

	# extract the individual color bands as greyscale
	blueBand, greenBand, redBand = extractBands(scaler, maskedImg)

	blueBand = blueBand.astype(int)
	# Grey Level Co-occurrence Matrices (GLCM)
	dx = 1 ; dy = 1
	GLCM = greycomatrix(blueBand,[dx,dy],[0, np.pi/2.0, np.pi, 3.0*np.pi/2.0, 2.0*np.pi], levels=greyLevels)
	#GLCM = calculateGLCM(blueBand, greyLevels)
	#GLCM = np.loadtxt('GLCM.txt')

	energy = entropy = contrast = homogeneity = 0

	for i in range (0, greyLevels):
		for j in range(0, greyLevels):
			if GLCM[i,j,0,0] != 0:
				# Energy (B)
				energy      += GLCM[i,j,0,0]**2

				# Entropy (B)
				entropy     += GLCM[i,j,0,0] * log10(GLCM[i,j,0,0])

				# Contrast (B)
				contrast    += GLCM[i,j,0,0] * (i-j)**2

				# Homogeneity (B)
				homogeneity += GLCM[i,j,0,0] / (1 + abs(i-j))
			else:
				pass

	return energy, entropy, contrast, homogeneity
