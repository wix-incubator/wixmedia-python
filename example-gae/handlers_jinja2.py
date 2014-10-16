# -*- encoding: UTF-8 -*-

import os
import webapp2
import jinja2

from django.conf import settings
from wixmedia.wixmedia_image import WixMediaImage



def image_url(filename='', original_filename='i.jpg', **params):
    image = WixMediaImage(settings.WIXMEDIA_ROOT + '/' + filename, original_filename)

    for oper, args in params.items():
        kwargs = dict([a.split('_') for a in args.split(',')])
        if hasattr(image, oper):
            getattr(image, oper)(**kwargs)

    return image.get_rest_url()




JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=[
        'jinja2.ext.autoescape',
    ],
    autoescape=True)
JINJA_ENVIRONMENT.globals['image_url'] = image_url




class Handler(webapp2.RequestHandler):

    def example(self, *args, **kwargs):
        context = {}

        template = JINJA_ENVIRONMENT.get_template('example_jinja2.html')
        self.response.write(template.render(context))

