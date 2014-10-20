from .exceptions import GeneralError
import image


class Client(object):

    METADATA_SERVICE_HOST         = 'mediacloud.wix.com'
    WIX_MEDIA_UPLOAD_URL_ENDPOINT = 'http://%s/files/upload/url' % METADATA_SERVICE_HOST
    IMAGE_SERVICE                 = 'prospero.wixapps.net'

    def __init__(self, api_key=None, api_secret=None):
        self.api_key    = api_key
        self.api_secret = api_secret

    @staticmethod
    def get_image_from_id(image_id):
        return image.Image(image_id=image_id, service_host=Client.IMAGE_SERVICE)

    def upload_image_from_path(self, file_path):

        if not self.api_key or not self.api_secret:
            raise GeneralError('invalid authorization parameters: initialize api key and secret')

        metadata = self._upload_to_pm_from_path(file_path)
        metadata['file_url'] = 'wix-ac831a9e-577b-4018-b8b8-88499c811234/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'

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

        metadata = self._upload_to_pm_from_stream(fp, filename)
        metadata['file_url'] = 'wix-ac831a9e-577b-4018-b8b8-88499c811234/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'

        return image.Image(image_id=metadata['file_url'], service_host=Client.IMAGE_SERVICE)

    def _upload_to_pm_from_path(self, file_path):
        return dict(uri='uri')

    def _upload_to_pm_from_stream(self, fp, file_name):
        return dict(uri='uri')