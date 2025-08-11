import os
import requests
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
from moviepy.video.fx import Crop

font_path = os.path.join(os.path.dirname(__file__), "LibertinusSans-Bold.ttf")

def download_file(url, filename):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    return filename

def create_vertical_video(quote, background_url, bg_type):
    bg_file = "background.mp4" if bg_type == "video" else "background.jpg"
    download_file(background_url, bg_file)

    if bg_type == "video":
        clip = VideoFileClip(bg_file).subclipped(0, 10).resized(height=1920)
        clip = Crop(x_center=clip.w / 2, width=1080, height=1920, y_center=clip.h / 2)(clip)
    elif bg_type == "image":
        clip = ImageClip(bg_file).with_duration(10).resized((1080, 1920))  # 10 секунд или сколько надо
    else:
        raise ValueError(f"Неизвестный тип: {bg_type}")
    
    # if bg_type == "image":
    #     clip = ImageClip(bg_file).with_duration(10).resized((1080, 1920))
    # else:
    #     # clip = VideoFileClip(bg_file).subclipped(0, 10).resized(height=1920)
    #     # x_center = clip.w / 2
    #     # clip = crop(clip, x_center=x_center, width=1080)
    #     clip = clip.resize(height=1920)
    #     clip = Crop(x_center=clip.w / 2, width=1080, height=1920, y_center=clip.h / 2)(clip)

    txt_clip = TextClip(
        text=quote,
        font=font_path,
        font_size=50,
        color='white',
        method='caption',
        size=(int(clip.w * 0.8), 300)
    ).with_position('center').with_duration(10)

    final = CompositeVideoClip([clip, txt_clip])
    output_path = "final_video.mp4"
    final.write_videofile(output_path, fps=30, codec='libx264')
    return output_path
