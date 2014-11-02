Wix Media Python SDK
--------------------
Video Manipulation
==================
Wix Media Platform provides web developers a versatile infrastructure for video manipulations via the Wix Media Python library.

## Usage ##

### Uploading Videos ###

To upload a video using Wix Media Python library, follow the steps in the example:

```python
from wix import media
import time

client = media.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")
video = client.upload_video_from_path('/path/to/video.mp4')

print "Video file was uploaded."

# Get the video by ID / URL:
print video.get_id()
print video.get_url() 
```
### Working with Videos ###

After uploading a video, you can easily retreive information about it using the SDK:

#### Video URL ####

Using the *get_url* function, for example:

```python
print video.get_url()
```

#### Video Status  ####

You can also get the video status using the *get_video_status* function. for example:

```python
print video.get_video_status()
```

#### Encoded Videos ####

You can get a list of all videos which are ready to be watched. using the *get_encoded_videos* function. for example:

```python
encoding_status = video.get_video_status()

if encoding_status == 'READY':
    print "Encoded videos:"

    ready_videos = video.get_encoded_videos()
    for k, ready_video in ready_videos.iteritems():
        print ready_video.get_url()
```
