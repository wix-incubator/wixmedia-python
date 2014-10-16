# -*- encoding: UTF-8 -*-

# from google.appengine.ext.webapp import template
# register = template.create_template_register()

import webapp2
from django.conf import settings

from django import template
register = template.Library()

from wixmedia.wixmedia_image import WixMediaImage


@register.simple_tag
def image_url(filename='', original_filename='i.jpg', **params):

    image = WixMediaImage(settings.WIXMEDIA_ROOT + '/' + filename, original_filename)

    for oper, args in params.items():
        kwargs = dict([a.split('_') for a in args.split(',')])
        if hasattr(image, oper):
            getattr(image, oper)(**kwargs)


    # operations = ['%s/%s' % (k, v) for k, v in params.items()]
    # url = '%(root)s/%(file)s/%(opts)s/%(original)s' % {
    #     'root': settings.WIXMEDIA_ROOT,
    #     'file': filename,
    #     'original': original_filename,
    #
    #     'opts': '/'.join(operations),
    # }

    return image.get_rest_url()


