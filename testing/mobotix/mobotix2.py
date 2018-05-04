import os as os
from tqdm import tqdm
from pysolar.solar import *
import datetime as datetime
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2

# location of the Mobotix camera at Cabauw
lat = 51.968243
lon = 4.927675

# select year/month/day/hour. type '*' for selecting all
year = '2018'
month = '04'
day = '25'
hour = '18'

directory_in_str = '/nobackup/users/mos/bbc.knmi.nl/MEMBERS/' + \
					'knmi/datatransfer/mobotix/vectrontest/'  + \
					year + '/' + month + '/' + day + '/' + hour

path = os.fsencode(directory_in_str)

azimuth   = np.zeros(len(os.listdir(path)),dtype=float)
altitude  = np.copy(azimuth)

for i,file in enumerate(sorted(os.listdir(path))):
	filename = os.fsdecode(file)
	if filename.endswith(".jpg"):
		year   = int('20'+filename[1:3])
		month  = int(filename[3:5])
		day    = int(filename[5:7])
		hour   = int(filename[7:9])
		minute = int(filename[9:11])
		second = int(filename[11:13])
		micrsc = int(filename[13:16])*1000
		#print(year,month,day,hour,minute,second,micrsc)
		date = datetime.datetime(year, month, day,
								 hour, minute, second, micrsc,
								 tzinfo=amsterdam)

		#img = cv2.imread(directory_in_str+'/'+filename+'.jpg')

		#x, y, nColors = img.shape

		azimuth[i]  = get_azimuth(lat, lon, date)+360
		altitude[i] = get_altitude(lat, lon, date)

		print(azimuth[i],altitude[i])

plt.plot(azimuth,altitude, 'bo')
plt.show()
