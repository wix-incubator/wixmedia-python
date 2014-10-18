from .wixmedia_image import WixMediaImage


class WixMediaService(object):

    WIX_MEDIA_SERVICE_HOST        = 'prospero.wixapps.net'
    WIX_MEDIA_UPLOAD_URL_ENDPOINT = 'http://%s/files/upload/url' % WIX_MEDIA_SERVICE_HOST

    def __init__(self, api_key, api_secret):
        self.api_key    = api_key
        self.api_secret = api_secret

    def upload_image_from_path(self, filepath):

        metadata = self._upload_to_pm_from_path(filepath)

        return WixMediaImage(metadata['file_url'], metadata['original_filename'])

    def upload_audio_from_path(self, filepath):
        pass

    def upload_video_from_path(self, filepath):
        pass

    def upload_file_from_stream(self, fp, filename):

        metadata = self._upload_to_pm_from_stream(fp, filename)

        return WixMediaImage(metadata['file_url'], metadata['original_filename'])

    def _upload_to_pm_from_path(self, filepath):
        return dict(uri='uri')

    def _upload_to_pm_from_stream(self, fp, filename):
        return dict(uri='uri')