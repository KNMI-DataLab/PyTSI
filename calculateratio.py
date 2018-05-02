# DESCRIPTION: calculates the Red/Blue ratio of every image pixel by dividing
#              the red by the blue band pixelwise while avoiding the mask

from myimports import *

def calculateRatio(maskedImg):
	redBlueRatio = np.zeros([settings.yres,settings.xres])

	yres,xres,nColors = maskedImg.shape

	blueBand = np.zeros((xres,yres),dtype=int)
	redBand = np.zeros((xres,yres),dtype=int)

	blueBand = maskedImg[:,:,0].astype(int)
	redBand  = maskedImg[:,:,2].astype(int)

	for i in range (0,yres):
		for j in range (0,xres):
			if blueBand[i,j]!=0:
				redBlueRatio[i,j]=redBand[i,j]/blueBand[i,j]

	if np.average(redBlueRatio)<0 or np.average(redBlueRatio) >100:
		print('Odd average redBlueRatio found')
		sys.exit('MYSTOP')

	return redBlueRatio
