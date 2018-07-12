import settings
import ephem
import math


def setup_objects():
    # create observer object
    obs = ephem.Observer()
    # define its latitude and longitude
    # in this case, we use the location of Cabauw
    obs.lat = settings.camera_latitude
    obs.lon = settings.camera_longitude

    # define which solar body we are investigating
    solar_body = ephem.Sun()

    return obs, solar_body


def transit(year, month, day, obs, solar_body):
    obs.date = str(year + '/' + month + '/' + day)

    obs.next_transit(solar_body)

    transit_alt = math.degrees(float(repr(solar_body.alt)))

    return transit_alt
