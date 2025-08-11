from gtts import gTTS
import io

def synthesize_speech(text, lang="ru"):
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp
