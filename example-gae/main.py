# -*- encoding: UTF-8 -*-

import os
import sys
from webapp2 import WSGIApplication, Route


# ROOT = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(os.path.abspath('..'))


app = WSGIApplication(
    debug=True,
    routes=[
        # [GET] /
        Route('/', handler='handlers.Handler', handler_method='example'),

        # Route('/ping', handler='service.handlers.Handler', handler_method='ping'),
        # Route('/dummy/examples', handler='service.handlers_dummy.DummyHandler', handler_method='examples'),
    ]
)


