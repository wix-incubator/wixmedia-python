from wixmedia import wixmedia_image

url   = 'http://media.wixapps.net/goog:234234234234234/ae1d86b24054482f8477bfbf2d426936.png/dog.png'
image = wixmedia_image.WixMediaImage(url)
#print image

#print image.crop(x=10, y=10, width=120, height=120).adjust().filter().get_img_tag()
#image.reset()

print image.srz(width=120, height=120, alignment="top-left") \
           .adjust(brightness=60) \
           .filter("oil", blur=22) \
           .get_img_tag(alt="dog")
image.reset()

#print image.srz(width=120, height=120).adjust("auto", contrast=53).filter("oil", blur=22).get_img_tag()

############

## from wixmedia import wixmedia_service

## service = wixmedia_service.WixMediaService(api_key="my_key", api_secret="my_secret")

## image = service.upload_image_from_path('/files/images/dog.jpg')

## print image.crop().adjust().filter().get_img_tag()
