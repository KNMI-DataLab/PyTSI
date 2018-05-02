# DESCRIPTION: get amount of pixels in the four different areas to be used in
#              postprocessing corrections

from myimports import *

def preSolarCorrection(labels, redBlueRatio, sunnyThreshold):
	# labels == 0 : mask
	# labels == 1 : outside circle
	# labels == 2 : horizon are
	# labels == 3 : inner circle
	# labels == 4 : sun circle

	initialAdjustmentFactorLimit = 0.5

	# pixels sun circle
	sunC = np.sum(((labels == 4) & (redBlueRatio != 0) & (redBlueRatio >= sunnyThreshold)))
	sunS = np.sum(((labels == 4) & (redBlueRatio != 0) & (redBlueRatio <  sunnyThreshold)))

	# pixels horizon area
	horizonC   = np.sum(((labels == 2) & (redBlueRatio != 0) & (redBlueRatio >= sunnyThreshold)))
	horizonS   = np.sum(((labels == 2) & (redBlueRatio != 0) & (redBlueRatio <  sunnyThreshold)))

	# pixels inner circle
	innerC     = np.sum(((labels == 3) & (redBlueRatio != 0) & (redBlueRatio >= sunnyThreshold)))
	innerS     = np.sum(((labels == 3) & (redBlueRatio != 0) & (redBlueRatio <  sunnyThreshold)))

	# pixels outside horizon area and inner circle
	outsideC   = np.sum(((labels == 1) & (redBlueRatio != 0) & (redBlueRatio >= sunnyThreshold)))
	outsideS   = np.sum(((labels == 1) & (redBlueRatio != 0) & (redBlueRatio <  sunnyThreshold)))

	showNumberOfPixels = False
	if showNumberOfPixels:
		print('sun circle cloudy pixels',sunC)
		print('sun circle sunny pixels ',sunS)

		print('horizon area cloudy pixels',horizonC)
		print('horizon area sunny pixels ',horizonS)

		print('inner circle cloudy pixels',innerC)
		print('inner circle sunny pixels ',innerS)

		print('outside cloudy pixels',outsideC)
		print('outside sunny pixels ',outsideS)

	return outsideC, outsideS, horizonC, horizonS, innerC, innerS, sunC, sunS
