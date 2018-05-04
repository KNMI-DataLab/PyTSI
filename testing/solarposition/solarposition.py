from pysolar.solar import *
import datetime

# location of the Mobotix camera at Cabauw
lon = 51.968243
lat = 4.927675

# file structure
year        = int('2018')
month       = int('05')
day         = int('04')
hour        = int('06')
minute      = int('00')
second      = int('00')
microsecond = int('000000')

date = datetime.datetime.now()
print(get_altitude(lon, lat, date))
date = datetime.datetime(year, month, day,
						 hour, minute, second, microsecond,
						 tzinfo=datetime.timezone.utc)
print(get_altitude(lon, lat, date))
