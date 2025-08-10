from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def create_thumbnail(background_path, quote, output_path="thumbnail.jpg"):
    # Размер обложки YouTube 1280x720
    width, height = 1280, 720

    # Загружаем фон
    bg = Image.open(background_path).convert("RGB")
    bg = bg.resize((width, height))

    draw = ImageDraw.Draw(bg)

    # Шрифт — Arial Bold, размер 50 (нужно чтобы шрифт был в системе или в папке)
    font_path = "arialbd.ttf"  # замените путь на доступный шрифт
    font_size = 48
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Обрамление текста и перенос по словам
    margin = 40
    max_width = width - 2 * margin
    lines = textwrap.wrap(quote, width=40)

    y_text = height // 3

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x_text = (width - w) // 2
        # Рисуем текст с тенью для читаемости
        shadowcolor = "black"
        for offset in [(1,1), (-1,-1), (1,-1), (-1,1)]:
            draw.text((x_text+offset[0], y_text+offset[1]), line, font=font, fill=shadowcolor)
        draw.text((x_text, y_text), line, font=font, fill="white")
        y_text += h + 10

    bg.save(output_path)
    return output_path
