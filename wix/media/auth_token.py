from exceptions import GeneralError
from datetime import datetime
from urlparse import urlparse
import http_utils
import json
import auth
import os


AUTH_SCHEME = "MCLOUDTOKEN"


def get_auth_token(api_key, api_secret, url):

    if not api_key or not api_secret:
        raise GeneralError('Invalid authorization parameters: initialize api key and secret')

    headers = {
        'x-wix-auth-nonce': os.urandom(6).encode("hex"),
        'x-wix-auth-ts':    '%sZ' % datetime.utcnow().isoformat()
    }

    authorization_header = auth.create_authorization_header(api_key, api_secret,
                                                            method="GET", path=urlparse(url).path, headers=headers)
    headers['Authorization'] = authorization_header

    http_status, response, response_headers = http_utils.get(url, headers=headers)

    if http_status != 200:
        raise GeneralError('Failed to get authorization token: http_status=%d' % http_status)

    response = json.loads(response)

    if response['scheme'] != AUTH_SCHEME:
        raise GeneralError('Invalid authorization scheme')

    return response['token']