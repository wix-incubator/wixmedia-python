import base64
import hmac
from hashlib import sha256 as sha256


class AuthException(Exception):
    pass


class HmacKeys(object):
    def __init__(self, access_key, secret_key):
        if access_key is None or secret_key is None:
            raise AuthException("Not ready to authenticate")

        self._access_key = None
        self._secret_key = None
        self._hmac_256   = None

        self.update_keys(access_key, secret_key)

    def update_keys(self, access_key, secret_key):
        self._access_key = access_key
        self._secret_key = secret_key
        self._hmac_256 = hmac.new(self._secret_key, digestmod=sha256)

    @staticmethod
    def algorithm():
        return 'HmacSHA256'

    def _get_hmac(self):
        return hmac.new(self._secret_key, digestmod=sha256)

    def sign_string(self, string_to_sign):
        new_hmac = self._get_hmac()
        new_hmac.update(string_to_sign)
        return base64.urlsafe_b64encode(new_hmac.digest()).strip()


class WixHmacAuthHandler(HmacKeys):
    """
    Implements the HMAC request signing used by Wix Media Cloud platform.
    """

    WixAuthService  = "WIX"
    WixHeaderPrefix = "x-wix-"

    def __init__(self, access_key, secret_key):
        HmacKeys.__init__(self, access_key, secret_key)

    def update_keys(self, access_key, secret_key):
        super(WixHmacAuthHandler, self).update_keys(access_key, secret_key)

    def add_auth(self, method="POST", path="/", headers={}):

        # if 'Date' not in headers:
        #     headers['Date'] = formatdate(usegmt=True)

        string_to_sign = WixHmacAuthHandler.canonical_string(method, path, headers)
        b64_hmac = self.sign_string(string_to_sign)
        auth = ("%s %s:%s" % (self.WixAuthService, self._access_key, b64_hmac))
        headers['Authorization'] = auth
        return headers

    @staticmethod
    def canonical_string(method, path, headers, expires=None):
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
