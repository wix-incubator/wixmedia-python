import json
import os
import urllib2
from urlparse import urlparse

import requests
import time

from .exceptions import GeneralError
import image
import auth


class Client(object):

    METADATA_SERVICE_HOST     = 'mediacloud.wix.com'
    WIX_MEDIA_UPLOAD_URL_PATH = '/files/upload/api/url'
    WIX_MEDIA_UPLOAD_URL      = 'http://%s%s' % (METADATA_SERVICE_HOST, WIX_MEDIA_UPLOAD_URL_PATH)
    IMAGE_SERVICE             = 'media.wixapps.net'

    def __init__(self, api_key=None, api_secret=None):
        self.api_key    = api_key
        self.api_secret = api_secret

    @staticmethod
    def get_image_from_id(image_id):
        return image.Image(image_id=image_id, service_host=Client.IMAGE_SERVICE)

    def _validate_auth_credentials(self):
        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

    def upload_image_from_path(self, file_path):
        self._validate_auth_credentials()

        with open(file_path, 'r') as fp:
            metadata = self._upload_to_pm_from_stream(fp, os.path.basename(file_path), "picture")
            return image.Image(image_id=metadata['file_url'], service_host=Client.IMAGE_SERVICE)

    def upload_file_from_stream(self, fp, file_name):
        self._validate_auth_credentials()

        metadata = self._upload_to_pm_from_stream(fp, file_name, media_type="picture")

        return image.Image(image_id=metadata['file_url'], service_host=Client.IMAGE_SERVICE)

    def upload_audio_from_path(self, file_path):
        self._validate_auth_credentials()

        raise NotImplementedError()

    def upload_video_from_path(self, file_path):
        self._validate_auth_credentials()

        raise NotImplementedError()

    def _get_upload_url(self):
        auth_handler = auth.WixHmacAuthHandler(self.api_key, self.api_secret)

        headers = {
            'x-wix-upload-nonce': os.urandom(6).encode("hex"),
            'x-wix-upload-ts':    str(time.time())
        }

        headers      = auth_handler.add_auth(method="GET", path=Client.WIX_MEDIA_UPLOAD_URL_PATH, headers=headers)

        opener       = urllib2.build_opener(urllib2.HTTPHandler)
        request      = urllib2.Request(Client.WIX_MEDIA_UPLOAD_URL, headers=headers)
        response     = opener.open(request)

        return json.loads(response.read())

    def _upload_to_pm_from_stream(self, fp, file_name, media_type):

        # Get URL for uploading file
        metadata   = self._get_upload_url()
        upload_url = metadata['upload_url']

        files   = {'file': (file_name, fp)}
        data    = {'media_type': media_type}
        headers = {
            'x-wix-orig-upload-url': urlparse(upload_url).path,
            'x-wix-upload-nonce':    os.urandom(6).encode("hex"),
            'x-wix-upload-ts':       str(time.time())
        }

        auth_handler = auth.WixHmacAuthHandler(self.api_key, self.api_secret)

        headers = auth_handler.add_auth("POST", urlparse(upload_url).path, headers)
        response = requests.post(upload_url, files=files, data=data, headers=headers)

        return json.loads(response.content)[0]