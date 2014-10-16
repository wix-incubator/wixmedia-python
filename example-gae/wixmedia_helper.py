# -*- encoding: UTF-8 -*-

from django.conf import settings
from wixmedia.wixmedia_image import WixMediaImage


def image_url(filename='', original_filename='i.jpg', **params):
    image = WixMediaImage(settings.WIXMEDIA_ROOT + '/' + filename, original_filename)

    for oper, args in params.items():
        kwargs = dict([a.split('_') for a in args.split(',')])
        if hasattr(image, oper):
            getattr(image, oper)(**kwargs)

    return image.get_rest_url()
