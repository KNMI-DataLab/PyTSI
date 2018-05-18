# get the altitude of the image
def get_altitude(lines):
    for line in lines:
        if line.startswith('tsi.image.solar.altitude='):
            # extract altitude from the correct line
            tmp1, tmp2 = line.split('=')
            altitude, tmp1 = tmp2.split('\n')

            # convert string to float
            altitude = float(altitude)
        else:
            pass

    return altitude


# get the azimuth of the image
def get_azimuth(lines):
    for line in lines:
        if line.startswith('tsi.image.solar.azimuth='):
            # extract azimuth from the correct line
            tmp1, tmp2 = line.split('=')
            azimuth, tmp1 = tmp2.split('\n')

            # convert string to float
            azimuth = float(azimuth)
        else:
            pass

    return azimuth


# get the fractional sky cover of the 'old' TSI software
def get_fractional_sky_cover_tsi(lines):
    for line in lines:
        if line.startswith('tsi.image.fraction.opaque='):
            # extract opaque fraction from the correct line
            tmp1, tmp2 = line.split('=')
            opaque_sky_cover_str, tmp1 = tmp2.split('\n')

            # convert string to float
            opaque_sky_cover_tsi = float(opaque_sky_cover_str)

        elif line.startswith('tsi.image.fraction.thin='):
            # extract thin fraction from the correct line
            tmp1, tmp2 = line.split('=')
            thin_sky_cover_tsi, tmp1 = tmp2.split('\n')

            # convert string to float
            thin_sky_cover_tsi = float(thin_sky_cover_tsi)

    fractional_sty_cover_tsi = opaque_sky_cover_tsi + thin_sky_cover_tsi

    return thin_sky_cover_tsi, opaque_sky_cover_tsi, fractional_sty_cover_tsi
