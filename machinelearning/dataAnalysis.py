import cv2 as cv2
from math import log10, sqrt
import sys as sys
import csv
import os
from tqdm import tqdm
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors
import time
from skimage.feature import greycomatrix


# five folders: data/swimcat/(A-sky,B-pattern,C-thick-dark,D-thick-white,E-veil)/images/*.png

# load the image and file name

# extract the bands
def extractBands(img, scaler):
    # extract R and B band individually from image
    # the arrays are set up in [y,x] orientation because the image
    # has some 'special' metadata which shows opposite resolution/geometry
    # view with: "$ identify -verbose data/20170419133000.jpg"
    blueBand = np.zeros([xres, yres])
    greenBand = np.zeros([xres, yres])
    redBand = np.zeros([xres, yres])

    for i in range(0, xres):
        for j in range(0, yres):
            # i = ypixel, j = xpixel, 0,2 = blue, red
            blueBand[i, j] = int(img[i, j, 0] / scaler)
            greenBand[i, j] = int(img[i, j, 1] / scaler)
            redBand[i, j] = int(img[i, j, 2] / scaler)

    return blueBand, greenBand, redBand


# calculate the GLCM matrix
def calculateGLCM(blueBand, greyLevels):
    # matrix elements represent relative frequence that two pixels occur
    # separated in a defined direction by distance dx,dy (A. Heinle et al., 2010)
    GLCM1 = np.zeros([greyLevels, greyLevels], dtype='int')
    GLCM2 = np.zeros([greyLevels, greyLevels], dtype='int')
    GLCM3 = np.zeros([greyLevels, greyLevels], dtype='int')
    GLCM4 = np.zeros([greyLevels, greyLevels], dtype='int')

    # pixel distance
    dx = 1
    dy = 1

    # calculate min and max grey values of the blue band
    greyMin = int(np.amin(blueBand[np.nonzero(blueBand)]))
    greyMax = int(np.amax(blueBand[np.nonzero(blueBand)]))

    # specify if an average of 4 matrices should be used
    # if false: only 2 matrices are used
    use4 = True

    # compute 4 GLCM matrices, bottom right, bottom left, top left, top right
    # loop over GLCM matrix elements
    for i in range(greyMin, greyMax):
        for j in range(greyMin, greyMax):
            # loop over image pixels
            for x in range(1, xres - 1):
                for y in range(1, yres - 1):
                    # when two pixels 'match' add +1 to GLCM matrix element
                    if blueBand[x, y] != i:
                        continue
                    else:
                        if blueBand[x + dx, y + dy] == j:
                            GLCM1[i, j] += 1
                        if blueBand[x - dx, y - dy] == j:
                            GLCM4[i, j] += 1
                        if use4:
                            if blueBand[x - dx, y + dy] == j:
                                GLCM2[i, j] += 1
                            if blueBand[x + dx, y - dy] == j:
                                GLCM3[i, j] += 1

    # calculate average of the four matrices
    # GLCM is the matrix used in textural feature analysis
    if use4:
        GLCM = (GLCM1 + GLCM2 + GLCM3 + GLCM4) / 4
    else:
        GLCM = (GLCM1 + GLCM2 + GLCM3 + GLCM4) / 2

    np.savetxt('GLCM.txt', GLCM, fmt='%3d')

    return GLCM


def calculateSpectralFeatures(redBand, greenBand, blueBand, N):
    meanR = np.sum(redBand) / N
    meanG = np.sum(greenBand) / N
    meanB = np.sum(blueBand) / N
    stDev = sqrt(np.sum(np.square(np.subtract(blueBand, meanB))) / (N - 1))
    skewness = np.sum(np.power(np.divide(np.subtract(blueBand, meanB), stDev), 3)) / N
    diffRG = meanR - meanG
    diffRB = meanR - meanB
    diffGB = meanG - meanB

    return meanR, meanG, meanB, stDev, skewness, diffRG, diffRB, diffGB


# energy,entropy,contrast,homogeneity
def calculateTexturalFeatures(GLCM, greyLevels):
    energy = entropy = contrast = homogeneity = 0
    for i in range(0, greyLevels):
        for j in range(0, greyLevels):
            if GLCM[i, j, 0, 0] != 0:
                # Energy (B)
                energy += GLCM[i, j, 0, 0] ** 2
                # Entropy (B)
                entropy += GLCM[i, j, 0, 0] * log10(GLCM[i, j, 0, 0])
                # Contrast (B)
                contrast += GLCM[i, j, 0, 0] * (i - j) ** 2
                # Homogeneity (B)
                homogeneity += GLCM[i, j, 0, 0] / (1 + abs(i - j))
            else:
                pass

    return energy, entropy, contrast, homogeneity


