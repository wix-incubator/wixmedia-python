# -*- encoding: UTF-8 -*-

import webapp2
from django.template.loader import render_to_string


class Handler(webapp2.RequestHandler):

    def example(self, *args, **kwargs):
        context = {}

        html = render_to_string('example_django.html', context)

        self.response.out.write(html)

