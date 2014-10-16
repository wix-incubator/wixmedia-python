# -*- encoding: UTF-8 -*-

import os
import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=[
        'jinja2.ext.autoescape',
    ],
    autoescape=True)

from wixmedia_helper import image_url
JINJA_ENVIRONMENT.globals['image_url'] = image_url


class Handler(webapp2.RequestHandler):

    def example(self, *args, **kwargs):
        context = {}

        template = JINJA_ENVIRONMENT.get_template('example_jinja2.html')
        self.response.write(template.render(context))

