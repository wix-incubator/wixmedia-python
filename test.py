from wix import media

client = media.Client(api_key="my_key", api_secret="my_secret")
image  = client.upload_image_from_path('/files/images/cat.jpg')

image_id = image.get_id()
print image_id

############

from wix import media

image_id = 'ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'

client = media.Client()
image  = client.get_image_from_id(image_id)

print image.fit(width=120, height=120) \
           .unsharp() \
           .oil() \
           .adjust(brightness=60, contrast=-40) \
           .get_url()

############

image.reset()
print image.canvas(width=480, height=240, alignment='faces', ext_color='ffffff').get_url()

image.reset()
print image.fill(width=480, height=240, alignment='top-left').get_url()

image.reset()
print image.fit(width=480, height=240, resize_filter=media.Lanczos2SharpFilter).get_url()

image.reset()
print image.crop(x=15, y=40, width=100, height=100).get_url()

image.reset()
print image.fit(width=120, height=120) \
           .adjust(brightness=60, contrast=-40) \
           .get_url()

image.reset()
print image.fit(width=120, height=120) \
           .auto_adjust() \
           .get_url()

image.reset()
print image.fit(width=120, height=120) \
           .quality(7) \
           .baseline() \
           .get_url()

image.reset()
wm_id = 'ggl-685734655894940532967/images/128766b24054482f8477bfbf2d426936/wm.jpg'
print image.watermark(wm_id=wm_id, opacity=45, alignment='top-left', scale=0).get_url()