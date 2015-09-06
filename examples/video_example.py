import sys
sys.path.append('..')

from wix import media
from pprint import pprint


# wixmp
client = media.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

# wixmp tenant
# client = media.TenantClient(user_id="YOUR_USER_ID", admin_secret="YOUR_ADMIN_SECRET",
#                             metadata_service_host="YOUR_TENANT_METADATA_HOST",
#                             image_service_host="YOUR_TENANT_IMAGE_HOST")

try:
    print "Uploading video ..."

    # upload a video and output video only in mp4 format (default is: mp4 and webm)
    encoding_options = """
    {
        "file_output": {
            "video": {
                "format":["mp4"]
                }
            }
    }
    """

    video = client.upload_video_from_path('/path/to/video.mp4', encoding_options=encoding_options)

    print "Video file was uploaded."
except:
    video_id = 'wixmedia-samples/video/000ed2d2451a4cc29b173d0506996ea0/FiveDaysManhattanShort1080p.mp4'
    video = client.get_video_from_id(video_id)
    print "Stock video file is used."


try:
    print "Waiting for video encoding to finish..."
    encoding_status = video.get_video_status(timeout=60)
    print "Encoding Status:", encoding_status

    if encoding_status == 'READY':
        print
        print "Encoded videos:"

        ready_videos = video.get_encoded_videos()
        pprint(ready_videos)

except Exception as e:
    print "Failed to get video information: %s " \
          "Check your settings:\nAPI_KEY: %s\nAPI_SECRET: %s" % \
          (e.message, client._api_key, client._api_secret)