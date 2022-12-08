import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload

from _authorize import authorize_user

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

credentials = authorize_user(SCOPES, load_from_cache=True)
service = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

playlists = service.playlists().list(part="snippet", mine=True).execute()
for playlist in playlists.get("items"):
    print(playlist.get("snippet").get("title"))

service.videos().insert(part="snippet,status", body={
    "snippet": {
        "title": "One",
        "description": "The First One"
    },
    "status": {
        "privacyStatus": "unlisted",
        "selfDeclaredMadeForKids": False
    }
}, media_body=MediaFileUpload("1.mov")).execute()
