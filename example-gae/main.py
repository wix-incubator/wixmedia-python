# -*- encoding: UTF-8 -*-

# import os
# import sys
from webapp2 import WSGIApplication, Route


# ROOT = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(os.path.abspath('..'))


app = WSGIApplication(
    debug=True,
    routes=[
        # [GET] /
        Route('/django', handler='handlers_django.Handler', handler_method='example'),
        Route('/jinja2', handler='handlers_jinja2.Handler', handler_method='example'),

    ]
)


