import ephem
import sys as sys
import math

gatech = ephem.Observer()
gatech.lon = '4.927675'
gatech.lat = '51.968243'
gatech.elevation = 1
gatech.date = '2018/05/09 12:00:30'
v = ephem.Sun(gatech)
print(math.degrees(float(repr(v.az))),math.degrees(float(repr(v.alt))))
