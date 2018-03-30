###############################################################################
# DESCRIPTION: plots the processed cloud image and saves the figure
#             
#              
#
#
# AUTHOR: Job Mos                                   # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plotRatio(img,redBlueRatio,sunnyThreshold,thinThreshold, filename):
	# calculate image properties (resolution of the image)
	# calculation doesn't work yet, setting manually
	#[xres,yres]=img.shape
	xres=288
	yres=352
	
	# span an x/y space
	x = np.linspace(0,xres-1,xres)
	y = np.linspace(0,yres-1,yres)
	
	# convert the data so that they can be plotted
	grid = redBlueRatio.reshape((yres, xres))

	# make a color map of fixed colors
	cmap = colors.ListedColormap(['black', 'blue', 'lightgray', 'white'])
	# set thresholds
	opaque = 1      #everything above 1 is thick opaque clouds
	lower  = 0.01
	mask   = 0
	bounds=[mask,lower,sunnyThreshold,thinThreshold,opaque]
	norm = colors.BoundaryNorm(bounds, cmap.N)

	# create subplot environment
	fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15,5))

	#### Original image
	imgChannels = cv2.split(img)
	trueColorImg=cv2.merge(list(reversed(imgChannels)))
	ax1.set_title('Original image')
	ax1.imshow(trueColorImg)

	#### TSI processed image
	img = cv2.imread('./data/'+filename+'0.png')
	imgChannels = cv2.split(img)
	trueColorImg=cv2.merge(list(reversed(imgChannels)))
	ax2.set_title('TSI processed image')
	ax2.imshow(trueColorImg)

	#### Reprocessed image
	ax3.set_title('Reprocessed image')
	
	# tell imshow about colormap so that only set colors are used
	img = ax3.imshow(grid, interpolation='nearest', cmap=cmap, norm=norm)

	# make a color bar
	fig.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds, fraction=0.045, pad=0.04)

	#plt.tight_layout()
	plt.savefig('results/test/'+filename)
	#plt.show()
	plt.close()