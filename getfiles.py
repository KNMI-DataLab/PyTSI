###############################################################################
# DESCRIPTION: read the information from the properties file
#              
#              
#              
#              
# AUTHOR: Job Mos			            # EMAIL: jobmos95@gmail.com
#
###############################################################################

#import libraries
from myimports import *
import gzip
import os

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

def plotAzimuthAltitude(azimuth,altitude):
	# plot the azimuth vs altitude with a horizontal line
	plt.plot(azimuth,altitude)
	plt.axhline(y=10, color='black')
	plt.xlabel('Azimuth')
	plt.ylabel('Altitude')
	plt.show()

def getFiles():
	# initiate variables
	# directory in which the data is located
	directory_in_str = 'data'

	# converts the directory from string into 'bytes'
	directory = os.fsencode(directory_in_str)

	# the '0' is added to exclude some files
	propertiesExtension = '0.properties.gz'
	imageExtension = '0.jpg'

	# empty lists for storing the data
	name = []
	altitude = []
	azimuth = []

	# look for the file names
	for file in os.listdir(directory):
		# decode the filename from bytes to string
		filename = os.fsdecode(file)
		# search for all files ending with particular extension
		if filename.endswith(propertiesExtension) == True:
			# unzip the gzip file, open the file as rt=read text
			with gzip.open(directory_in_str+'/'+filename, 'rt') as f:
				lines = []
				# read the file and store line per line
				for i, line in enumerate(f):
					lines.append(line)
				#create the lists of relevant properties
				name.append(filename.replace(propertiesExtension,''))
				altitude.append(getAltitude(lines))
				azimuth.append(getAzimuth(lines))
		else:
			pass

	# sort the filename, altitude and azimuth by filename
	# this compact method zips, sortes and unzips in one line of code
	name, altitude, azimuth = zip(*sorted(zip(name, altitude, azimuth)))

	#plot the azimuth vs altitude
	plotAzimuthAltitude(azimuth,altitude)

	# select the image
	img = cv2.imread(directory_in_str+'/'+filename.replace(propertiesExtension,imageExtension))

	return img
