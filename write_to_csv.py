import settings


def headers(writer):
    if settings.data_type == 'TSI':
        writer.writerow(['filename',
                         'altitude',
                         'azimuth',
                         'thin_sky_cover',
                         'opaque_sky_cover',
                         'fractional_sky_cover',
                         'fractional_sky_cover_hybrid',
                         'thin_sky_cover_TSI',
                         'opaque_sky_cover_TSI',
                         'fractional_sky_cover_TSI',
                         'energy',
                         'entropy',
                         'contrast',
                         'homogeneity',
                         'outside_c',
                         'outside_s',
                         'horizon_c',
                         'horizon_s',
                         'inner_c',
                         'inner_s',
                         'sun_c',
                         'sun_s',
                         ])

    elif settings.data_type == 'SEG':
        writer.writerow(['filename',
                         'mean_r',
                         'mean_g',
                         'mean_b',
                         'st_dev',
                         'skewness',
                         'diff_rg',
                         'diff_rb',
                         'diff_gb',
                         'enegry',
                         'entropy',
                         'contrast',
                         'homogeneity',
                         'cloud_cover',
                         'cloud_type'
                         ])

    elif settings.data_type == 'mobotix':
        writer.writerow(['filename',
                         'azimuth',
                         'altitude',
                         'cloud_cover'
                         ])


def output_data(writer, data_row):
    # if settings.data_type == 'TSI':
    writer.writerow(data_row)
