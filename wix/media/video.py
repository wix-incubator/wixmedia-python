from media import Media
from utils import BackOff
import json


class Video(Media):
    def __init__(self, video_id, service_host, client):
        super(Video, self).__init__(video_id, service_host, client)

    # returns: video encoding status: 'IN-QUEUE', 'INPROGRESS', 'READY', 'FAILED'
    def get_video_status(self, timeout=60):
        metadata        = self.get_metadata(refresh=True)
        encoding_status = metadata['op_status']

        back_off    = BackOff(max_wait_time=timeout)
        should_wait = True

        while encoding_status not in ["READY", "FAILED"] and should_wait:
            should_wait = back_off.wait()

            metadata        = self.get_metadata(refresh=True)
            encoding_status = metadata['op_status']

        return encoding_status

    def get_encoded_videos(self, refresh=False):
        metadata = self.get_metadata(refresh=refresh)

        ready_videos = list()
        for video_info in metadata['file_output']['video']:
            video_info['url'] = "/".join(['http://%s' % self.service_host, video_info['url']])
            ready_videos.append(video_info)

        return ready_videos
