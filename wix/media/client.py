from datetime import datetime
from urlparse import urlparse
from uuid import uuid4
from io import BytesIO
import mimetypes
import calendar
import urllib2
import json
import os
from .exceptions import GeneralError, UploadError
import image
import auth


class Client(object):

    METADATA_SERVICE_HOST     = 'mediacloud.wix.com'
    WIX_MEDIA_UPLOAD_URL_PATH = '/files/upload/api/url'
    WIX_MEDIA_UPLOAD_URL      = 'http://%s%s' % (METADATA_SERVICE_HOST, WIX_MEDIA_UPLOAD_URL_PATH)
    # IMAGE_SERVICE             = 'media.wixapps.net'
    IMAGE_SERVICE             = '107.178.253.0'

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
            'x-wix-upload-ts':    Client.get_utc_now_ts()
        }

        headers = auth_handler.add_auth(method="GET", path=Client.WIX_MEDIA_UPLOAD_URL_PATH, headers=headers)

        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            request = urllib2.Request(Client.WIX_MEDIA_UPLOAD_URL.encode("utf-8"), headers=headers)
            response = opener.open(request)
        except urllib2.HTTPError as e:
            raise UploadError(e.reason())

        if response.code != 200:
            raise UploadError('failed to get upload url: http_status=%d' % response.code)

        return json.loads(response.read())

    def _upload_to_pm_from_stream(self, fp, file_name, media_type):

        # Get URL for uploading file
        metadata   = self._get_upload_url()
        upload_url = metadata['upload_url']

        fields = {"media_type": media_type}
        files  = {'file': {'filename': file_name, 'content': fp.read()}}
        data, content_type = self.encode_multipart(fields, files)

        headers = {
            'Content-Type':          content_type,
            'Content-Length':        str(len(data)),
            'x-wix-orig-upload-url': urlparse(upload_url).path,
            'x-wix-upload-nonce':    os.urandom(6).encode("hex"),
            'x-wix-upload-ts':       Client.get_utc_now_ts()
        }

        auth_handler = auth.WixHmacAuthHandler(self.api_key, self.api_secret)
        headers = auth_handler.add_auth("POST", urlparse(upload_url).path, headers)

        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(upload_url.encode("utf-8"), data=data, headers=headers)
        response = opener.open(request)

        if response.code != 200:
            raise UploadError('failed to upload file: http_status=%d' % response.code)

        return json.loads(response.read())[0]

    def encode_multipart(self, fields, files, boundary=None):

        def escape_quote(s):
            return s.replace('"', '\\"')

        if boundary is None:
            boundary = uuid4().hex

        lines = []

        for name, value in fields.items():
            lines.extend((
                '--{0}'.format(boundary),
                'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
                '',
                str(value),
            ))

        for name, value in files.items():
            filename = value['filename']
            if 'mimetype' in value:
                mimetype = value['mimetype']
            else:
                mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            lines.extend((
                '--{0}'.format(boundary),
                'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(
                        escape_quote(name), escape_quote(filename)),
                'Content-Type: {0}'.format(mimetype),
                '',
                value['content'],
            ))

        lines.extend((
            '--{0}--'.format(boundary),
            '',
        ))

        s = BytesIO()
        for element in lines:
            s.write(str(element))
            s.write('\r\n')
        body = s.getvalue()

        content_type = 'multipart/form-data; boundary={0}'.format(boundary)

        return body, content_type

    @staticmethod
    def get_utc_now_ts():
        return calendar.timegm(datetime.utcnow().utctimetuple())