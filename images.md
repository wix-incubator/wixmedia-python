Wix Media Python SDK
--------------------
Image Manipulation
===========================
Wix Media Platform provides web developers a versatile infrastructure for image manipulations easily accessable through the [Wix Media Images RESTful API](http://media.wixapps.net/playground/docs/images_restfull_api.html). The Wix Media Python library provides a wrapper over the API.

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

The code snippet above gives the following image-id as output:
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
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,usm_0.50_0.20_0.00,oil,con_-40,br_60/cat.jpg
```
----------------
__Note__: 
All rendered URLs (as shown in the previous *img* tag) conform to the following structure:
```
http://host.com/user-id/media-type/file-id/version/operation/params(p_value, comma-separated),manipulations(p_value, comma-separated)/filename.ext
```
Using this python package eliminates the need to manually construct such urls. For more information about the URLs browse [Wix Media Images RESTful API](http://media.wixapps.net/playground/docs/images_restfull_api.html) documentation.

-----------------

##### Image Transformation Operations #####

The following image transformations are available (one per image maipulation request):
- Canvas
- Fill
- Fit
- Crop


###### Canvas ######

Resizes the image canvas, filling the width and height boundaries and crops any excess image data. The resulting image will match the width and height constraints without scaling the image.

```python
canvas(width, height, alignment=None, ext_color=None)
```

Parameter | value | Description
----------|-------|------------
width *(mandatory)*|Integer|The width constraint (pixels).
height *(mandatory)*|Integer|The height constraint (pixels).
alignment *(optional)*|string|The position pointing the place from which to start cropping  the picture. See optional values in the table below.```default: center```
ext_color *(optional)*|string (RGB)| the extension color, in case the canvas size is larger than the image itself. Please note that the string expected is a 6 hexadecimal digits representing RRGGBB. 

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
print image.canvas(width=480, height=240, alignment='faces', ext_color='ffffff').get_url()
```
would generate the URL:
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/canvas/h_240,w_480,a_fs,c_ffffff/cat.jpg
```

###### Fill ######

Creates an image with the specified width and height while retaining original image proportion. If the requested proportion is different from the original proportion, only part of the original image may be used to fill the area specified by the width and height.

```python
fill(width, height, resize_filter=None, alignment=None)
```

Parameter | value | Description
----------|-------|------------
width *(mandatory)*|Integer|The width constraint (pixels).
height *(mandatory)*|Integer|The height constraint (pixels).
resize_filter *(optional)*|string|The resize filter to be used. One of the values below. ```default: LanczosFilter```
alignment *(optional)*|string|The position pointing the place from which to start cropping  the picture. See optional values in the table below.```default: center```

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

resize_filter optional values + descriptions (view links):

[PointFilter](http://www.imagemagick.org/Usage/filter/#point)|[BoxFilter](http://www.imagemagick.org/Usage/filter/#box)|[TriangleFilter](http://www.imagemagick.org/Usage/filter/#triangle)|[HermiteFilter](http://www.imagemagick.org/Usage/filter/#hermite)
--------|---------|---------|--------
[**HanningFilter**](http://www.imagemagick.org/Usage/filter/#hanning)|[**HammingFilter**](http://www.imagemagick.org/Usage/filter/#hamming)|[**BlackmanFilter**](http://www.imagemagick.org/Usage/filter/#balckman)|[**GaussianFilter**](http://www.imagemagick.org/Usage/filter/#gaussian)
[**QuadraticFilter**](http://www.imagemagick.org/Usage/filter/#quadratic)|[**CubicFilter**](http://www.imagemagick.org/Usage/filter/#cubics)|[**CatromFilter**](http://www.imagemagick.org/Usage/filter/#catrom)|[**MitchellFilter**](http://www.imagemagick.org/Usage/filter/#mitchell)
[**JincFilter**](http://www.imagemagick.org/Usage/filter/#jinc)|[**SincFilter**](http://www.imagemagick.org/Usage/filter/#sinc)|[**SincFastFilter**](http://www.imagemagick.org/Usage/filter/#sinc)|[**KaiserFilter**](http://www.imagemagick.org/Usage/filter/#kaiser)
[**WelchFilter**](http://www.imagemagick.org/Usage/filter/#welch)|[**ParzenFilter**](http://www.imagemagick.org/Usage/filter/#parzen)|[**BohmanFilter**](http://www.imagemagick.org/Usage/filter/#bohman)|[**BartlettFilter**](http://www.imagemagick.org/Usage/filter/#bartlett)
[**LagrangeFilter**](http://www.imagemagick.org/Usage/filter/#lagrange)|[**LanczosFilter**](http://www.imagemagick.org/Usage/filter/#lanczos)|[**LanczosSharpFilter**](http://www.imagemagick.org/Usage/filter/#lanczos_sharp)|[**Lanczos2Filter**](http://www.imagemagick.org/Usage/filter/#lanczos2)
[**Lanczos2SharpFilter**](http://www.imagemagick.org/Usage/filter/#lanczos2sharp)|[**RobidouxFilter**](http://www.imagemagick.org/Usage/filter/#robidoux)|[**RobidouxSharpFilter**](http://www.imagemagick.org/Usage/filter/#robidoux_sharp)|[**CosineFilter**](http://www.imagemagick.org/Usage/filter/#cosine)

**Sample Request**

```python
print image.fill(width=480, height=240, alignment='top-left').get_url()
```
would generate the URL:
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fill/h_240,w_480/cat.jpg
```

###### Fit ######

Resizes the image to fit to the specified width and height while retaining original image proportion. The entire image will be visible but not necessarily fill the area specified by the width and height.

```python
fit(width, height, resize_filter=None)
```

Parameter | value | Description
----------|-------|------------
width *(mandatory)*|Integer|The width constraint (pixels).
height *(mandatory)*|Integer|The height constraint (pixels).
resize_filter *(optional)*|string|The resize filter to be used. One of the in the table below. ```default: LanczosFilter```

resize_filter optional values + descriptions (view links):

[PointFilter](http://www.imagemagick.org/Usage/filter/#point)|[BoxFilter](http://www.imagemagick.org/Usage/filter/#box)|[TriangleFilter](http://www.imagemagick.org/Usage/filter/#triangle)|[HermiteFilter](http://www.imagemagick.org/Usage/filter/#hermite)
--------|---------|---------|--------
[**HanningFilter**](http://www.imagemagick.org/Usage/filter/#hanning)|[**HammingFilter**](http://www.imagemagick.org/Usage/filter/#hamming)|[**BlackmanFilter**](http://www.imagemagick.org/Usage/filter/#balckman)|[**GaussianFilter**](http://www.imagemagick.org/Usage/filter/#gaussian)
[**QuadraticFilter**](http://www.imagemagick.org/Usage/filter/#quadratic)|[**CubicFilter**](http://www.imagemagick.org/Usage/filter/#cubics)|[**CatromFilter**](http://www.imagemagick.org/Usage/filter/#catrom)|[**MitchellFilter**](http://www.imagemagick.org/Usage/filter/#mitchell)
[**JincFilter**](http://www.imagemagick.org/Usage/filter/#jinc)|[**SincFilter**](http://www.imagemagick.org/Usage/filter/#sinc)|[**SincFastFilter**](http://www.imagemagick.org/Usage/filter/#sinc)|[**KaiserFilter**](http://www.imagemagick.org/Usage/filter/#kaiser)
[**WelchFilter**](http://www.imagemagick.org/Usage/filter/#welch)|[**ParzenFilter**](http://www.imagemagick.org/Usage/filter/#parzen)|[**BohmanFilter**](http://www.imagemagick.org/Usage/filter/#bohman)|[**BartlettFilter**](http://www.imagemagick.org/Usage/filter/#bartlett)
[**LagrangeFilter**](http://www.imagemagick.org/Usage/filter/#lagrange)|[**LanczosFilter**](http://www.imagemagick.org/Usage/filter/#lanczos)|[**LanczosSharpFilter**](http://www.imagemagick.org/Usage/filter/#lanczos_sharp)|[**Lanczos2Filter**](http://www.imagemagick.org/Usage/filter/#lanczos2)
[**Lanczos2SharpFilter**](http://www.imagemagick.org/Usage/filter/#lanczos2sharp)|[**RobidouxFilter**](http://www.imagemagick.org/Usage/filter/#robidoux)|[**RobidouxSharpFilter**](http://www.imagemagick.org/Usage/filter/#robidoux_sharp)|[**CosineFilter**](http://www.imagemagick.org/Usage/filter/#cosine)

**Sample Request**

```python
print image.fit(width=480, height=240, resize_filter=media.Lanczos2SharpFilter).get_url()
```
would generate the URL:
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_240,w_480,rf_25/cat.jpg
```

###### Crop ######

Crops the image based on the supplied coordinates, starting at the x, y coordinates along with the width and height parameters.

```python
crop(x, y, width, height)
```

Parameter | Value | Description
----------|-------|------------
x *(mandatory)*|Integer|The x-pixel-coordinate to start cropping from. (represents the top-left corner point of the cropped area).
y *(mandatory)*|Integer|The y-pixel-coordinate to start cropping from. (represents the top-left corner point of the cropped area).
width *(mandatory)*|Integer|The width constraint (pixels).
height *(mandatory)*|Integer|The height constraint (pixels).

**Sample Request**
```python
print image.crop(x=15, y=40, width=100, height=100).get_url()
```
would generate the URL:
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/crop/y_40,h_100,w_100,x_15/cat.jpg
```

##### Image Adjustment Operation #####

###### Adjust ######

Applies an adjustment to an image.

```python
adjust(**props_dict)
```
the parameters may be one or more of the following options:

function | parameter(s) | Description
---------|--------------|------------
brightness *(optional)*|Integer (%)|brightness. ```value between -100 and 100```
contrast *(optional)*|Integer (%)|contrast ```value between -100 and 100```
saturation *(optional)*|Integer (%)|saturation ```value between -100 and 100```
hue *(optional)*|Integer (%)|hue ```value between -100 and 100```
quality *(optional)*|Integer (%)|The quality constraint if JPEG image. Values are between 0 and 100. ```default: 75```

**Sample Request**
```python
print image.fit(width=120, height=120) \
           .adjust(brightness=60, contrast=-40) \
           .get_url()
```
would generate the URL: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,con_-40,br_60/cat.jpg
```

###### Auto-Adjust ######

Performs a general auto-enhancement to an image.

```python
auto_adjust()
```

*Sample Request:*
```python
print image.fit(width=120, height=120) \
           .auto_adjust() \
           .get_url()
```
would generate the URL: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,auto_adj/cat.jpg
```

*** 

##### Oil Filter #####

Applies an oil paint effect on an image.

```python
oil()
```

*Sample Request:*
```python
print image.fit(width=120, height=120) \
           .oil() \
           .get_url()
```
would generate the URL: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,oil/cat.jpg
```

*** 

##### Negative Filter #####

Negates the colors of the image.

```python
neg()
```

*Sample Request:*
```python
print image.fit(width=120, height=120) \
           .neg() \
           .get_url()
```
would generate the URL: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,neg/cat.jpg
```

***

##### Pixelate Filter #####

Applies a pixelate effect to the image. The parameter value is the width of pixelation squares, (in pixels).

```python
pixelate(value)
```

*Sample Request:*
```python
print image.fit(width=120, height=120) \
           .pixelate(20) \
           .get_url()
```
would generate the URL: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,pix_20/cat.jpg
```

***

##### Pixelate Faces Filter #####

Applies a pixelate effect to faces in the image. The parameter value is the width of pixelation squares, (in pixels).

```python
pixelate_faces(value)
```

*Sample Request:*
```python
print image.fit(width=120, height=120) \
           .pixelate_faces(35) \
           .get_url()
```
would generate the URL: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,pixfs_35/cat.jpg
```

***

##### Blur Filter #####

Applies a blur effect to the image. The parameter value indicates the blur in percents.

```python
blur(value)
```

*Sample Request:*
```python
print image.fit(width=120, height=120) \
           .blur(50) \
           .get_url()
```
would generate the URL: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,blur_50/cat.jpg
```

*** 

##### Sharpening Filter #####

Applies a sharpening filter on the image, using the radius parameter. please note that the radius’ value is a float number.

```python
sharpen(radius)
```

*Sample Request:*
```python
print image.fit(width=120, height=120) \
           .sharpen(0.70) \
           .get_url()
```
would generate the URL: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,shrp_0.70/cat.jpg
```

***

##### Unsharp Mask Filter #####

The Unsharp Mask, applies the filter using radius, amount & threshold parameters. (see table below)

```python
unsharp(radius=0.5, amount=0.2, threshold=0.0)
```

optional values:

Value | Description | Valid values
------|-------------|-------------
radius|sharpening mask radius|0 to image size
amount|sharpening mask amount|0 to 100
threshold|shapening mask threshold|0 to 255

*Sample Request:*
```python
print image.fit(width=120, height=120) \
           .unsharp(radius=0.4, amount=0.2, threshold=0.0) \
           .get_url()
```
would generate the URL: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/fit/h_120,w_120,usm_0.40_0.20_0.00/cat.jpg
```

*** 

**Multiple Filters Sample Requests**
```python
image.filter(oil, neg)
```
would generate: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/<operation>,oil,neg/dog.png
```
***
```python
image.neg()
     .pixelate(108)
```
would generate: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/<operation>,neg,pix_108/dog.png
```
***
```python
image.oil()
     .neg()
     .pixelate(125) 
     .sharpen(0.40)
```
would generate: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/<operation>,oil,neg,pix_125,shrp_0.40/dog.png
```



##### Image Watermark Operation #####

Enables users to apply watermark such as copyright notice in order to protect their images. 
* The system allows replacing watermark if needed.

```python
watermark(wm_id, opacity=None, alignment=None, scale=None)
```

Parameter | value | Description
----------|-------|------------
wm_id *(mandatory)*|string|The watermark image id. Please notice that the wmid format is similar to the file_id format used earlier in the URL. Must be url-plus encoded.
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
image = wixmedia_image.WixMediaImage('http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/dog.png')
image.watermark(wm_id='ggl-685734655894940532967%2Fimages%2F128766b24054482f8477bfbf2d426936%2Fwm.jpg', opacity=45, scale=0)
```
would generate the URL:
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/wm/wmid_ggl-685734655894940532967%2Fimages%2F128766b24054482f8477bfbf2d426936%2Fwm.jpg, op_45,scl_0/dog.png
```
and:
```python
image.watermark(opacity=100, alignment='top-left', scale=50)
```
would generate: (giving a its default values)
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/wm/op_100,a_tl,scl_50/dog.png
```

**Sample Response**
```
{ "error": 0, "error_description": "success", "wm_filepath": "ggl-685734655894940532967/images/88dfc1cb1babd66a7bc635dbb599d94d/dog.png" }
```

###### More Options ######

**JPEG Options**

option | parameter(s) | description
-------|------------|------------
baseline|-|An option for JPEGs only. Applies baseline encoding on the image, instead of progressive encoding.
quality|Integer (%)|Quality of the image, values between 0 and 100 

**Sample Requests**
```python
image = wixmedia_image.WixMediaImage('http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/dog.png')
image.baseline()
```
would generate the URL:
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/<operation>,bl/dog.png
```
and:
```python
image.quality(0.70)
```
would generate: 
```
http://media.wixapps.net/ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/v1/<operation>,q_0.70/dog.png
```
