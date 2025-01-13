import requests
from PIL import Image, ImageDraw, ImageFont
import random


# Получаем случайный шаблон мемов
def get_random_meme_template():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url).json()
    memes = response['data']['memes']
    meme = random.choice(memes)
    return meme['url']


# Создаём мем
def create_meme(image_url, text):
    img = Image.open(requests.get(image_url, stream=True).raw)
    draw = ImageDraw.Draw(img)

    # Задаём параметры шрифта
    font = ImageFont.truetype("arial.ttf", 40)

    # Получаем размеры текста
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Смещаем текст выше от нижнего края
    padding = 50  # Отступ от нижнего края
    position = ((img.width - text_width) / 2, img.height - text_height - padding)

    # Рисуем текст на изображении
    draw.text(position, text, font=font, fill="white", stroke_fill="black", stroke_width=2)
    img.save("meme.png")
    print("Мем создан и сохранен как meme.png.")


meme_url = get_random_meme_template()
text = input("Введите текст для мема: ")
create_meme(meme_url, text)
