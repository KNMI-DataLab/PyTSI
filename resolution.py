import settings


def get_resolution(img):
    """Get the resolution of the image

    Order (x,y) can be swapped/reversed because the image format of TSI jpg files is reversed (for some reason).
    Resolution in both directions is then set as global so that it can be called like::

        print(resolution.x)
        print(resolution.y)

    Args:
        img (int): Original unprocessed image

    Returns:

    """
    global x, y, nColors

    if settings.data_type == 'TSI':
        y, x, nColors = img.shape
    else:
        x, y, nColors = img.shape
