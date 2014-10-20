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

        Route('/django', handler='handlers.Handler', handler_method='example'),

    ]
)


