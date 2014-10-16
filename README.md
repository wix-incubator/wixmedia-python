wixmedia-python SDK
===================

The Wix Media Services are a collection of tools for handling online media files, such as images, audio and video. The services include storage, serving, uploading, transcoding and processing, client-side widgets and SDKs, user-repository metadata and media-collections. Result of processing media files, such as resized images, encoded audio or transcoded video, are stored in Google Cloud Storage.

The Wix Media Services is now offered for developers as a third party service within Google Cloud Platform.

This package is a Python wrapper for Wixmedia Image RESTful API, which allows you to upload files and perform various manipulations on them. 

## Setup ##

Installing the Wixmedia package is as simple as adding it to your project's include path.  

If you're using git, you can just clone down the repo like this:

```
git clone git@github.com:wix/wixmedia-python.git
```

__Note__: If you don't have git or would rather install by unpacking a Zip or Tarball, you can always grab the latest version of the package from [the downloads page](https://github.com/wix/wixmedia-python/archive/master.zip). 


## Wixmedia API ##

Wixmedia provides web developers a versatile infrastructure for file manipulations easily accessable through Wixmedia's RESTful Image API. 
In addition, Wixmedia offers the following Python wrapper, which provides easier access to the Wixmedia API (by automatically generating Wixmedia URL requests).

For more details about Wixmedia Image RESTful API, you are welcome to browse our documentation [here](https://github.com/wix/wixmedia/master/README.md). 

## Wixmedia Usage ##

### Uploading files ###

Media files can be uploaded to the Wix Media Services using various widgets, APIs and SDKs (Python, Java, PHP, Javascript). The following example shows server-to-server image upload:

```python
from wixmedia import wixmedia_service

service = wixmedia_service.WixMediaService(api_key="my_key", api_secret="my_secret")
image   = service.upload_image_from_path('/files/images/dog.jpg')

print image.srz(width=120, height=120) \
           .adjust(brightness=60) \
           .filter("oil", blur=22) \
           .get_img_tag(alt="dog")
```

### Rendering files ###

#### Images ####

Images can be uploaded to the Wix Media Services platform the followind SDK.
Once an image was uploaded, the service can apply various manipulations on it. These manipulations include, but are not limited to, resizing, cropping, rotating, sharpening, watermarking, face-detection and applying numerous filters. 

For more information about image manipulation in your apps, browse the Wix Media Services - [Images documentation.](https://github.com/wix/wixmedia-python/blob/master/ImagesDoc.md).

#### Audio ####

Audio files can be be uploaded to the Wix Media Services platform using various widgets, APIs and SDKs.
The service supports two different modes for storing and manipulating audio files - a Simple Audio mode and a Professional Audio mode.

In Simple Audio mode, the user can upload an mp3 file of any quality, and use it as-is. In Professional Audio mode the user can upload a WAV file of at least 44.1KHz/16bit. This file is then automatically transcoded into additional versions: several high-quality versions (like FLAC and high-bitrate mp3), and one (relatively) low-quality version for immediate playback. The high quality files are stored securely, thus can be used in commercial music-selling applications.

For more information about audio support in your apps, browse the Wix Media Services - Audio documentation.

#### Video ####

Video files can be be uploaded to the Wix Media Services platform using various widgets, APIs and SDKs.
Every video file uploaded into the service is automatically encoded into additional formats and qualities. These are particularly designed so that the videos will be playable on any browser and internet-connected device.
The system allows for both public and secure storage of the video files. Public videos can be streamed or downloaded without the viewer authorization. Secured videos can be used in commercial video applications.

For more information about video support in your apps, browse the Wix Media Services - Video documentation.
