import cv2
from tqdm import tqdm
import os
import sys
import glob

dataFolder = '/home/mos/Documents/TSI/machinelearning/data/tsi/'
outputFolder = '/home/mos/Documents/TSI/machinelearning/data/croppedImages/'

print('test')

for subdir, dirs, files in tqdm(sorted(os.walk(dataFolder))):
    imageCounter = 0
    for file in tqdm(sorted(files)):
        numberOfImages = len(glob.glob1(subdir, "*.jpg"))
        filename = os.fsdecode(file)
        if filename.endswith(".jpg"):
            imageCounter += 1
            # absolute location of the file
            fileLocation = subdir + '/' + filename
            # read the image
            img = cv2.imread(fileLocation)

            xres, yres, numberOfColorbands = img.shape
            N = xres * yres

            # index direction of x and y is reversed in original jpgs (somehow)
            # this means that x coordinates are actually y coordinates and
            # vice versa
            # west
            xWest   = 91
            xdxWest = 191
            yWest   = 60
            ydyWest = 140

            # east
            xEast   = 91
            xdxEast = 191
            yEast   = 162
            ydyEast = 242

            # MORNING
            if imageCounter / numberOfImages > 0.15 and imageCounter / numberOfImages < 0.17:
                #print(imageCounter/numberOfImages, filename)
                croppedImg = img[xWest:xdxWest, yWest:ydyWest]
                cv2.imwrite(outputFolder + 'west_cropped' + filename, croppedImg)

            # MIDDAY
            if imageCounter / numberOfImages > 0.50 and imageCounter / numberOfImages < 0.52:
                #print(imageCounter/numberOfImages, filename)
                croppedImg = img[xWest:xdxWest, yWest:ydyWest]
                cv2.imwrite(outputFolder + 'west_cropped' + filename, croppedImg)

                croppedImg = img[xEast:xdxEast, yEast:ydyEast]
                cv2.imwrite(outputFolder + 'east_cropped' + filename, croppedImg)

            # EVENING
            if imageCounter / numberOfImages > 0.83 and imageCounter / numberOfImages < 0.85:
                #print(imageCounter/numberOfImages, filename)
                croppedImg = img[xEast:xdxEast, yEast:ydyEast]
                cv2.imwrite(outputFolder + 'east_cropped' + filename, croppedImg)

print('END')
