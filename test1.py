from wix import media

client = media.Client(api_key="my_key", api_secret="my_secret")
image  = client.upload_image_from_path('/files/images/cat.jpg')

image_id = image.get_id()
print image_id

############

from wix import media

image_id = 'wix-ac831a9e-577b-4018-b8b8-88499c811234/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'

client = media.Client()
image  = client.get_image_from_id(image_id)

print image.fit(width=120, height=120) \
           .unsharp() \
           .oil() \
           .adjust(brightness=60, contrast=-40) \
           .get_url()

############

#image.reset()
#print image.srz(width=480, height=240, quality=75, blur=0.6, radius=0.60, amount=0.9, threshold=0.00).get_url()
#
#image.reset()
#print image.srb(width=480, height=240, quality=85).get_url()
#
#image.reset()
#print image.canvas(width=480, height=240, quality=70, alignment='faces').get_url()


#
#print image.watermark(opacity=45, scale=0).get_img_tag()
#image.reset()
#print image.watermark(opacity=45, alignment='top-left', scale=0).get_img_tag()