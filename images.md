wixmedia-python SDK
-------------------
Image Manipulation
===========================
Wix Media Services provides web developers a versatile infrastructure for image manipulations easily accessable through the [Wix Media Images RESTful API](http://media.wixapps.net/playground/docs/images_restfull_api.html). The Wix Media Python library is a wrapper over the API.

## Usage ##

### Uploading Images ###

It’s easy to upload images using the Wix Media Python library. For example:

```python
from wix import media

client = media.Client(api_key="my_key", api_secret="my_secret")
image  = client.upload_image_from_path('/files/images/cat.jpg')

image_id = image.get_id()
print image_id

```

The code snippet above gives the following image id as output:
```
ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg
```

__Note__: Wix Media Services supports the followoing images file formats: JPEG, GIF and PNG.

### Rendering Images ###

After uploading an image, you can easily apply any manipulation as described later in the document.
For example:

```python
from wix import media

image_id = 'ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg'

client = media.Client()
image  = client.get_image_from_id(image_id)

print image.fit(width=120, height=120) \
           .unsharp() \
           .oil() \
           .adjust(brightness=60, contrast=-40) \
           .get_url()
```

The last code snippet applies image manipulation on a previously uploaded image and prints the URL for rendering the manipulated image. The URL can be embedded in an HTML *img* tag:

```html
http://prospero.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/fit/h_120,w_120/filter/usm_0.50_0.20_0.00,oil/adjust/con_-40,br_60/cat.jpg
```
----------------
__Note__: 
All rendered URLs (as shown in the previous *img* tag) conform to the following structure:
```
http://host.com/user-id/media-type/file-id/operation/params(p_value, comma-separated)/filename.ext
```
Using this python package eliminates the need to manually construct such urls. For more information about the URLs browse [Wix Media Images RESTful API](http://media.wixapps.net/playground/docs/images_restfull_api.html) documentation.

-----------------

##### Image Transformation Operations #####

The following image transformations are available (one per image maipulation request):
- srz (shortcut for applying *fill* transformation and unsharp mask)
- srb (shortcut for applying *fit* transformation and unsharp mask)
- Canvas
- Fill
- Fit
- Crop


###### srz ######

Scaled and resize with center crop, followed by unsharp mask. Most useful shortcut for simple image optimization, while maintaining good balance between output size and quality.

```python
srz(width, height, quality=None, radius=None, amount=None, threshold=None)
```

Parameter | value | Description
----------|-------|------------
width *(mandatory)*|Integer|The width constraint (pixels).
height *(mandatory)*|Integer|The height constraint (pixels).
quality *(optional)*|Integer (%)|The quality constraint if JPEG image. Values are between 0 and 100. ```default: 75```
blur *(optional)*|Float|Blur factor. Value > 1 is blurry, <1 is sharp. ```default: 1```
radius *(optional)*|Float|the unsharp mask radius. ```default: 0.50.```
amount *(optional)*|Float|the unsharp mask amount. ```default: 0.20.```
threshold *(optional)*|Float|the unsharp mask threshold. ```default: 0.00.```

**Sample Request**
```python
print image.srz(width=480, height=240, quality=85, blur=0.6, radius=0.60, amount=0.9, threshold=0.00).get_url()
```
would generate the URL:
```
http://prospero.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/srz/q_85,h_240,usm_0.60_0.90_0.00,w_480,blur_0.6/cat.jpg
```
###### srb - scaled resize without crop ######

Resizes the image to fit within the width and height boundaries without cropping or scaling the image, but will not increase the size of the image if it is smaller than the output size. The resulting image will maintain the same aspect ratio of the input image.

```python
srb(width, height, resize_filter=None, quality=None, radius=None, amount=None, threshold=None)
```

Parameter | value | Description
----------|-------|------------
width *(mandatory)*|Integer|The width constraint (pixels).
height *(mandatory)*|Integer|The height constraint (pixels).
resize_filter *(optional)*|Integer|The resize filter to be used. One of the following values: ```PointFilter, BoxFilter, TriangleFilter, HermiteFilter, HanningFilter, HammingFilter, BlackmanFilter, GaussianFilter, QuadraticFilter, CubicFilter, CatromFilter, MitchellFilter, JincFilter, SincFilter, SincFastFilter, KaiserFilter, WelshFilter, ParzenFilter, BohmanFilter, BartlettFilter, LagrangeFilter, LanczosFilter, LanczosSharpFilter, Lanczos2Filter, Lanczos2SharpFilter, RobidouxFilter, RobidouxSharpFilter, CosineFilter```. ```default: LanczosFilter```
quality *(optional)*|Integer (%)|The quality constraint if JPEG image. Values are between 0 and 100. ```default: 75```
radius *(optional)*|Float|the unsharp mask radius. ```default: 0.50.```
amount *(optional)*|Float|the unsharp mask amount. ```default: 0.20.```
threshold *(optional)*|Float|the unsharp mask threshold. ```default: 0.00.```

**Sample Request**
```python
print image.srb(width=480, height=240, quality=85).get_url()
```
would generate the URL:
```
http://prospero.wixapps.net/wix-ac831a9e-577b-4018-b8b8-88499c811234/images/ae1d86b24054482f8477bfbf2d426936/srb/q_85,h_240,w_480/cat.jpg
```


###### Canvas ######

Resizes the image canvas, filling the width and height boundaries and crops any excess image data. The resulting image will match the width and height constraints without scaling the image.

```python
canvas(width, height, quality=None, alignment=None)
```

Parameter | value | Description
----------|-------|------------
width *(mandatory)*|Integer|The width constraint (pixels).
height *(mandatory)*|Integer|The height constraint (pixels).
quality *(optional)*|Integer (%)|The quality constraint if JPEG image. Values are between 0 and 100. ```default: 75```
alignment *(optional)*|string|The position pointing the place from which to start cropping  the picture (the cropping alignment). see optional values in the table below.```default: center```

alignment optional values:

Value | Description
------|------------
center|Focus on the center of the image, both vertical and horizontal center.
top|Focus on the top of the image, horizontal center.
top-left|Focus on the top left side of the image.
top-right|Focus on the top right side of the image.
bottom|Focus on the bottom of the image, horizontal center.
bottom-left|Focus on the bottom left side of the image.
bottom-right|Focus on the bottom right side of the image.
left|Focus on the left side of the image, vertical center.
right|Focus on the right side of the image, vertical center.
face|Focus on a face on the image. Detects a face in the picture and centers on it. When multiple faces are detected in the picture, the focus will be on one of them.
faces|Focus on all faces in the image. Detects multiple faces and centers on them. Will do a best effort to have all the faces in the new image, depending on the size of the new canvas.

**Sample Request**
```python
print image.canvas(width=480, height=240, quality=70, alignment='faces').get_url()
```
would generate the URL:
```
http://prospero.wixapps.net/wix-ac831a9e-577b-4018-b8b8-88499c811234/images/ae1d86b24054482f8477bfbf2d426936/canvas/q_70,h_240,a_fs,w_480/cat.jpg
```
and:
```python
image.canvas(width=480, height=240, quality=75)
```
would generate (giving 'alignment' its default values):
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/canvas/w_480,h_240,q_75/dog.png
```


###### fill ######

Create an image with the exact given width and height while retaining original proportions. Use only part of the image that fills the given dimensions. Only part of the original image might be visible if the required proportions are different than the original ones.

```python
fill(width, height ,quality=None)
```

Parameter | value | Description
----------|-------|------------
width *(mandatory)*|Integer|The width constraint (pixels).
height *(mandatory)*|Integer|The height constraint (pixels).
quality *(optional)*|Integer (%)|The quality constraint if JPEG image. Values are between 0 and 100. ```default falue: 75```

**Sample Request**

```python
image = wixmedia_image.WixMediaImage('http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/dog.png')
image.fill(width=480, height=240, quality=75)
```
would generate the URL:
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/fill/w_480,h_240,q_75/dog.png
```
and:
```
image.fill(width=480, height=240)
```
would generate: (with the quality's default value)
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/fill/w_480,h_240/dog.png   
```
###### crop ######

Crops the image based on the supplied coordinates, starting at the x, y pixel coordinates along with the width and height parameters.

```python
crop(x, y, width, height, quality=None)
```

Parameter | Value | Description
----------|-------|------------
x *(mandatory)*|Integer|The x-pixel-coordinate to start cropping from. (represents the top-left corner point of the cropped area).
y *(mandatory)*|Integer|The y-pixel-coordinate to start cropping from. (represents the top-left corner point of the cropped area).
width *(mandatory)*|Integer|The width constraint (pixels).
height *(mandatory)*|Integer|The height constraint (pixels).
quality *(optional)*|Integer (%)|The quality constraint if JPEG image. Values are between 0 and 100. ```default value:75```

**Sample Request**
```python
image = wixmedia_image.WixMediaImage('http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/dog.png')
image.crop(x=120, y=120, width=480, hdight=240, quality=75)
```
would generate the URL:
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/crop/x_120,y_120,w_480,h_240,q_75/dog.png
```
and:
```
image.crop(x=120, y=120, width=480, height=240)
```
would generate: (with the quality's default value)
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/crop/x_120,y_120,w_480,h_240/dog.png
```


##### Image Adjustment Operation #####

Applies an adjustment to an image. Parameters values can be either specific or set to “auto”. An auto parameter without any values performs a general auto-enhancement.

```python
adjust(*props, **adjust_props)
```
the parameters may be one or more of the following options:

function | parameter(s) | Description
---------|--------------|------------
br *(optional)*|Integer (%)|brightness. ```value between -100 and 100```
con *(optional)*|Integer (%)|contrast ```value between -100 and 100```
sat *(optional)*|Integer (%)|saturation ```value between -100 and 100```
hue *(optional)*|Integer (%)|hue ```value between -100 and 100```
auto *(optional)*|-|auto adjust

**Sample Requests**
```python
image = wixmedia_image.WixMediaImage('http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/dog.png')

image.adjust(auto)  
```
would generate the URL: 
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/adjust/auto/dog.png
```
***
```pyhton
image.adjust(br=-82, con=12, hue=50)  
```
would generate: 
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/adjust/br_-82,con_12,hue_50/dog.png
```
***
```python
image.adjust(con=60)
```
would generate: 
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/adjust/con_60/dog.png
```
***
```python
image.adjust(b=100) 
```
would generate: 
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/adjust/br_100/dog.png
```
##### Image Filter Operation #####

Applies one (or more) of the following effects to an image: 
- Oil paint effect
- Negative effect
- Pixelate effect 
- Regular
- Based on facial recognition
- Blur
- Sharpen

```python
filter(*funcs, **filter_funcs)
```
Parameters value can be either specific values:

function | parameter(s) | Description
---------|--------------|------------
oil|-|Applies an oil paint effect on an image.
neg|-|Negates the colors of the image.
pix|Integer|Applies a pixelate effect to the image. The parameter value is the width of pixelation squares, (in pixels).
pix_faces|Integer|Applies a pixelate effect to faces in the image. The parameter value is the width of pixelation squares, (in pixels).
blur|Integer (%)|Applies a blur effect to the image. The parameter value indicates the blur in percents.
sharpen|Integer_Integer_Ingteger|Sharpens the image using radius, amount & threshold parameters. (see table below) ``` when no values are supplied, sharpen is auto```

sharpen optional values:

Value | Description | Valid values
------|-------------|-------------
radius|sharpening mask radius|0 to image size
amount|sharpening mask amount|0 to 100
threshold|shapening mask threshold|0 to 255


**Sample Requests**
```python
image = wixmedia_image.WixMediaImage('http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/dog.png')

image.filter(blur=50)
```
would generate the URL:

```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/filter/blur_50/dog.png
```
***
```python
image.filter(oil, neg)
```
would generate: 
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/filter/oil,neg/dog.png
```
***
```python
image.filter(neg, pixelate=108)
```
would generate: 
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/filter/neg,pix_108/dog.png
```
***
```python
image.filter(sharpen(radius=100, amount=30, thershold=217))
```
would generate: 
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/filter/sharpen_100_30_217/dog.png
```
***
```python
image.filter(oil, neg, pixelate=125, sharpen(radius=100, amount=30, thershold=217)??????)
```
would generate: 
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/filter/oil,neg,pix_125,sharpen_100_30_217/dog.png
```


##### Image Watermark Operation #####

Enables users to apply watermark such as copyright notice in order to protect their images. 
* The system allows replacing watermark if needed.

```python
watermark(opacity=None, alignment=None, scale=None)
```

Parameter | value | Description
----------|-------|------------
opacity *(optional)*|Integer (%)|The Watermark opacity. values are between 0 and 100. ```op default value: 100.```
alignment *(optional)*|string|The watermark position. ``` a default option: center.``` for more details, see the table below.
scale *(optional)*|Integer (%)|Watermark horizontal scaling as percents of the requested image width. Values are between 0 and 100. ```scl efault value: 0```

alignment optional values:

Value | Description
------|------------
center|center of the image. 
top|central top part of the image.
top-left|top left part of the image.
top-right|top right part of the image.
bottom|central bottom part of the image. 
bottom-left|bottom left part of the image.
bottom-right|bottom right part of the image. 
left|central left part of the image. 
right|central right part of the image. 
face|face-recognition based alignment.
faces|focus on all faces in the image.

**Sample Request**
```python
image = wixmedia_image.WixMediaImage('http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/dog.png')
image.watermark(opacity=45, scale=0)
```
would generate the URL:
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/wm/op_45,scl_0/dog.png
```
and:
```python
image.watermark(opacity=100, alignment='top-left', scale=50)
```
would generate: (giving a its default values)
```
http://media.wixapps.net/goog-098152434167072483196/images/ae1d86b24054482f8477bfbf2d426936/wm/op_100,a_tl,scl_50/dog.png
```

**Sample Response**
```
{ "error": 0, "error_description": "success", "wm_filepath": "/goog-098152434167072483196/images/media/123456_wxm_88dfc1cb1babd66a7bc635dbb599d94d.jpg/dog.png" }
```
