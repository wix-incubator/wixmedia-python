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
/wix_image_id/srz/w_{w},h_{h},q_{q},a_{a},us_{r}_{a}_{t}/original_image_name.ext
```

Parameter | value | Description
----------|-------|------------
w (mandatory)|Integer|The width constraint (pixels).
h (mandatory)|Integer|The height constraint (pixels).

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
