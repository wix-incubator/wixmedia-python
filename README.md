
Wix Media Python SDK
====================

Wix Media Platform is a collection of APIs for image, audio, and video files, and services for storing, serving, uploading, and managing those files.

In addition to this basic functionality, Wix Media Platform includes the following components: 
* **Image Services** give you powerful REST APIs that enable you to manipulate images hosted on Wix Media Platform on the fly.
* **Video Services** let you host, transcode, and serve video seamlessly across any Internet-enabled device. 
* **Audio Services** enable you to upload professional audio files, which are automatically transcoded into web-friendly formats.
* **Dashboard** provides the ability to upload and organize media, view statistics about media serving, and produce ready-to-use code snippets. 
* **SDKs** include client- and server-side libraries.

Managing media files includes user-repository metadata and media-collections service. Result of processing media files, such as resized images, encoded audio or transcoded video, are stored in Google Cloud Storage.

The Wix Media Python SDK is a Python wrapper, which provides easier access to the Wix Media Plaform APIa and services.

## Setup ##

Installing wixmedia-python package is as simple as adding it to your project's include path.  

If you're using git, you can just clone down the repo like this:

```
git clone git@github.com:wix/wixmedia-python.git
```

__Note__: If you don't have git or would rather install by unpacking a Zip or Tarball, you can always grab the latest version of the package from [the downloads page](https://github.com/wix/wixmedia-python/archive/master.zip). 

## Usage ##

### Uploading files ###

The following example shows server-to-server image upload:

```python
from wix import media

client = media.Client(api_key="my_key", api_secret="my_secret")
image  = client.upload_image_from_path('/files/images/cat.jpg')

print image.get_id()
```

The code snippet above gives the following image id as output:
```
ggl-685734655894940532967/images/ae1d86b24054482f8477bfbf2d426936/cat.jpg
```

### Rendering Media ###

#### Images ####
Images can be uploaded to the Wix Media Platform using this package.
Once an image was uploaded, you cab apply various manipulations on it. These manipulations include, but are not limited to, resizing, cropping, rotating, sharpening, watermarking, face-detection and applying numerous filters. 

For more information about image manipulation in your apps, browse the [Images SDK documentation.](https://github.com/wix/wixmedia-python/blob/master/images.md).

#### Audio ####
The platform supports two different modes for storing and manipulating audio files - a Simple Audio mode and a Professional Audio mode.

In Simple Audio mode, the user can upload an mp3 file of any quality, and use it as-is. In Professional Audio mode the user can upload a WAV file of at least 44.1KHz/16bit. This file is then automatically transcoded into additional versions: several high-quality versions (like FLAC and high-bitrate mp3), and one (relatively) low-quality version for immediate playback. The high quality files are stored securely, thus can be used in commercial music-selling applications.

For more information about audio support in your apps, browse the Audio SDK documentation.

#### Video ####
Every video file uploaded into the service is automatically encoded into additional formats and qualities. These are particularly designed so that the videos will be playable on any browser and internet-connected device.
The system allows for both public and secure storage of the video files. Public videos can be streamed or downloaded without the viewer authorization. Secured videos can be used in commercial video applications.

For more information about video support in your apps, browse the Video SDK documentation.
