from gtts import gTTS
import io

def synthesize_speech(text, lang="ru"):
    tts = gTTS(text=text, lang=lang)
    # Создаем временный файл с нужным суффиксом
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix="speech.mp3")
    tmp_file.close()  # Закрываем файл, чтобы gTTS мог записать
    tts.save(tmp_file.name)  # Сохраняем аудио в файл
    return tmp_file.name  # Возвращаем путь к файлу
