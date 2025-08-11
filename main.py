import os
import random
import requests
from video_maker import create_vertical_video
from youtube_upload import upload_video
from thumbnail import create_thumbnail
from quotes import get_russian_quote

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# def get_random_quote():
#     try:
#         res = requests.get("https://zenquotes.io/api/random", timeout=10)
#         if res.status_code == 200:
#             data = res.json()[0]
#             return f"{data['q']} — {data['a']}"
#     except:
#         pass
#     return "Stay positive and keep pushing forward!"

def get_random_background():
    headers = {"Authorization": PEXELS_API_KEY}
    query = random.choice(["motivation", "nature", "success", "inspiration"])

    if random.choice([True, False]):
        res = requests.get(f"https://api.pexels.com/v1/search?query={query}&per_page=50", headers=headers, timeout=10)
        if res.status_code == 200 and res.json().get("photos"):
            url = random.choice(res.json()["photos"])["src"]["original"]
            return url, "image"
    else:
        res = requests.get(f"https://api.pexels.com/videos/search?query={query}&per_page=50", headers=headers, timeout=10)
        if res.status_code == 200 and res.json().get("videos"):
            url = random.choice(res.json()["videos"])["video_files"][0]["link"]
            return url, "video"

    return None, None

if __name__ == "__main__":
    quote = get_russian_quote()
    background_url, bg_type = get_random_background()

    if not background_url:
        raise Exception("Не удалось получить фон с Pexels API.")

    video_path = create_vertical_video(quote, background_url, bg_type)

    # Скачиваем фон для обложки (если видео — берём первый кадр)
    bg_file = "thumb_bg.jpg"
    if bg_type == "image":
        r = requests.get(background_url)
        with open(bg_file, "wb") as f:
            f.write(r.content)
    else:
        # Для видео можно добавить логику извлечения первого кадра
        # Пока — скачиваем видео и берем первый кадр (упрощенно)
        from moviepy import VideoFileClip
        from PIL import Image
        import tempfile
        import shutil

        temp_video = "temp_video.mp4"
        r = requests.get(background_url)
        with open(temp_video, "wb") as f:
            f.write(r.content)
        clip = VideoFileClip(temp_video)
        frame = clip.get_frame(0)
        img = Image.fromarray(frame)
        img.save(bg_file)
        clip.close()
        os.remove(temp_video)

    thumbnail_path = create_thumbnail(bg_file, quote)

    upload_video(
        video_path,
        title=f"Motivation | {quote[:50]}",
        description=f"{quote}\n\n#motivation #success #inspiration",
        tags=["motivation", "success", "inspiration", "life", "mindset"],
        thumbnail_path=thumbnail_path
    )
