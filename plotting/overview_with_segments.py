###############################################################################
# DESCRIPTION:
#
#
#
#
# AUTHOR: Job Mos			            # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *

def saveOutputToFigures(filename,img,imgTSI,regions,imageWithOutlines,imageWithOutlinesHYTA):
	fig, (ax1,ax2,ax3,ax4,ax5) = plt.subplots(1,5)

	# conversion needs to be centralized in one place.
	img = img[...,::-1] # convert from BGR -> RGB
	imgTSI = imgTSI[...,::-1] # convert from BGR -> RGB

	ax1.set_adjustable('box-forced')
	ax2.set_adjustable('box-forced')
	ax3.set_adjustable('box-forced')
	ax4.set_adjustable('box-forced')
	ax5.set_adjustable('box-forced')

	ax1.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax1.set_title('Original image')
	ax1.imshow(img)

	ax2.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax2.set_title('Old software')
	ax2.imshow(imgTSI)

	ax3.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax3.set_title('New segments')
	ax3.imshow(regions)

	ax4.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax4.set_title('Fixed')
	ax4.imshow(imageWithOutlines)

	ax5.tick_params(axis='both', which='both',bottom='off',top='off',left='off',right='off',labelbottom='off',labelleft='off')
	ax5.set_title('HYTA')
	ax5.imshow(imageWithOutlinesHYTA)

	plt.tight_layout()

	plt.savefig('results/regions/'+filename+'_segmented_image.png',bbox_inches='tight')
	plt.close()
