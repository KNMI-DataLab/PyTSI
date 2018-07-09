import settings


def headers(writer):
    """Write the headers (strings) to csv file

    Args:
        writer: csv writing object
    """
    if settings.data_type == settings.tsi_str:
        writer.writerow(['filename',
                         'altitude',
                         'azimuth',
                         'thin_sky_cover',
                         'opaque_sky_cover',
                         'cloud_cover_fixed',
                         'cloud_cover_hybrid_mce',
                         'cloud_cover_hybrid_otsu',
                         'thin_cloud_cover_TSI',
                         'opaque_cloud_cover_TSI',
                         'cloud_cover_TSI',
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

    elif settings.data_type == settings.cat_str:
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
                         'cloud_cover_fixed',
                         'cloud_cover_hybrid',
                         'cloud_type'
                         ])

    elif settings.data_type == settings.seg_str:
        writer.writerow(['filename',
                         'cloud_cover_GT',
                         'cloud_cover_fixed',
                         'cloud_cover_hybrid',
                         ])

    elif settings.data_type == settings.mob_str:
        writer.writerow(['filename',
                         'azimuth',
                         'altitude',
                         'energy',
                         'entropy',
                         'contrast',
                         'homogeneity',
                         'cloud_cover'
                         ])


def output_data(writer, data_row):
    # if settings.data_type == 'TSI':
    writer.writerow(data_row)