# cloud cover
def calculateSkyCover(img, cloudyThreshold, filename):
    redBlueRatio = np.zeros([xres, yres])

    # blue red ratio calculation for each pixel in the image
    for i in range(0, xres):
        for j in range(0, yres):
            # i = ypixel, j = xpixel, 0,2 = blue, red
            redBlueRatio[i, j] = abs(int(img[i, j, 2]) - int(img[i, j, 0]))

    #####PLOTTING
    grid = redBlueRatio.reshape((xres, yres))

    # make a color map of fixed colors
    cmap = colors.ListedColormap(['white', 'blue', 'blue'])
    # cmap = 'Blues'
    # set thresholds
    cloudy = 256
    lower = 0
    bounds = [lower, cloudyThreshold, cloudy]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # tell imshow about colormap so that only set colors are used
    img = plt.imshow(grid, interpolation='nearest', cmap=cmap, norm=norm)

    # make a color bar
    plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds, fraction=0.045, pad=0.04)
    # plt.colorbar()
    plt.savefig('results/' + filename)
    plt.close()
    #####

    sunnyPixels = 0
    cloudyPixels = 0

    # classify each pixel as cloudy/clear
    for i in range(0, xres):
        for j in range(0, yres):
            # avoid mask
            if redBlueRatio[i, j] >= cloudyThreshold:
                sunnyPixels += 1
            else:
                cloudyPixels += 1

    fractionalSkyCover = cloudyPixels / (sunnyPixels + cloudyPixels)

    return fractionalSkyCover


# write to file: id,mean,stdev,skew,diff,energy,entropy,contrast,homogeneity,cloudcover,class
# classes:
# - 0: sky
# - 1: pattern
# - 2: thick dark
# - 3: thick white
# - 4: veil

def main():
    global xres, yres

    greyLevels = 256
    scaler = int(256 / greyLevels)

    dx = dy = 1

    cloudyThreshold = 25

    database = 'swimcat'

    dataFolder = '/home/mos/Documents/TSI/machinelearning/data/labeled_images/' + database + '/'

    dirList = []
    dirList.append(dataFolder + 'A-sky/images')
    dirList.append(dataFolder + 'B-pattern/images/')
    # dirList.append(dataFolder + 'C-thick-dark/images/')
    dirList.append(dataFolder + 'D-thick-white/images/')
    dirList.append(dataFolder + 'E-veil/images/')

    with open('data_' + database + '_' + str(greyLevels) + 'levels.csv', 'w', newline='') as csvfile:
        # set up csv writing environment
        writer = csv.writer(csvfile, delimiter=',')
        # write the headers to the file
        csvfile.write(
            'filename,meanR,meanG,meanB,stDev,skewness,diffRG,diffRB,diffGB,energy,entropy,contrast,homogeneity,cloudCover,cloudClass\n')
        for cloudClass, dirName in enumerate(tqdm(dirList)):
            dirName = os.fsencode(dirList[cloudClass])
            dirName = os.listdir(dirName)
            for file in tqdm(dirName):
                filename = os.fsdecode(file)
                # absolute location of the file
                fileLocation = dirList[cloudClass] + '/' + filename
                # read the image
                img = cv2.imread(fileLocation)
                xres, yres, numberOfColorbands = img.shape
                N = xres * yres
                # extract the bands
                blueBand, greenBand, redBand = extractBands(img, scaler)
                # plt.imshow(blueBand)
                # plt.savefig('results/test/'+str(greyLevels)+'levels'+filename)
                # calculate the GLCM
                blueBand = blueBand.astype(int)
                GLCM = greycomatrix(blueBand, [dx, dy], [0, np.pi / 2.0, np.pi, 3.0 * np.pi / 2.0, 2.0 * np.pi],
                                    levels=greyLevels)
                # GLCM = calculateGLCM(blueBand,greyLevels)
                # calculate the spectral features
                meanR, meanG, meanB, stDev, skewness, diffRG, diffRB, diffGB = calculateSpectralFeatures(redBand,
                                                                                                         greenBand,
                                                                                                         blueBand, N)
                # calculate the textural features
                energy, entropy, contrast, homogeneity = calculateTexturalFeatures(GLCM, greyLevels)
                # calculate the cloud cover
                cloudCover = calculateSkyCover(img, cloudyThreshold, filename)
                # write the data to a file
                writer.writerow((
                                filename, meanR, meanG, meanB, stDev, skewness, diffRG, diffRB, diffGB, energy, entropy,
                                contrast, homogeneity, cloudCover, cloudClass))

    print('END')


if __name__ == '__main__':
    main()
