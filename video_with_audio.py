from moviepy import VideoFileClip, AudioFileClip

def add_audio_to_video(video_path, audio_path, output_path="final_video_with_audio.mp4"):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")
    return output_path
