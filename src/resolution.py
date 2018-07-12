import settings


def get_resolution(img):
    """Get the resolution of the image.

    Order (x,y) can be swapped/reversed because the image format of TSI jpg files is reversed (for some reason).
    Resolution in both directions is then set as global so that it can be called like::

        print(settings.x)
        print(settings.y)

    Args:
        img: Original unprocessed image
    """
    global x, y, n_colors

    if settings.data_type == 'TSI':
        y, x, n_colors = img.shape
    else:
        x, y, n_colors = img.shape

    settings.x = x
    settings.y = y
    settings.n_colors = n_colors