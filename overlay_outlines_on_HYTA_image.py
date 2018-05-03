# DESCRIPTION: overlay the outlines on HYTA image

from myimports import *
from setthresholds import setThresholds

def overlayOutlinesOnHYTAImage(img,outlines,stencil,threshold,filename):
	imgRGB = np.zeros(outlines.shape, np.uint8)

	ratioBR = np.zeros([resolution.y,resolution.x],dtype=float)
	# extract blue and red bands
	B = np.zeros((resolution.x,resolution.y),dtype=int)
	R = np.zeros((resolution.x,resolution.y),dtype=int)
	B = img[:,:,0].astype(int)
	R = img[:,:,2].astype(int)

	# replace all masked pixels (where RGB = 0) with a large negative
	maskValue = -99

	# set all zeros (a.k.a. mask)to large negative
	B[B==0] = maskValue
	R[R==0] = maskValue

	# calculate the blue/red ratio
	for i in range (0,resolution.y):
		for j in range (0,resolution.x):
			if R[i,j]!=maskValue and B[i,j]!=maskValue:
				ratioBR[i,j]=B[i,j]/R[i,j]
			else:
				ratioBR[i,j]=maskValue

	# catch Nan
	if np.argwhere(np.isnan(ratioBR)).any() == True:
		print('NaN found in B/R ratios')
		sys.exit('MYSTOP')

	for i in range(0,resolution.y):
		for j in range(0,resolution.x):
			if ratioBR[i,j]!=maskValue:
				ratioBR[i,j] = (ratioBR[i,j]-1)/(ratioBR[i,j]+1)

	# convert greyscale image to RGB image
	#sun (blue)
	imgRGB[np.where(np.logical_and(ratioBR>=threshold, ratioBR!=maskValue))] = (0,0,255)
	#cloud (white)
	imgRGB[np.where(np.logical_and(ratioBR< threshold, ratioBR!=maskValue))] = (255,255,255)
	#mask (black)
	imgRGB[np.where(ratioBR==maskValue)] = (0,0,0)

	# create mask of outlines and create inverse mask
	img2gray = cv2.cvtColor(outlines,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)

	# black out area of outlines
	img_bg = cv2.bitwise_and(imgRGB[0:resolution.y,0:resolution.x], imgRGB[0:resolution.y,0:resolution.x], mask = mask_inv)

	# take only region of outlines from outlines image
	outlines_fg = cv2.bitwise_and(outlines, outlines, mask = mask)

	dst = cv2.add(img_bg,outlines_fg)

	imageWithOutlines = cv2. bitwise_and(dst,stencil)

	return imageWithOutlines
