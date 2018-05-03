# DESCRIPTION: gets the resolution of the image
from myimports import *

def getResolution(img):
	global x,y,nColors
	y, x, nColors = img.shape
