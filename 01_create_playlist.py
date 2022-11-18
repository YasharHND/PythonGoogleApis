import googleapiclient.discovery

from _constants import *
from auth_manager import load_user_credentials

credentials = load_user_credentials()
youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# Inserting playlist #1
youtube.playlists().insert(
    part="snippet",
    body={
        "snippet": {
            "title": "PL #1"
        }
    }
).execute()

# Inserting playlist #2
youtube.playlists().insert(
    part="snippet",
    body={
        "snippet": {
            "title": "PL #2"
        }
    }
).execute()

# Listing playlists...
for playlist in youtube.playlists().list(mine=True, part="snippet").execute()["items"]:
    print(playlist["snippet"]["channelId"], playlist["id"], playlist["snippet"]["title"])

# YouTube Content ID (to get the contentOwnerId)
# youtubePartner = googleapiclient.discovery.build('youtubePartner', 'v1', credentials=credentials, static_discovery=False)
# contentOwners = youtubePartner.contentOwners().list(fetchMine=True).execute()
