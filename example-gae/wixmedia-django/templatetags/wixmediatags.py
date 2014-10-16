# -*- encoding: UTF-8 -*-

from django import template
register = template.Library()

from wixmedia_helper import image_url as image_url_helper

image_url = register.simple_tag(image_url_helper)

# @register.simple_tag
# def image_url(filename='', original_filename='i.jpg', **params):
#
#     image = WixMediaImage(settings.WIXMEDIA_ROOT + '/' + filename, original_filename)
#
#     for oper, args in params.items():
#         kwargs = dict([a.split('_') for a in args.split(',')])
#         if hasattr(image, oper):
#             getattr(image, oper)(**kwargs)
#
#
#     # operations = ['%s/%s' % (k, v) for k, v in params.items()]
#     # url = '%(root)s/%(file)s/%(opts)s/%(original)s' % {
#     #     'root': settings.WIXMEDIA_ROOT,
#     #     'file': filename,
#     #     'original': original_filename,
#     #
#     #     'opts': '/'.join(operations),
#     # }
#
#     return image.get_rest_url()
