Wix Media Python SDK
--------------------
Audio Manipulation
==================
Wix Media Platform provides web developers a versatile infrastructure for audio files manipulations via the Wix Media Python library.

## Usage ##

### Uploading Audio Files ###

To upload an audio file using Wix Media Python library, follow the steps in the example:

```python
from wix import media
client = media.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

print "Uploading audio ..."
audio = client.upload_audio_from_path('/path/to/audio.mp3')
print "Uploaded audio url:", audio.get_url()
```
### Working with Audio ###

After uploading a video, you can easily retreive information about it using the SDK:

#### Audio URL ####

Using the *get_url* function, for example:

```python
print audio.get_url()
```
