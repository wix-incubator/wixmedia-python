from media import Media


class Video(Media):
    def __init__(self, video_id, service_host, client):
        super(Video, self).__init__(video_id, client)

        self.service_host = service_host

    def get_url(self):
        return "/".join(['http://%s' % self.service_host, self.id])