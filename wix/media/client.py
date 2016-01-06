from exceptions import GeneralError, UploadError
import functools
import urllib2
import json
import os
from image import Image
from video import Video
from audio import Audio
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
                        raise GeneralError(e.reason)

                    client.get_auth_token()
                    retry_count += 1
                else:
                    raise

        return result

    return _func


class Client(object):

    def __init__(self, api_key=None, api_secret=None, auth_service='WIX',
                 metadata_service_host='mediacloud.wix.com',
                 image_service_host='media.wixapps.net',
                 video_service_host='storage.googleapis.com'):

        self._api_key      = api_key
        self._api_secret   = api_secret
        self._auth_token   = ''
        self._auth_service = auth_service

        self._image_service_host    = image_service_host
        self._video_service_host    = video_service_host
        self._metadata_service_host = metadata_service_host

        self._wix_media_image_upload_url = 'http://%s/files/upload/url' % self._metadata_service_host
        self._wix_media_audio_upload_url = 'http://%s/files/upload/url' % self._metadata_service_host
        self._wix_media_video_upload_url = 'http://%s/files/video/upload/url' % self._metadata_service_host

        if auth_service == 'WIXTENANT':
            self._wix_media_auth_token_url   = 'http://%s/auth/tenant/token' % self._metadata_service_host
        else:
            self._wix_media_auth_token_url   = 'http://%s/auth/token' % self._metadata_service_host

        self._wix_media_get_file_info_url_prefix = 'http://%s/files/' % self._metadata_service_host

    @property
    def api_key(self):
        return self._api_key

    @property
    def api_secret(self):
        return self._api_secret

    def get_image_from_id(self, image_id):
        return Image(image_id=image_id, service_host=self._image_service_host, client=self)

    def upload_image_from_path(self, file_path):
        with open(file_path, 'r') as fp:
            return self.upload_image_from_stream(fp, os.path.basename(file_path), self._wix_media_image_upload_url)

    def upload_image_from_stream(self, fp, file_name, upload_url_endpoint):
        metadata = self._upload_to_pm_from_stream(fp, file_name, "picture", upload_url_endpoint)

        return Image(image_id=metadata['file_url'], service_host=self._image_service_host, client=self)

    def get_video_from_id(self, video_id):
        return Video(video_id=video_id, service_host=self._video_service_host, client=self)

    def upload_video_from_path(self, file_path, encoding_options=None):
        with open(file_path, 'r') as fp:
            return self.upload_video_from_stream(fp, os.path.basename(file_path), self._wix_media_video_upload_url, encoding_options)

    def upload_video_from_stream(self, fp, file_name, upload_url_endpoint, encoding_options=None):
        parts = dict()
        if encoding_options:
            parts.update({'encoding_options': encoding_options})

        metadata = self._upload_to_pm_from_stream(fp, file_name, "video", upload_url_endpoint, **parts)

        return Video(video_id=metadata['file_url'], service_host=self._video_service_host, client=self)

    def get_audio_from_id(self, audio_id):
        return Audio(audio_id=audio_id, service_host=self._video_service_host, client=self)

    def upload_audio_from_path(self, file_path):
        with open(file_path, 'r') as fp:
            return self.upload_audio_from_stream(fp, os.path.basename(file_path), self._wix_media_audio_upload_url)

    def upload_audio_from_stream(self, fp, file_name, upload_url_endpoint):
        metadata = self._upload_to_pm_from_stream(fp, file_name, "music", upload_url_endpoint)

        return Audio(audio_id=metadata['file_url'], service_host=self._video_service_host, client=self)

    def get_auth_token(self):
        self._auth_token = auth_token.get_auth_token(self._api_key, self._api_secret, self._wix_media_auth_token_url, auth_service=self._auth_service)

    def get_media_metadata_from_service(self, metadata_id):

        if not self._auth_token:
            self.get_auth_token()

        metadata = self._get_media_metadata_from_service(metadata_id)
        return metadata

    def _upload_to_pm_from_stream(self, fp, file_name, media_type, upload_url_endpoint, **parts):

        if not self._auth_token:
            self.get_auth_token()

        upload_url = self._get_upload_url(upload_url_endpoint)
        metadata   = self._upload_to_url(upload_url, fp, file_name, media_type, **parts)

        return metadata

    @retry_auth
    def _get_upload_url(self, upload_url_endpoint):

        headers = {'Authorization': AUTH_SCHEME + ' ' + self._auth_token}
        print headers
        http_status, content, _ = http_utils.get(upload_url_endpoint, headers)

        if http_status != 200:
            raise UploadError('failed to get upload url: http_status=%d' % http_status)

        metadata = json.loads(content)
        return metadata['upload_url']

    @retry_auth
    def _upload_to_url(self, upload_url, fp, file_name, media_type, **parts):

        fields  = {"media_type": media_type}
        fields.update(parts)

        files   = {'file': {'filename': file_name, 'content': fp.read()}}
        headers = {'Authorization':  AUTH_SCHEME + ' ' + self._auth_token}

        http_status, content, _ = http_utils.post_multipart(upload_url, headers, fields, files)

        if http_status != 200:
            raise UploadError('failed to upload file: http_status=%d' % http_status)

        return json.loads(content)[0]

    @retry_auth
    def _get_media_metadata_from_service(self, metadata_id):

        headers = {'Authorization': AUTH_SCHEME + ' ' + self._auth_token}

        url = '%s%s' % (self._wix_media_get_file_info_url_prefix, metadata_id)
        http_status, content, _ = http_utils.get(url, headers)

        if http_status != 200:
            raise GeneralError('failed to get file metadata: http_status=%d' % http_status)

        return json.loads(content)


class TenantClient(Client):

    def __init__(self, user_id=None, admin_secret=None, metadata_service_host=None, image_service_host=None, video_service_host='storage.googleapis.com'):
        super(TenantClient, self).__init__(
            api_key=user_id, api_secret=admin_secret, auth_service='WIXTENANT',
            metadata_service_host=metadata_service_host,
            image_service_host=image_service_host,
            video_service_host=video_service_host
        )


