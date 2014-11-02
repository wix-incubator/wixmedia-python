from media import Media
import json


class Video(Media):
    def __init__(self, video_id, service_host, client):
        super(Video, self).__init__(video_id, client)

        self.service_host = service_host

    def get_url(self):
        return "/".join(['http://%s' % self.service_host, self.id])

    # returns: video encoding status: 'IN-QUEUE', 'INPROGRESS', 'READY', 'FAILED'
    def get_video_status(self):
        metadata = self.get_metadata(refresh=True)

        return metadata['op_status']

    def get_encoded_videos(self, refresh=False):
        metadata = self.get_metadata(refresh=refresh)

        file_info = json.loads(metadata['file_info'])
        return {k: Video(id, self.service_host, self.client) for k, id in file_info['ready_videos'].iteritems()}