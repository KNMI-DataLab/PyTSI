# DESCRIPTION: calculates the sky cover based on hybrid thresholding

import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import sys
import timeit
from math import log10
from scipy.optimize import minimize

def calculateSkyCoverWithHYTA(cloudPixels,sunPixels):
	fractionalSkyCover = cloudPixels / (sunPixels+cloudPixels)

	return fractionalSkyCover
