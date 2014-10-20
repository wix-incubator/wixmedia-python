# -*- encoding: UTF-8 -*-

import webapp2
from django.template.loader import render_to_string

from wixmedia.wixmedia_image import WixMediaImage


class Item(object):
    # it can be model

    url = 'http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/dog.png'

    def get_thumbnail_url(self):
        image = WixMediaImage(self.url)
        image.srz(width=120, height=120, alignment="top-left").adjust(brightness=60)
        return image.get_rest_url()


class Handler(webapp2.RequestHandler):

    def example(self, *args, **kwargs):
        context = {}

        item = Item()
        context['item'] = item

        self.response.out.write(render_to_string('example.html', context))

