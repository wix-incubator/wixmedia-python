from datetime import datetime


class Media(object):
    def __init__(self, media_id, client):
        self.id          = media_id
        self.client      = client

        self.metadata    = None
        self.metadata_ts = None

    def get_id(self):
        return self.id

    def metadata_id(self):
        user_id, partition, file_id, _ = self.id.split('/', 4)
        return file_id

    def get_url(self):
        raise NotImplementedError()

    def get_metadata(self, refresh=False):
        if self.metadata is None or refresh:
            self.metadata    = self._get_metadata_from_service()
            self.metadata_ts = datetime.utcnow()

        return self.metadata

    def _get_metadata_from_service(self):
        return self.client.get_media_metadata_from_service(self.metadata_id())