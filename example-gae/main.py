# -*- encoding: UTF-8 -*-

from django.template.loader import render_to_string
import webapp2
from wix import media


class RenderImagesHandler(webapp2.RequestHandler):
    def get(self):

        # Image id's can be fetched from datastore ...

        cat_image_id = 'wix-ac831a9e-577b-4018-b8b8-88499c811234/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'
        dog_image_id = 'wix-ac831a9e-577b-4018-b8b8-88499c811234/images/c074a4a8ea854ee7b5b893ce2a0c7361/dog.jpg'

        cat_image_thumbnail_url = self.create_image_thumbnail_url(cat_image_id)
        dog_image_thumbnail_url = self.create_image_thumbnail_url(dog_image_id)

        context = {
            'thumbnail_urls': [(cat_image_thumbnail_url, 'cat'), (dog_image_thumbnail_url, 'dog')]
        }

        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(render_to_string('example.html', context))

    def create_image_thumbnail_url(self, image_id):
        client = media.Client()
        image  = client.get_image_from_id(image_id)

        return image.srz(width=120, height=120).get_url()


app = webapp2.WSGIApplication([
    ('/', RenderImagesHandler),
], debug=True)