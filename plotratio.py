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
import matplotlib as mpl

def plotRatio(blueRedRatio):
	# calculate image properties (resolution of the image)
	# calculation doesn't work yet, setting manually
	#[xres,yres]=img.shape
	xres=288
	yres=352
	
	# span an x/y space
	x = np.linspace(0,xres-1,xres)
	y = np.linspace(0,yres-1,yres)
	
	# convert the data so that they can be plotted
	grid = blueRedRatio.reshape((yres, xres))

	# make a color map of fixed colors
	cmap = colors.ListedColormap(['black', 'white', 'blue'])
	bounds=[0,0.01,1.2,10]
	norm = colors.BoundaryNorm(bounds, cmap.N)

	# tell imshow about colormap so that only set colors are used
	img = plt.imshow(grid, interpolation='nearest', cmap=cmap, norm=norm)

	# make a color bar
	plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds)

	plt.savefig('cloudy.png')
	plt.show()
