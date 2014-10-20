from .exceptions import GeneralError
import image


class Client(object):

    METADATA1_SERVICE_HOST        = 'prospero.wixapps.net'
    WIX_MEDIA_UPLOAD_URL_ENDPOINT = 'http://%s/files/upload/url' % METADATA1_SERVICE_HOST
    IMAGE_SERVICE                 = '107.178.251.117'

    def __init__(self, api_key=None, api_secret=None):
        self.api_key    = api_key
        self.api_secret = api_secret

    @staticmethod
    def get_image_from_path(image_path):
        return image.Image(url_path=image_path, service_host=Client.IMAGE_SERVICE)

    def upload_image_from_path(self, file_path):
        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

        metadata = self._upload_to_pm_from_path(file_path)
        metadata['file_url'] = 'wix-123454167072483196/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'

        return image.Image(url_path=metadata['file_url'], service_host=Client.IMAGE_SERVICE)

    def upload_audio_from_path(self, file_path):
        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

    def upload_video_from_path(self, file_path):
        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

    def upload_file_from_stream(self, fp, filename):
        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

        metadata = self._upload_to_pm_from_stream(fp, filename)
        metadata['file_url'] = 'wix-123454167072483196/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'

        return image.Image(url_path=metadata['file_url'], service_host=Client.IMAGE_SERVICE)

    def _upload_to_pm_from_path(self, file_path):
        return dict(uri='uri')

    def _upload_to_pm_from_stream(self, fp, file_name):
        return dict(uri='uri')