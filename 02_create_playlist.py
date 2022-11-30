import googleapiclient.discovery

from _authorize import authorize_user

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
credentials = authorize_user(SCOPES)
service = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Inserting playlist #1
service.playlists().insert(
    part="snippet",
    body={
        "snippet": {
            "title": "PL #1"
        }
    }
).execute()

# Inserting playlist #2
service.playlists().insert(
    part="snippet",
    body={
        "snippet": {
            "title": "PL #2"
        }
    }
).execute()

# Listing playlists...
for playlist in service.playlists().list(mine=True, part="snippet").execute()["items"]:
    print(playlist["snippet"]["channelId"], playlist["id"], playlist["snippet"]["title"])