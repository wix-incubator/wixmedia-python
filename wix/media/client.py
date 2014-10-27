from datetime import datetime
import functools
from urlparse import urlparse
import calendar
import urllib2
import json
import os
from .exceptions import GeneralError, UploadError
from .image import Image
import auth
from wix.media import http_utils

AUTH_ALGORITHM = "MCLOUDTOKEN"


def retry_auth(func):
    @functools.wraps(func)
    def _func(client, *args, **kwargs):

        got_result  = False
        retry_count = 0
        result      = None

        while not got_result:
            try:
                result = func(client, *args, **kwargs)
                got_result = True
            except urllib2.HTTPError as e:
                if e.code == 403:
                    if retry_count > 1:
                        raise UploadError(e.reason)

                    client.get_auth_token()
                    retry_count += 1
                else:
                    raise UploadError('failed to upload file: http_status=%d, reason=%s' % (e.code, e.reason))

        return result

    return _func


class Client(object):

    METADATA_SERVICE_HOST     = 'mediacloud.wix.com'
    WIX_MEDIA_UPLOAD_URL      = 'http://%s/files/upload/url' % METADATA_SERVICE_HOST
    WIX_MEDIA_AUTH_TOKEN_URL  = 'http://%s/auth/get-token' % METADATA_SERVICE_HOST
    # IMAGE_SERVICE             = 'media.wixapps.net'
    IMAGE_SERVICE             = '107.178.253.0'

    def __init__(self, api_key=None, api_secret=None):
        self.api_key    = api_key
        self.api_secret = api_secret
        self.auth_token = ''

    @staticmethod
    def get_image_from_id(image_id):
        return Image(image_id=image_id, service_host=Client.IMAGE_SERVICE)

    def _validate_auth_credentials(self):
        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

    def get_auth_token(self):
        self._validate_auth_credentials()

        headers = {
            'x-wix-upload-nonce': os.urandom(6).encode("hex"),
            'x-wix-upload-ts':    Client._get_utc_now_ts()
        }

        url = Client.WIX_MEDIA_AUTH_TOKEN_URL
        auth_handler = auth.WixHmacAuthHandler(self.api_key, self.api_secret)
        headers = auth_handler.add_auth(method="GET", path=urlparse(url).path, headers=headers)

        try:
            http_status, _, response_headers = http_utils.get(url, headers=headers)

            if http_status != 200:
                raise UploadError('Failed to get upload url: http_status=%d' % http_status)

            algorithm, self.auth_token = response_headers['Authorization'].split(' ', 1)

            if algorithm != AUTH_ALGORITHM:
                raise GeneralError('Invalid authorization algorithm')

        except urllib2.HTTPError as e:
            raise UploadError(e.reason())

    def upload_image_from_path(self, file_path):
        with open(file_path, 'r') as fp:
            metadata = self._upload_to_pm_from_stream(fp, os.path.basename(file_path), "picture")
            return Image(image_id=metadata['file_url'], service_host=Client.IMAGE_SERVICE)

    def upload_file_from_stream(self, fp, file_name):
        metadata = self._upload_to_pm_from_stream(fp, file_name, media_type="picture")

        return Image(image_id=metadata['file_url'], service_host=Client.IMAGE_SERVICE)

    def _upload_to_pm_from_stream(self, fp, file_name, media_type):

        if not self.auth_token:
            self.get_auth_token()

        upload_url = self._get_upload_url()
        metadata   = self._upload_to_url(upload_url, fp, file_name, media_type)

        return metadata

    @retry_auth
    def _get_upload_url(self):

        headers = {'Authorization': AUTH_ALGORITHM + ' ' + self.auth_token}

        http_status, content, _ = http_utils.get(Client.WIX_MEDIA_UPLOAD_URL, headers)

        if http_status != 200:
            raise UploadError('failed to get upload url: http_status=%d' % http_status)

        metadata = json.loads(content)
        return metadata['upload_url']

    @retry_auth
    def _upload_to_url(self, upload_url, fp, file_name, media_type):

        fields  = {"media_type": media_type}
        files   = {'file': {'filename': file_name, 'content': fp.read()}}
        headers = {'Authorization':  AUTH_ALGORITHM + ' ' + self.auth_token}

        http_status, content, _ = http_utils.post_multipart(upload_url, headers, fields, files)

        if http_status != 200:
            raise UploadError('failed to upload file: http_status=%d' % http_status)

        return json.loads(content)[0]

    @staticmethod
    def _get_utc_now_ts():
        return calendar.timegm(datetime.utcnow().utctimetuple())