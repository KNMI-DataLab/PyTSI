import settings


def headers(writer):
    if settings.data_type == 'TSI':
        writer.writerow(['filename',
                         'altitude',
                         'azimuth',
                         'thinSkyCover',
                         'opaqueSkyCover',
                         'fractionalSkyCover',
                         'fractionalSkyCoverHYTA',
                         'thinSkyCoverTSI',
                         'opaqueSkyCoverTSI',
                         'fractionalSkyCoverTSI',
                         'energy',
                         'entropy',
                         'contrast',
                         'homogeneity',
                         'outsideC',
                         'outsideS',
                         'horizonC',
                         'horizonS',
                         'innerC',
                         'innerS',
                         'sunC',
                         'sunS',
                         ])

    elif settings.data_type == 'SWIMSEG':
        writer.writerow(['filename',
                         'meanR',
                         'meanG',
                         'meanB',
                         'stDev',
                         'skewness',
                         'diffRG',
                         'diffRB',
                         'diffGB',
                         'enegry',
                         'entropy',
                         'contrast',
                         'homogeneity',
                         'cloud_cover',
                         'cloud_type'
                         ])


def output_data(writer, data_row):
    # if settings.data_type == 'TSI':
    writer.writerow(data_row)
