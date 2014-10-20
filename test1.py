from wix import media

client = media.Client(api_key="my_key", api_secret="my_secret")
image  = client.upload_image_from_path('/files/images/dog.jpg')

print image.get_path()
print image.watermark(opacity=45, scale=0).get_img_tag()


############


image_path = 'goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/dog.png'
client = media.Client()

image = client.get_image_from_path(image_path)

print image.srz(width=120, height=120, alignment="top-left") \
           .adjust(brightness=60, contrast=-40) \
           .oil() \
           .blur(22) \
           .sharpen(0.3) \
           .get_img_tag(alt="dog")


#image.reset()
#
#print image.watermark(opacity=45, scale=0).get_img_tag()
#image.reset()
#print image.watermark(opacity=45, alignment='top-left', scale=0).get_img_tag()