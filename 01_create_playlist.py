import googleapiclient.discovery

from _authorize import authorize_user

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

print("Authorizing user...")

credentials = authorize_user(SCOPES)
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

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
