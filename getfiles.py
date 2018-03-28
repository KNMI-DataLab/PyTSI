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

def getAltitude(lines):
	for line in lines:
		if line.startswith('tsi.image.solar.altitude='):
			tmp1, tmp2 = line.split('=')
			altitudeStr, tmp1 = tmp2.split('\n')

			altitude = float(altitudeStr)
		else:
			pass
		
	return altitude

def getAzimuth(lines):
	for line in lines:
		if line.startswith('tsi.image.solar.azimuth='):
			tmp1, tmp2 = line.split('=')
			azimuthStr, tmp1 = tmp2.split('\n')

			azimuth = float(azimuthStr)
		else:
			pass

	return azimuth

def plotAzimuthAltitude(azimuth,altitude):
	plt.plot(azimuth,altitude)
	plt.axhline(y=10, color='black')
	plt.xlabel('Azimuth')
	plt.ylabel('Altitude')
	plt.show()

def getFiles():
	directory_in_str = 'data'

	directory = os.fsencode(directory_in_str)

	propertiesExtension = '0.properties.gz'
	imageExtension = '0.jpg'

	name = []
	altitude = []
	azimuth = []

	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(propertiesExtension) == True:
			with gzip.open(directory_in_str+'/'+filename, 'rt') as f:
				lines = []
				for i, line in enumerate(f):
					lines.append(line)
				name.append(filename.replace(propertiesExtension,''))
				altitude.append(getAltitude(lines))
				azimuth.append(getAzimuth(lines))
		else:
			pass

	name, altitude, azimuth = zip(*sorted(zip(name, altitude, azimuth)))

	plotAzimuthAltitude(azimuth,altitude)

	img = cv2.imread(directory_in_str+'/'+filename.replace(propertiesExtension,imageExtension))

	return img
