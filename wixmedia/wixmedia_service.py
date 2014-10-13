from .wixmedia_image import WixMediaImage


class WixMediaService(object):

    def __init__(self, api_key, api_secret):
        pass

    # returns metadata on uploaded file: possible only file_url
    def upload_file_from_path(self, filepath):

        metadata = self._upload_to_pm_from_path(filepath)

        return WixMediaImage(metadata['uri'])

    def upload_file_from_stream(self, fp, filename):

        metadata = self._upload_to_pm_from_stream(fp, filename)

        return WixMediaImage(metadata['file_url'])

    def _upload_to_pm_from_path(self, filepath):
        return dict()

    def _upload_to_pm_from_stream(self, fp, filename):
        return dict()