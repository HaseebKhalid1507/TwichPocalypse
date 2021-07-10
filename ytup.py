import datetime
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = './youtube-secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def uploadmp4(post):
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'

    request_body = {
        'snippet': {
            'categoryI': 24,
            'title': post.title + " || " + post.link_flair_text.split(' ')[1],
            'description': 'Credits: ' + post.link_flair_text.split(' ')[1],
            'tags': ['Twich', post.link_flair_text.split(' ')[1], 'livestreamfail', 'memes', 'clips']
        },
        'status': {
            'privacyStatus': 'public',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload("videos/" + post.title + ".mp4")

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()