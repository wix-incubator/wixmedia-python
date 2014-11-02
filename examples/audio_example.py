import sys
sys.path.append('..')

from wix import media

client = media.Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

try:
    print "Uploading audio ..."

    audio = client.upload_audio_from_path('/path/to/audio.mp3')

    print "audio file was uploaded."
except Exception as e:
    audio_id = 'wixmedia-samples/music/000b6f01dbf2491792c77be69eb228b0/RYYBJamSession7.mp3'
    audio    = client.get_audio_from_id(audio_id)
    print "Stock audio file is used."

print
print "Uploaded audio url:", audio.get_url()