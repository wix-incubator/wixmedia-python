wixmedia-python SDK
===================

This library allows you to upload files and perform various manipulations on uploaded images. 
These manipulations include, but are not limited to, resizing, cropping, rotating, sharpening, watermarking, face-detection and applying numerous filters. 
This functionality eliminates the need for offline processing in order to optimize images for web development. 
The resulting files are saved for later usage, so image processing occurs only once per each permutation.

## Overview ##
Uses [Google App Engine](http://appengine.google.com) with [Wix](http://wix.com) for image manupulaitons for web developers.

## Downloading ##

Installing the Wixmedia package is as simple as adding it to your project's include path.  

If you're using git, you can just clone down the repo like this:

```
git clone git@github.com:wix/wixmedia-python.git
```

__Note__: If you don't have git or would rather install by unpacking a Zip or Tarball, you can always grab the latest version of the package from [the downloads page](https://github.com/wix/wixmedia-python/archive/master.zip). 


## Wixmedia API ##
Wix provides Wixmedia library for uploading files and performing manipulations on images.

## Wixmedia Usage ##

### Uploading files ###

It’s easy to upload files using the Wixmedia Python Library.
For example:

```
from wixmedia import wixmedia_service

service = wixmedia_service.WixMediaService(api_key="my_key", api_secret="my_secret")

image = service.upload_file_from_path('/files/images/dog.jpg')

print image.crop().adjust().filter().get_img_tag()
```

### Rendering images ###

After uploading an image, you can easily apply any manipulation suggested by Wix using the API documented here. 
For example:

```
from wixmedia import wixmedia_image

image = wixmedia_image.WixMediaImage('uri')

print image.get_img_tag(width=4, alt="golan")
print image.get_img_tag()

print image.crop().adjust().filter().get_img_tag()
```

#### API List ####
All the APIs conform to a URI structure in the form of: 

```
http(s)://endpoint.com/file-id/operation/params(p_value, comma-separated)/filename.ext
```
For example:
```
http://endpont.com/5d958389e0a2.jpg/srz/w_480,h_240,q_75,us_0.50_1.20_0.00/dog.jpg
```

##### Image Transformation Operations #####

Applies one (or more) of the following transformation operations to an image:
- Scaled resize with aligned crop   [srz]
- Scaled resize (without crop)   [srb]
- Canvas
- Fill
- Crop

###### srz - scaled resize with aligned crop ######

Scaled and resize with aligned crop, followed by unsharp mask. Most useful shortcut for simple image optimization, while maintaining good balance between output size and quality.

```
srz(self, w, h, q, a, radius, amount, threshold)
```

Parameter | value | Description
----------|-------|------------
w (mandatory)|Integer|The width constraint (pixels).
h (mandatory)|Integer|The height constraint (pixels).
q (optional)|Integer (%)|The quality constraint if jpg. Values are between 0 and 100. ``` q=auto would give the default falue: 75```
a (optional)|string|The position pointing the place from which to start cropping  the picture (the cropping alignment). ``` a=auto would give the default option: Central cropping.``` see values in the table below.
us (optional)|float_float_float|The unshark mask, built from three values, described in the table below. ```(default value: 0.00).```

a optional values:

Value | Description
------|------------
c|center of the image. 
t|central top part of the image.
tl|top left part of the image.
tr|top right part of the image.
b|central bottom part of the image. 
bl|bottom left part of the image.
br|bottom right part of the image. 
l|central left part of the image. 
r|central right part of the image. 
f|face-recognition based alignment.

us optional values:

Value | Description
------|------------
r|the unsharp mask radius. default value: 0.50.
a|the unsharp mask amount default value: 0.20
t|the unsharp mask threshold.

####### Sample Request #######
```
image = wixmedia_image.WixMediaImage('uri', "dog.jpg")
image.srz(w=480, h=240, q=75, a='tl', radius=0.50, amount=1.20, threshold=0.00)
```
would generate the URL:
```
http://endpoint.com/5d958389e0a2.jpg/srz/w_480,h_240,q_75,a_tl,us_0.50_1.20_0.00/dog.jpg
```

###### srb - scaled resize without crop ######

Resizes the image to fit within the width and height boundaries without cropping or scaling the image, but will not increase the size of the image if it is smaller than the output size. 
The resulting image will maintain the same aspect ratio of the input image.

```
srb(self, w, h, q, radius, amount, threshold)
```

Parameter | value | Description
----------|-------|------------
w (mandatory)|Integer|The width constraint (pixels).
h (mandatory)|Integer|The height constraint (pixels).
q (optional)|Integer (%)|The quality constraint if jpg. Values are between 0 and 100. ``` q=auto would give the default falue: 75```
us (optional)|float_float_float|The unshark mask, built from three values: r (the unsharp mask radius. default value: 0.50.), a (the unsharp mask amount default value: 0.20), t (the unsharp mask threshold.  default value: 0.00).

####### Sample Request #######
```
image = wixmedia_image.WixMediaImage('uri', "dog.jpg")
image.srb(w=480, h=240, q=75)
```
would generate the URL:
```
http://endpoint.com/5d958389e0a2.jpg/srb/w_480,h_240,q_75,us_0.50_1.20_0.00/dog.jpg
```
###### Canvas ######

Resizes the image canvas, filling the width and height boundaries and crops any excess image data. The resulting image will match the width and height constraints without scaling the image.

```
canvas(self, w, h, q, a)
```

Parameter | value | Description
----------|-------|------------
w (mandatory)|Integer|The width constraint (pixels).
h (mandatory)|Integer|The height constraint (pixels).
q (optional)|Integer (%)|The quality constraint if jpg. Values are between 0 and 100. ``` q=auto would give the default falue: 75```
a (optional)|string|The position pointing the place from which to start cropping  the picture (the cropping alignment). see optional values in the table below.

a optional values:

Value | Description
------|------------
c|Focus on the center of the image, both vertical and horizontal center.
t|Focus on the top of the image, horizontal center.
tl|Focus on the top left side of the image.
tr|Focus on the top right side of the image.
b|Focus on the bottom of the image, horizontal center.
bl|Focus on the bottom left side of the image.                                                                                br|Focus on the bottom right side of the image.                                                                               l|Focus on the left side of the image, vertical center.                                                                       r|Focus on the right side of the image, vertical center.
f|Focus on a face on the image. Detects a face in the picture and centers on it. When multiple faces are detected in the picture, the focus will be on one of them.
fs|Focus on all faces in the image. Detects multiple faces and centers on them. Will do a best effort to have all the faces in the new image, depending on the size of the new canvas.

####### Sample Request ####### 
```
image = wixmedia_image.WixMediaImage('uri', "dog.jpg")
image.canvas(w=480, h=240, q=75, a='fs')
```
would generate the URL:
```
http://endpoint.com/5d958389e0a2.jpg/canvas/w_480,h_240,q_75,a_fs/dog.jpg
```
and:
```
image.canvas(w=480, h=240, q=75)
```
would generate: (giving a its default values)
```
http://endpoint.com/5d958389e0a2.jpg/canvas/w_480,h_240,q_75/dog.jpg
```

##### Image Adjustment Operation #####

Applies an adjustment to an image. Parameters values can be either specific or set to “auto”. An auto parameter without any values performs a general auto-enhancement

##### Image Filter Operation #####

Applies one (or more) of the following effects to an image: 
- Oil paint effect
- Negative effect
- Pixelate effect 
- Regular
- Based on facial recognition
- Blur
- Sharpen

##### Image Watermark Operation #####

Enables users to apply watermark such as copyright notice in order to protect their images. 
* The system allows replacing watermark if needed.

###### Watermarks ######

Enables users to apply watermark such as copyright notice in order to protect their images. The system allows to replace watermark if needed.

```
watermark(self, op, a, scl)
```

Parameter | value | Description
----------|-------|------------
op (optional)|Integer (%)|The Watermark opacity. values are between 0 and 100. ```op=auto would give the default value: 100.```
a (optional)|string|The watermark position. ``` a=auto would give the default option: center.``` for more details, see the table below.
scl (optional)|Integer (%)|Watermark horizontal scaling as percents of the requested image width. Values are between 0 and 100. ```scl=auto would give the default value: 0```

a optional values:

Value | Description
------|------------
c|center of the image. 
t|central top part of the image.
tl|top left part of the image.
tr|top right part of the image.
b|central bottom part of the image. 
bl|bottom left part of the image.
br|bottom right part of the image. 
l|central left part of the image. 
r|central right part of the image. 
f|face-recognition based alignment.

Sample Request
--------------
```
image = wixmedia_image.WixMediaImage('uri', "dog.jpg")
image.watermark(op=45, scl=0)
```
would generate the URL:
```
http://endpoint.com/5d958389e0a2.jpg/wm/op_45,scl_0/dog.jpg
```
and:
```
image.watermark(op=100, a='tl', scl=50)
```
would generate: (giving a its default values)
```
http://endpoint.com/5d958389e0a2.jpg/wm/op_100,a_tl,scl_50/dog.jpg
```

Sample Response
---------------
```
{ "error": 0, "error_description": "success", "wm_filepath": "/media/123456_wxm_88dfc1cb1babd66a7bc635dbb599d94d.jpg" }
```
