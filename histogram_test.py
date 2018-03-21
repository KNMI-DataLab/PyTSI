'''
 * Python program to create a color histogram on a masked image.
 *
 * Usage: python ColorHistogramMask.py <filename>
'''
import cv2, sys, numpy as np
from matplotlib import pyplot as plt

# read original image, in full color, based on command
# line argument
img = cv2.imread("20180309120600.jpg")

# display the original image 
cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
cv2.imshow("Original Image", img)
cv2.waitKey(0)

# create a circular mask to select the 7th well in the first row
# WRITE YOUR CODE HERE
mask = np.zeros(img.shape, dtype = "uint8")
cv2.circle(mask, (1053, 240), 49, (255, 255, 255), -1)

# use cv2.bitwise_and() to apply the mask to img, and save the 
# results in a new image named maskedImg
# WRITE YOUR CODE HERE
maskedImg = cv2.bitwise_and(img, mask)

# create a new window and display maskedImg, to verify the 
# validity of your mask
# WRITE YOUR CODE HERE
cv2.namedWindow("masked plate", cv2.WINDOW_NORMAL)
cv2.imshow("masked plate", maskedImg)
cv2.waitKey(0)

# right now, the mask is black and white, but it has three
# color channels. We need it to have only one channel.
# Convert the mask to a grayscale image, using slicing to
# pull off just the first channel
mask = mask[:, :, 0]

# split into channels
channels = cv2.split(img)

# list to select colors of each channel line
colors = ("b", "g", "r") 

# create the histogram plot, with three lines, one for
# each color
plt.xlim([0, 256])
for(channel, c) in zip(channels, colors):
    # change this to use your circular mask to apply the histogram
    # operation to the 7th well of the first row
    # MODIFY CODE HERE
    histogram = cv2.calcHist([channel], [0], mask, [256], [0, 256])
    plt.plot(histogram, color = c)

plt.xlabel("Color value")
plt.ylabel("Pixels")

plt.show()
