# DESCRIPTION: main function. loops over files, calls other functionsand writes
#              data to file(s)

from myimports import *
import gzip
import os
import csv
from tqdm import tqdm
from processor import processor
from performstatisticalanalysis import performStatisticalAnalysis
from plotskycover import plotSkyCoverComparison
from postprocessor import postProcessor

# get the altitude of the image
def getAltitude(lines):
	for line in lines:
		if line.startswith('tsi.image.solar.altitude='):
			# extract altitude from the correct line
			tmp1, tmp2 = line.split('=')
			altitudeStr, tmp1 = tmp2.split('\n')

			# convert string to float
			altitude = float(altitudeStr)
		else:
			pass

	return altitude

# get the azimuth of the image
def getAzimuth(lines):
	for line in lines:
		if line.startswith('tsi.image.solar.azimuth='):
			# extract azimuth from the correct line
			tmp1, tmp2 = line.split('=')
			azimuthStr, tmp1 = tmp2.split('\n')

			# convert string to float
			azimuth = float(azimuthStr)
		else:
			pass

	return azimuth

# get the fractional sky cover of the 'old' TSI software
def getFractionalSkyCoverTSI(lines):
	for line in lines:
		if line.startswith('tsi.image.fraction.opaque='):
			# extract opaque fraction from the correct line
			tmp1, tmp2 = line.split('=')
			opaqueSkyCoverStr, tmp1 = tmp2.split('\n')

			# convert string to float
			opaqueSkyCoverTSI = float(opaqueSkyCoverStr)

		elif line.startswith('tsi.image.fraction.thin='):
			# extract thin fraction from the correct line
			tmp1, tmp2 = line.split('=')
			thinSkyCoverStr, tmp1 = tmp2.split('\n')

			# convert string to float
			thinSkyCoverTSI = float(thinSkyCoverStr)

	fractionalSkyCoverTSI = opaqueSkyCoverTSI + thinSkyCoverTSI

	return thinSkyCoverTSI, opaqueSkyCoverTSI, fractionalSkyCoverTSI

def main():
	# set/initialize the global variables
	settings.init()

	# initiate variables
	# directory in which the data is located
	directory_in_str = '/usr/people/mos/Documents/data/DBASE/20180201_tsi-cabauw_realtime'

	# converts the directory from string into 'bytes'
	directory = os.fsencode(directory_in_str)

	# alphabetically sort the files in the diretory
	sortedDirectory = sorted(os.listdir(directory))

	# the '0' is added to exclude some files in the directory
	propertiesExtension = '0.properties.gz'
	imageExtension = '0.jpg'

	#open the data file
	with open('data.csv', 'w') as fd:
		writer = csv.writer(fd, delimiter='\t')
		# write headers to file
		writer.writerow(['filename', 'altitude', 'azimuth',
						'thinSkyCover', 'opaqueSkyCover', 'fractionalSkyCover',
						'fractionalSkyCoverHYTA',
						'thinSkyCoverTSI', 'opaqueSkyCoverTSI', 'fractionalSkyCoverTSI',
						'energy', 'entropy', 'contrast', 'homogeneity',
						'outsideC', 'outsideS', 'horizonC', 'horizonS',
						'innerC', 'innerS', 'sunC', 'sunS'])

		# look for the file names
		for file in tqdm(sortedDirectory):
			# decode the filename from bytes to string
			filename = os.fsdecode(file)
			# search for all files ending with particular extension
			if filename.endswith(propertiesExtension):
				# unzip the gzip file, open the file as rt=read text
				with gzip.open(directory_in_str+'/'+filename, 'rt') as f:
					lines = []
					# read the file and store line per line
					for line in f:
						lines.append(line)
					#get the altitude and azimuth from the defs
					altitude = getAltitude(lines)
					azimuth = getAzimuth(lines)

					# only carry out calculations for solar angle > 10 degrees
					# this strategy is proposed by Long et al
					if altitude >= 10:
						# get the fractional sky cover from 'old' TSI software
						thinSkyCoverTSI, opaqueSkyCoverTSI, fractionalSkyCoverTSI = getFractionalSkyCoverTSI(lines)

						# read the image
						img = cv2.imread(directory_in_str+'/'+filename.replace(propertiesExtension,imageExtension))
						imgTSI = cv2.imread(directory_in_str+'/'+filename.replace(propertiesExtension,'0.png'))

						# main processing function
						thinSkyCover, opaqueSkyCover, fractionalSkyCover,fractionalSkyCoverHYTA, maskedImg, outsideC, outsideS, horizonC, horizonS, innerC, innerS, sunC, sunS = processor(img, imgTSI, azimuth, altitude, filename.replace(propertiesExtension,''))

						# calculate statistical properties of the image
						energy = 0
						entropy = 0
						contrast = 0
						homogeneity = 0
						energy, entropy, contrast, homogeneity = performStatisticalAnalysis(maskedImg)

						# write data to file
						writer.writerow((filename.replace(propertiesExtension,''),
										altitude, azimuth,
										thinSkyCover, opaqueSkyCover, fractionalSkyCover,
										fractionalSkyCoverHYTA,
										thinSkyCoverTSI, opaqueSkyCoverTSI, fractionalSkyCoverTSI,
										energy, entropy, contrast, homogeneity,
										outsideC, outsideS, horizonC, horizonS,
										innerC, innerS, sunC, sunS
										))

	# postprocessing step which carries out corrections for solar/horizon area
	#postProcessor()

	# plot the sky cover comparison
	#plotSkyCoverComparison()

if __name__ == '__main__':
	main()
