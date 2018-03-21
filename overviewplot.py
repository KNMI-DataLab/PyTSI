###############################################################################
# DESCRIPTION: plots a window consisting of 4 subplots
#              1) original image 2) mask 3) masked image 4) histogram
#              
#
#
# AUTHOR: Job Mos						# EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *

def overviewPlot(img,mask,maskedImg):
	# convert the mask to a grayscale image, using slicing to
	# pull off just the first channel
	mask = mask[:, :, 0]

	# split into channels, required for accurate color representation in plots
	imgChannels = cv2.split(img)
	maskedImgChannels = cv2.split(maskedImg)

	# list to select colors of each channel line
	colors = ("b", "g", "r") 

	# convert images to reverse colors in order for accurate color representation in plots
	# cv2 works with "b,g,r" while matplotlib uses "r,g,b"
	trueColorImg=cv2.merge(list(reversed(imgChannels)))
	trueColorMaskedImg=cv2.merge(list(reversed(maskedImgChannels)))
	#mask=np.invert(mask)

	# create subplots
	createOverview=1
	if createOverview==True:
		plt.xlim([0,256])
		plt.subplot(221), plt.title ("Original Image"), plt.imshow(trueColorImg)
		plt.subplot(222), plt.title ("Mask"),plt.imshow(mask,'gray'),plt.colorbar()
		plt.subplot(223), plt.title ("Masked Image"), plt.imshow(trueColorMaskedImg)
		for (imgChannel,c) in zip(imgChannels,colors):
			# calculate the histogram
			histogram = cv2.calcHist([imgChannel],[0],mask,[256], [0,256])
			# additive plot of the three channels
			plt.subplot(224), plt.title ("Histogram of Masked Image"), plt.plot(histogram,color = c)

	plt.show()