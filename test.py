import pprint
from wix import media

client = media.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

try:
    image = client.upload_image_from_path('/path/to/image.jpg')

    print "Image was uploaded."
except Exception as e:
    image_id = 'wixmedia-samples/images/cdf1ba9ec9554baca147db1cb6e011ec/parrot.jpg'
    image  = client.get_image_from_id(image_id)

    print "Stock file is used."

print image.get_id()

print image.fit(width=420, height=420) \
           .unsharp() \
           .oil() \
           .adjust(brightness=10, contrast=-15) \
           .get_url()

############

image.reset()
print image.canvas(width=480, height=240, ext_color='ffffff').get_url()

image.reset()
print image.fill(width=480, height=240).get_url()

image.reset()
print image.fit(width=480, height=240, resize_filter=media.Lanczos2SharpFilter).get_url()

image.reset()
print image.crop(x=1900, y=800, width=800, height=900).get_url()

image.reset()
print image.fit(width=120, height=120) \
           .adjust(brightness=10, contrast=-15) \
           .get_url()

image.reset()
print image.fit(width=420, height=420) \
           .oil() \
           .get_url()

image.reset()
print image.fit(width=420, height=420) \
           .neg() \
           .get_url()

image.reset()
print image.fit(width=420, height=420) \
           .pixelate(5) \
           .get_url()

image.reset()
print image.fit(width=420, height=420) \
           .blur(5) \
           .get_url()

image.reset()
print image.fit(width=420, height=420) \
           .sharpen(0.8) \
           .get_url()

image.reset()
print image.fit(width=420, height=420) \
           .unsharp(radius=0.4, amount=0.2, threshold=0.0) \
           .get_url()

image.reset()
print image.fit(width=420, height=420) \
           .baseline() \
           .get_url()

image.reset()
print image.fit(width=420, height=420) \
           .quality(35) \
           .get_url()

print image.fit(width=420, height=420) \
           .crop(x=60, y=60, width=300, height=300) \
           .unsharp() \
           .get_url()

#######
import time

client = media.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")
video = client.upload_video_from_path('/path/to/video.mp4')

print "Video file was uploaded."

print video.get_id()
print video.get_url()

encoding_status = video.get_video_status()

# polling video encoding status ...
while encoding_status not in ["READY", "FAILED"]:
    print "Encoding Status:", encoding_status
    time.sleep(1)

    encoding_status = video.get_video_status()

print "Encoding Status:", encoding_status

if encoding_status == 'READY':
    print
    print "Encoded videos:"

    ready_videos = video.get_encoded_videos()
    for k, ready_video in ready_videos.iteritems():
        print ready_video.get_url()