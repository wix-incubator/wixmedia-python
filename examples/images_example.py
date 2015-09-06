import os
import sys
sys.path.append('..')
from wix import media

SAMPLE_MEDIA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "sample_media"))


# wixmp
client = media.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

# wixmp tenant
# client = media.TenantClient(user_id="YOUR_USER_ID", admin_secret="YOUR_ADMIN_SECRET",
#                             metadata_service_host="YOUR_TENANT_METADATA_HOST",
#                             image_service_host="YOUR_TENANT_IMAGE_HOST")

try:
    path_to_image = os.path.join(SAMPLE_MEDIA_DIR, 'parrot.jpg')
    image = client.upload_image_from_path(path_to_image)

    print "Image was uploaded."
except Exception as e:
    image_id = 'wixmedia-samples/images/cdf1ba9ec9554baca147db1cb6e011ec/parrot.jpg'
    image = client.get_image_from_id(image_id)

    print "Stock image file is used."

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
print image.crop(x=900, y=70, width=1050, height=730).get_url()

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
