# DESCRIPTION: gets the resolution of the image
from myimports import *

def get_resolution(img):
	global x,y,nColors
	y, x, nColors = img.shape
