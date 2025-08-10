import os
import requests
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, TextClip

font_path = os.path.join(os.path.dirname(__file__), "Montserrat-Regular.ttf")

def download_file(url, filename):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    return filename

def create_video(quote, background_url, bg_type):
    bg_file = "background.mp4" if bg_type == "video" else "background.jpg"
    download_file(background_url, bg_file)

    if bg_type == "image":
        clip = ImageClip(bg_file, duration=10)
    else:
        clip = VideoFileClip(bg_file).subclipped(0, 10).resized(height=1080)

    txt_clip = TextClip(
        text=quote,
        font=font_path,
        font_size=50,
        color='white',
        method='caption',
        size=(clip.w * 0.8, None)
    ).set_position('center').set_duration(10)

    final = CompositeVideoClip([clip, txt_clip])
    output_path = "final_video.mp4"
    final.write_videofile(output_path, fps=24, codec='libx264')
    return output_path
