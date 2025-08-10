from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import time

def upload_video(file_path, title, description, tags, thumbnail_path=None):
    # Авторизация с OAuth2 (для refresh token)
    from google.oauth2.credentials import Credentials

    creds = Credentials(
        token=None,
        refresh_token=os.getenv("YT_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("YT_CLIENT_ID"),
        client_secret=os.getenv("YT_CLIENT_SECRET")
    )

    youtube = build('youtube', 'v3', credentials=creds)

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
    response = None

    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Загрузка: {int(status.progress() * 100)}%")

    print(f"Видео загружено: https://youtu.be/{response['id']}")

    if thumbnail_path:
        print("Загрузка кастомной обложки...")
        for _ in range(5):  # retry попытки
            try:
                youtube.thumbnails().set(
                    videoId=response['id'],
                    media_body=MediaFileUpload(thumbnail_path)
                ).execute()
                print("Обложка успешно установлена")
                break
            except Exception as e:
                print(f"Ошибка загрузки обложки: {e}")
                time.sleep(3)
