import os
import requests
import moviepy.editor as mp

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
        clip = mp.ImageClip(bg_file, duration=10)
    else:
        clip = mp.VideoFileClip(bg_file).subclip(0, 10).resize(height=1080)

    txt_clip = mp.TextClip(
        quote,
        fontsize=50,
        color='white',
        font='Arial-Bold',
        method='caption',
        size=(clip.w * 0.8, None)
    ).set_position('center').set_duration(10)

    final = mp.CompositeVideoClip([clip, txt_clip])
    output_path = "final_video.mp4"
    final.write_videofile(output_path, fps=24)
    return output_path
