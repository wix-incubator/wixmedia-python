import urlparse
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

    def upload_image_from_path(self, file_path):

        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

        auth_handler = auth.WixHmacAuthHandler(self.api_key, self.api_secret)
        headers = {}
        headers = auth_handler.add_auth(method="GET", path=Client.WIX_MEDIA_UPLOAD_URL_PATH, headers=headers)
        # Get URL for uploading file
        metadata = self._upload_to_pm_from_path(file_path, headers)

        metadata['file_url'] = 'ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'

        # Upload file
        headers = auth_handler.add_auth(method="GET", path=metadata['file_url'], headers=headers)
        # call function which implements actual POST and pass new 'headers' to it
        # ...


        return image.Image(image_id=metadata['file_url'], service_host=Client.IMAGE_SERVICE)

    def upload_audio_from_path(self, file_path):

        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

    def upload_video_from_path(self, file_path):

        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

    def upload_file_from_stream(self, fp, filename):

        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

        auth_handler = auth.WixHmacAuthHandler(self.api_key, self.api_secret)
        headers = {}
        headers = auth_handler.add_auth(method="GET", path=Client.WIX_MEDIA_UPLOAD_URL_PATH, headers=headers)

        metadata = self._upload_to_pm_from_stream(fp, filename, headers)
        metadata['file_url'] = 'ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'

        return image.Image(image_id=metadata['file_url'], service_host=Client.IMAGE_SERVICE)

    def _upload_to_pm_from_path(self, file_path, headers):
        return dict(uri='uri')

    def _upload_to_pm_from_stream(self, fp, file_name, headers):
        return dict(uri='uri')