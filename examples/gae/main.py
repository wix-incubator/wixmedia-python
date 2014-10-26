# -*- encoding: UTF-8 -*-

from django.template.loader import render_to_string
import webapp2
from wix import media


class RenderImagesHandler(webapp2.RequestHandler):
    def get(self):

        # Image id's can be fetched from datastore ...
        image_ids = [
            'ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg',
            'ggl-685734655894940532967/images/c074a4a8ea854ee7b5b893ce2a0c7361/dog.jpg'
        ]

        context = {
            'thumbnail_urls': [RenderImagesHandler.create_image_thumbnail_url(image_id) for image_id in image_ids]
        }

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(render_to_string('example.html', context))

    @staticmethod
    def create_image_thumbnail_url(image_id):
        client = media.Client()
        image  = client.get_image_from_id(image_id)

        return image.fill(width=120, height=120).unsharp().quality().get_url()


app = webapp2.WSGIApplication([
    ('/', RenderImagesHandler),
], debug=True)