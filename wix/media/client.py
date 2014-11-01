from exceptions import GeneralError, UploadError
import functools
import urllib2
import json
import os
from image import Image
from video import Video
import http_utils
import auth_token


AUTH_SCHEME = "MCLOUDTOKEN"


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

    IMAGE_SERVICE_HOST         = 'media.wixapps.net'
    VIDEO_SERVICE_HOST         = 'storage.googleapis.com'
    METADATA_SERVICE_HOST      = 'mediacloud.wix.com'
    WIX_MEDIA_IMAGE_UPLOAD_URL = 'http://%s/files/upload/url' % METADATA_SERVICE_HOST
    WIX_MEDIA_VIDEO_UPLOAD_URL = 'http://%s/files/video/upload/url' % METADATA_SERVICE_HOST
    WIX_MEDIA_AUTH_TOKEN_URL   = 'http://%s/auth/token' % METADATA_SERVICE_HOST
    WIX_MEDIA_GET_FILE_INFO_URL_PREFIX = 'http://%s/files/' % METADATA_SERVICE_HOST

    def __init__(self, api_key=None, api_secret=None):
        self.api_key    = api_key
        self.api_secret = api_secret
        self.auth_token = ''

    def get_image_from_id(self, image_id):
        return Image(image_id=image_id, service_host=Client.IMAGE_SERVICE_HOST, client=self)

    def upload_image_from_path(self, file_path):
        with open(file_path, 'r') as fp:
            return self.upload_image_from_stream(fp, os.path.basename(file_path), Client.WIX_MEDIA_IMAGE_UPLOAD_URL)

    def upload_image_from_stream(self, fp, file_name, upload_url_endpoint):
        metadata = self._upload_to_pm_from_stream(fp, file_name, media_type="picture", upload_url_endpoint=upload_url_endpoint)

        return Image(image_id=metadata['file_url'], service_host=Client.IMAGE_SERVICE_HOST, client=self)

    def get_video_from_id(self, video_id):
        return Video(video_id=video_id, service_host=Client.VIDEO_SERVICE_HOST, client=self)

    def upload_video_from_path(self, file_path):
        with open(file_path, 'r') as fp:
            return self.upload_video_from_stream(fp, os.path.basename(file_path), Client.WIX_MEDIA_VIDEO_UPLOAD_URL)

    def upload_video_from_stream(self, fp, file_name, upload_url_endpoint):
        metadata = self._upload_to_pm_from_stream(fp, file_name, media_type="video", upload_url_endpoint=upload_url_endpoint)

        return Video(video_id=metadata['file_url'], service_host=Client.VIDEO_SERVICE_HOST, client=self)

    def get_auth_token(self):
        self.auth_token = auth_token.get_auth_token(self.api_key, self.api_secret, Client.WIX_MEDIA_AUTH_TOKEN_URL)

    def _upload_to_pm_from_stream(self, fp, file_name, media_type, upload_url_endpoint):

        if not self.auth_token:
            self.get_auth_token()

        upload_url = self._get_upload_url(upload_url_endpoint)
        metadata   = self._upload_to_url(upload_url, fp, file_name, media_type)

        return metadata

    @retry_auth
    def _get_upload_url(self, upload_url_endpoint):

        headers = {'Authorization': AUTH_SCHEME + ' ' + self.auth_token}

        http_status, content, _ = http_utils.get(upload_url_endpoint, headers)

        if http_status != 200:
            raise UploadError('failed to get upload url: http_status=%d' % http_status)

        metadata = json.loads(content)
        return metadata['upload_url']

    @retry_auth
    def _upload_to_url(self, upload_url, fp, file_name, media_type):

        fields  = {"media_type": media_type}
        files   = {'file': {'filename': file_name, 'content': fp.read()}}
        headers = {'Authorization':  AUTH_SCHEME + ' ' + self.auth_token}

        http_status, content, _ = http_utils.post_multipart(upload_url, headers, fields, files)

        if http_status != 200:
            raise UploadError('failed to upload file: http_status=%d' % http_status)

        return json.loads(content)[0]

    @retry_auth
    def get_media_metadata_from_service(self, metadata_id):

        headers = {'Authorization': AUTH_SCHEME + ' ' + self.auth_token}

        url = '%s%s' % (Client.WIX_MEDIA_GET_FILE_INFO_URL_PREFIX, metadata_id)
        http_status, content, _ = http_utils.get(url, headers)

        if http_status != 200:
            raise GeneralError('failed to get file metadata: http_status=%d' % http_status)

        metadata = json.loads(content)
        return metadata