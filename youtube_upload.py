from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def upload_video(file_path, title, description, tags):
    youtube = build(
        'youtube', 'v3',
        developerKey=os.getenv("YOUTUBE_API_KEY")
    )
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"Видео загружено: https://youtu.be/{response['id']}")
