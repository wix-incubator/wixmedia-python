# Copyright 2010 Google Inc.
# Copyright (c) 2011 Mitch Garnaat http://garnaat.org/
# Copyright (c) 2011, Eucalyptus Systems, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.


"""
Handles authentication required to Wix Media Cloud platform
"""

import base64
import hmac
import copy
from email.utils import formatdate
import urllib

try:
    from hashlib import sha1 as sha
    from hashlib import sha256 as sha256
except ImportError:
    import sha
    sha256 = None

class AuthException(Exception):
    pass

class HmacKeys(object):
    """Key based Auth handler helper."""

    def __init__(self, access_key, secret_key):
        if access_key is None or secret_key is None:
            raise AuthException("Not ready to authenticate")
        self.update_keys(access_key, secret_key)

    def update_keys(self, access_key, secret_key):
        self._access_key = access_key
        self._secret_key = secret_key
        self._hmac = hmac.new(self._secret_key, digestmod=sha)
        if sha256:
            self._hmac_256 = hmac.new(self._secret_key,
                                      digestmod=sha256)
        else:
            self._hmac_256 = None

    def algorithm(self):
        if self._hmac_256:
            return 'HmacSHA256'
        else:
            return 'HmacSHA1'

    def _get_hmac(self):
        if self._hmac_256:
            digestmod = sha256
        else:
            digestmod = sha
        return hmac.new(self._secret_key,
                        digestmod=digestmod)

    def sign_string(self, string_to_sign):
        new_hmac = self._get_hmac()
        new_hmac.update(string_to_sign)
        return base64.urlsafe_b64encode(new_hmac.digest()).strip()

    def __getstate__(self):
        pickled_dict = copy.copy(self.__dict__)
        del pickled_dict['_hmac']
        del pickled_dict['_hmac_256']
        return pickled_dict

    def __setstate__(self, dct):
        self.__dict__ = dct
        self.update_keys(self._secret_key)


class WixHmacAuthHandler(HmacKeys):
    """
    Implements the HMAC request signing used by Wix Media Cloud platform.
    """

    WixAuthService  = "WIX"
    WixHeaderPrefix = "x-wix-"

    def __init__(self, access_key, secret_key):
        HmacKeys.__init__(self, access_key, secret_key)
        self._hmac_256 = None

    def update_keys(self, access_key, secret_key):
        super(WixHmacAuthHandler, self).update_keys(access_key, secret_key)
        self._hmac_256 = None

    def add_auth(self, method="POST", path="/", headers={}, **kwargs):

        # if 'Date' not in headers:
        #     headers['Date'] = formatdate(usegmt=True)

        string_to_sign = self.canonical_string(method, path, headers)
        b64_hmac = self.sign_string(string_to_sign)
        auth = ("%s %s:%s" % (self.WixAuthService, self._access_key, b64_hmac))
        headers['Authorization'] = auth
        return headers

    def unquote_v(nv):
        if len(nv) == 1:
            return nv
        else:
            return (nv[0], urllib.parse.unquote(nv[1]))

    def canonical_string(self, method, path, headers, expires=None):
        """
        Generates the canonical string for the given parameters
        """
        interesting_headers = {}
        for key in headers:
            lk = key.lower()
            if headers[key] is not None and lk.startswith(WixHmacAuthHandler.WixHeaderPrefix):
                interesting_headers[lk] = str(headers[key]).strip()

        # if you're using expires for query string auth, then it trumps date
        # (and provider.date_header)
        # if expires:
        #     interesting_headers['date'] = str(expires)

        buf = "%s\n" % method

        # don't include anything after the first ? in the resource...
        t = path.split('?')
        buf += t[0]

        sorted_header_keys = sorted(interesting_headers.keys())
        for key in sorted_header_keys:
            val = interesting_headers[key]
            if key.startswith(WixHmacAuthHandler.WixHeaderPrefix):
                buf += "%s:%s\n" % (key, val)
            else:
                buf += "%s\n" % val

        return buf
