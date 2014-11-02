import sys
sys.path.append('..')

from wix import media

client = media.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

try:
    print "Uploading video ..."

    video = client.upload_video_from_path('/path/to/video.mp4')

    print "Video file was uploaded."
except:
    video_id = 'wixmedia-samples/video/000ed2d2451a4cc29b173d0506996ea0/FiveDaysManhattanShort1080p.mp4'
    video = client.get_video_from_id(video_id)
    print "Stock video file is used."

print
print "Uploaded video url:", video.get_url()

try:
    print "Waiting for video encoding to finish..."
    encoding_status = video.get_video_status(timeout=60)
    print "Encoding Status:", encoding_status

    if encoding_status == 'READY':
        print
        print "Encoded videos:"

        ready_videos = video.get_encoded_videos()
        for k, ready_video in ready_videos.iteritems():
            print ready_video.get_url()
except:
    print "Failed to get video information. " \
          "Check your settings:\nAPI_KEY: %s\nAPI_SECRET: %s" % \
          (client._api_key, client._api_secret)