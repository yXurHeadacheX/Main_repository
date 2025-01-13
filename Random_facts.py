import requests
from googletrans import Translator

translate = Translator()
# URL для получения случайных фактов
url = "https://uselessfacts.jsph.pl/random.json"

# Отправляем GET-запрос
response = requests.get(url)

# Проверяем, успешен ли запрос
if response.status_code == 200:
    fact = response.json().get("text")
    fact_ru = translate.translate(fact, dest="ru").text
    print(f"Случайный факт: {fact_ru}")
else:
    print(f"Произошла ошибка: {response.status_code}")
