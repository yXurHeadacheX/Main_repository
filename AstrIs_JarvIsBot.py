# Импорт
import telebot
import os
import keyboard
import time
import speech_recognition as sr
from pydub import AudioSegment
import pyautogui
import requests
from google.cloud import speech
import hashlib
from transformers import LlamaTokenizer, LlamaForCausalLM
from torch.optim import Adam
from mistralai import Mistral
import mss
from tabulate import tabulate
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import psutil
import platform
from datetime import datetime
import subprocess
import winreg as reg
import ctypes, sys
from PIL import Image
import io
from transformers import AutoImageProcessor, ResNetForImageClassification
import torch
from urllib.request import urlopen
import pytesseract
#______________________________________________________________________
# Токены и переменные
MISTRAL_API_TOKEN = os.getenv("mistral_api_token")
PASSWORD_HASH = str(os.getenv("hash_pass"))
MODEL = "mistral-large-latest"
bot = telebot.TeleBot(token=os.getenv("token_jarvis"))

#ДОБАВИТЬ ВОЗМОЖНОСТЬ ИНИЦИАЛИЗАЦИИ ФОТО, Т.Е. РАСПОЗНАВАНИЕ ТЕКСТА ПО ФОТО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#_______________________________________________________________________
# Словари и списки
authorized_users = {}
hotkeys = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    "`", "[", "]", ";", "'", ",", ".", "/",
    "Space", "Ctrl", "Alt", "Shift", "Tab", "Win", "Enter", "Backspace", "Del", "Insert", "Escape",
    "Up", "Down", "Left", "Right",
    "Ctrl+Alt+Del", "Alt+Tab", "Alt+F4", "Alt+F10", "Alt+Shift+F9", "Ctrl+Up", "Ctrl+Down", "Ctrl+Left", "Ctrl+Right",
    "Ctrl+Home", "Ctrl+End", "Ctrl+Page Up", "Ctrl+Page Down", "Ctrl+Tab",
    "Ctrl+1", "Ctrl+2", "Ctrl+3", "Ctrl+4", "Ctrl+5", "Ctrl+6", "Ctrl+7", "Ctrl+8", "Ctrl+9",
    "Ctrl+T", "Ctrl+W"
]
hotkeys_translate = {
    "A": "Ф", "B": "И", "C": "С", "D": "В", "E": "У", "F": "А", "G": "П", "H": "Р", "I": "Ш", "J": "О", "K": "Л",
    "L": "Д", "M": "Ь", "N": "Т", "O": "Щ", "P": "З", "Q": "Й", "R": "К", "S": "Ы", "T": "Е", "U": "Г", "V": "М", "W": "Ц", "X": "Ч", "Y": "Н", "Z": "Я",
}
list_apps = [
    [1, "Cyberpunk2077"], [2, "Spotify"], [3, "Telegram"], [4, "Steam"],
    [5, "VsCode"], [6, "Яндекс"], [7, "Bash"], [8, "CS2"],
    [9, "Forza4"], [10, "Poppy3"], [11, "BattleBit"], [12, "Dishonored2"]
]
dict_directory = {
    "cyberpunk2077": r"D:\games\Cyberpunk 2077 v.2.2 (2020)\Cyberpunk 2077\bin\x64\Cyberpunk2077.exe",
    "spotify": r'C:\Users\stakh\AppData\Roaming\Spotify\Spotify.exe',
    "telegram": r"D:\Telegram Desktop\Telegram.exe",
    "steam": r"D:\Steam\steam.exe",
    "vscode": r"C:\Microsoft VS Code\Code.exe",
    "яндекс": r"C:\Users\stakh\AppData\Local\Yandex\YandexBrowser\Application\browser.exe",
    "bash": r"C:\Program Files\Git\git-bash.exe",
    "cs2": r"D:\Steam\steamapps\common\Counter-Strike Global Offensive\game\bin\win64\cs2.exe",
    "forza4": r"D:\games\Forza.Horizon.4.Ultimate.Edition.Steam.Rip-InsaneRamZes\ForzaHorizon4\ForzaHorizon4.exe",
    "poppy3": r"D:\realgames\Poppy Playtime Chapter 3\Playtime_Chapter3.exe",
    "battlebit": r"D:\Steam\steamapps\common\BattleBit Remastered\BattleBit.exe",
    "dishonored2": r"D:\realgames\Dishonored 2\Dishonored2.exe"
}
list_keyboard_func = [
    [1, "C(англ.) - уменьшить громкость"], [2, "B - прибавить громкость"],
    [3, "D - выключить звук"], [4, "K - приостанавлить проигрывание"],
    [5, "G - нажать на паузу или проигрывать"], [6, "Q - предыдущая запись"],
    [7, "P - следующая запись"]
]
#_____________________________________________________________________________________________
# Вспомогательные функции
def create_keyboard(): # Создание клавиатуры
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row(KeyboardButton('📱 Список приложений'), KeyboardButton('🖥 Скриншот'))
    keyboard.row(KeyboardButton('⌨️ Ввод текста'), KeyboardButton('🖱 Управление курсором'))
    keyboard.row(KeyboardButton('📊 Статистика системы'), KeyboardButton('📶 Bluetooth'))
    keyboard.row(KeyboardButton('📋 Запущенные процессы'))
    return keyboard
def generate_response(user_id, user_input): # Генерация ответа с использованием Mistral
    try:
        client = Mistral(api_key=MISTRAL_API_TOKEN)
        full_response = ""
        stream_response = client.chat.stream(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        )
        for chunk in stream_response:
            if chunk.data.choices[0].delta.content:
                full_response += chunk.data.choices[0].delta.content
        if not full_response:
            return "Извините, произошла ошибка при генерации ответа."
        return full_response
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Произошла ошибка при обработке запроса."

def check_password(message):
    """
    Проверка пароля и авторизации пользователя
    """
    user_id = message.from_user.id

    # Если пользователь уже авторизован
    if user_id in authorized_users and authorized_users[user_id]:
        print("Пользователь {} уже авторизован.".format(user_id))
        return True

    # Если это текстовое сообщение, проверяем пароль
    if hasattr(message, 'text') and message.text:
        entered_password = message.text.strip()
        hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
        if hashed_password == PASSWORD_HASH:
            authorized_users[user_id] = True
            bot.reply_to(message, "Пароль верный. Доступ разрешен.")
            bot.delete_message(user_id, message.message_id)
            bot.send_message("5555053905", f"Пользователь {user_id} пытается функционировать с ботом.")
            return True

    # Если пользователь не авторизован
    if user_id not in authorized_users or not authorized_users[user_id]:
        bot.reply_to(message, "Пожалуйста, введите пароль.")
        return False

    return False

#_____________________________________________________________________________________________
# Обработчики сообщений и команд
@bot.message_handler(commands=['start']) # Функция старта бота
def start_message(message):
    if check_password(message):
        bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=create_keyboard())

@bot.message_handler(commands=['apps']) # Функция отображения списка приложений
def ListAppsForStart(message):
    if check_password(message):
        keyboard = InlineKeyboardMarkup()
        for app in list_apps:
            keyboard.add(InlineKeyboardButton(app[1], callback_data=f"start_app_{app[1].lower()}"))
        bot.send_message(message.chat.id, "Выберите приложение:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('start_app_')) # функция запуска приложения
def callback_start_app(call):
    app_name = call.data.split('_')[2]
    if app_name in dict_directory:
        os.startfile(dict_directory[app_name])
        bot.answer_callback_query(call.id, f"Запускаю {app_name}")
    else:
        bot.answer_callback_query(call.id, "Нет в списке такого приложения!")

@bot.message_handler(commands=["keyboard"]) # Функция отображения списка клавиш для нажатия
def AnsKey_en(message):
    if check_password(message):
        keyboard = InlineKeyboardMarkup()
        for key in hotkeys:
            keyboard.add(InlineKeyboardButton(key, callback_data=f"hotkey_{key.lower()}"))
        bot.send_message(message.chat.id, "Выберите hotkey:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('hotkey_')) # функция обработки нажатия hotkey
def callback_hotkey_en(call):
    key = call.data.split('_')[1]
    try:
        keyboard.send(key)
        bot.answer_callback_query(call.id, f"Клавиша {key.upper()} нажата")
    except Exception as e:
        bot.answer_callback_query(call.id, f"Ошибка: {str(e)}")

@bot.message_handler(commands=["writetxt"])
def Itxt(message):
    if check_password(message):
        bot.send_message(message.chat.id, "Введите текст для ввода:")
        bot.register_next_step_handler(message, confirm_text_input)

def confirm_text_input(message):
    text = message.text
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Подтвердить", callback_data=f"confirm_text_{text}"),
        InlineKeyboardButton("Отменить", callback_data="cancel_text")
    )
    bot.send_message(message.chat.id, f"Вы хотите ввести текст: {text}", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_text_') or call.data == 'cancel_text')
def callback_text_input(call):
    if call.data == 'cancel_text':
        bot.answer_callback_query(call.id, "Ввод текста отменен")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        text = call.data.split('confirm_text_')[1]
        try:
            keyboard.write(text)
            bot.answer_callback_query(call.id, f"Текст введен: {text}")
            bot.edit_message_text(f"Текст успешно введен: {text}", call.message.chat.id, call.message.message_id)
        except Exception as e:
            bot.answer_callback_query(call.id, "Не удалось ввести текст")
            bot.edit_message_text(f"Ошибка при вводе текста: {str(e)}", call.message.chat.id, call.message.message_id)

@bot.message_handler(commands=["sendsctpart"])
def AnsSctPart(message):
    if check_password(message):
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("300x200", callback_data="sct_300x200"),
                     InlineKeyboardButton("500x300", callback_data="sct_500x300"))
        keyboard.row(InlineKeyboardButton("800x600", callback_data="sct_800x600"),
                     InlineKeyboardButton("1024x768", callback_data="sct_1024x768"))
        keyboard.row(InlineKeyboardButton("Ввести вручную", callback_data="sct_custom"))

        bot.send_message(message.chat.id, "Выберите размер скриншота или введите вручную:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('sct_'))
def callback_sct(call):
    if call.data == 'sct_custom':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Введите ширину и высоту скриншота через пробел (например, 400 300):")
        bot.register_next_step_handler(call.message, process_custom_size)
    else:
        width, height = map(int, call.data.split('_')[1].split('x'))
        send_screenshot(call.message, width, height)

def process_custom_size(message):
    try:
        width, height = map(int, message.text.split())
        send_screenshot(message, width, height)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, введите два числа, разделенные пробелом.")

def send_screenshot(message, width, height):
    try:
        with mss.mss() as sct:
            monitor = {"top": 200, "left": 300, "width": width, "height": height}
            output = f"sct-{monitor['top']}x{monitor['left']}_{monitor['width']}x{monitor['height']}.png"
            sct_img = sct.grab(monitor)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        with open(output, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove(output)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при создании скриншота: {e}")

@bot.message_handler(commands=["sendsctfull"])
def SendSctFull(message):
    if check_password(message):
        with mss.mss() as sct:
            screen = sct.shot(mon=-1, output='fullscreen.jpg')
            bot.send_photo(message.chat.id, open("fullscreen.jpg", "rb"))
            os.remove("fullscreen.jpg")

@bot.message_handler(commands=['offgenerate'])
def off_generate(message):
    if check_password(message):
        bot.send_message(message.chat.id, "Генератор отключен")
        global flag
        flag = False

@bot.message_handler(commands=['ongenerate'])
def on_generate(message):
    if check_password(message):
        bot.send_message(message.chat.id, "Генератор включен")
        global flag
        flag = True

@bot.message_handler(commands=['logout'])
def logout(message):
    if check_password(message):
        user_id = message.from_user.id
        if user_id in authorized_users:
            del authorized_users[user_id]
        bot.reply_to(message, "Вы вышли из системы. Для продолжения работы введите пароль.")

@bot.message_handler(commands=["manykeyboard"]) # Команда для многократного нажатия клавиш
def AnsKeyMany(message):
    if check_password(message):
        bot.send_message(message.chat.id, "Напишите название hotkey, а через пробел кол-во нажатий")
        bot.register_next_step_handler(message, SendKeysMany)

def SendKeysMany(message): # Отправка многократного нажатия клавиш
    try:
        for i in range(int(message.text.lower().split(' ')[1])):
            keyboard.send(message.text.lower().split(' ')[0])
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка в коде:\
            {e}")

@bot.message_handler(commands=["holdauto"]) # Команда для автоматического зажатия клавиши
def AnsHoldAuto(message):
    if check_password(message):
        bot.send_message(message.chat.id, "Напишите название hotkey для зажатия, а через пробел другую клавишу, а через еще один пробел кол-во нажатий второй клавиши")
        bot.register_next_step_handler(message, PressHoldAuto)

def PressHoldAuto(message): # Отправка автоматического зажатия клавиши
    try:
        keyboard.press(message.text.lower().split(' ')[0])
        for i in range(int(message.text.lower().split(' ')[2])):
            keyboard.send(message.text.lower().split(' ')[1])
        keyboard.release(message.text.lower().split(' ')[0])
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка в коде:\
            {e}")

@bot.message_handler(commands=["holdinput"]) # Команда для зажатия клавиши вручную
def AnsHold(message):
    if check_password(message):
        bot.send_message(message.chat.id, "Напишите название hotkey для зажатия, а через пробел вторую клавишу\n\
            В случае, если уже нужно отпустить кнопку, пишите сначала кнопку, которую нужно было зажать, а затем stop")
        bot.register_next_step_handler(message, PressHold)
def PressHold(message): # Отправка зажатия клавиши вручную
    try:
        keyboard.press(message.text.lower().split(" ")[0])
        if message.text.lower().split(' ')[1] != "stop":
            keyboard.send(message.text.lower().split(" ")[1])
            time.sleep(0.6)
            with mss.mss() as sct:
                screen = sct.shot(mon=-1, output='fullscreen.jpg')
                bot.send_photo(message.chat.id, open("fullscreen.jpg", "rb"))
                os.remove("fullscreen.jpg")
            bot.register_message_reaction_handler(message, AnsHold(message))
        else:
            keyboard.release(message.text.lower().split(" ")[0])
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка в коде:\
            {e}")

@bot.message_handler(commands=['cursor']) # Команда для изменения курсора
def handle_cursor_command(message):
    if check_password(message):
        bot.send_message(message.chat.id, "Введите команду в формате: cursor(курсор) [направление] [расстояние]")
        bot.register_next_step_handler(message, input_cursor_position)

def input_cursor_position(message): # Отправка позиции курсора
    command = message.text.lower.strip()
    parts = command.split()
    if len(parts) >= 3:
        direction = parts[1]
        try:
            distance = int(parts[2])
            if direction == "вверх":
                pyautogui.moveRel(0, -distance)
            elif direction == "вниз":
                pyautogui.moveRel(0, distance)
            elif direction == "влево":
                pyautogui.moveRel(-distance, 0)
            elif direction == "вправо":
                pyautogui.moveRel(distance, 0)
            elif direction == "click" or direction == "клик":
                pyautogui.click()
            elif direction == "двойной":
                pyautogui.doubleClick()
            else:
                bot.reply_to(message, "Неизвестное направление. Используйте: вверх, вниз, влево, вправо, клик или двойной.")
                return
            bot.reply_to(message, f"Курсор перемещен на {distance} пикселей {direction}")
        except ValueError:
            bot.reply_to(message, "Неверный формат команды. Используйте: курсор [направление] [расстояние]")
    else:
        bot.reply_to(message, "Неверный формат команды. Используйте: курсор [направление] [расстояние]")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    voice_ogg = "temp_voice.ogg"
    voice_wav = "temp_voice.wav"

    try:
        if user_id not in authorized_users or not authorized_users[user_id]:
            bot.reply_to(message, "Пожалуйста, сначала авторизуйтесь, отправив пароль.")
            return

        # Получаем информацию о голосовом сообщении
        file_info = bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"

        # Скачиваем голосовое сообщение
        response = requests.get(file_url)

        # Сохраняем во временный файл
        with open(voice_ogg, 'wb') as f:
            f.write(response.content)

        # Конвертируем в WAV
        audio = AudioSegment.from_ogg(voice_ogg)
        audio.export(voice_wav, format="wav")

        # Инициализируем распознаватель
        recognizer = sr.Recognizer()

        # Настраиваем параметры распознавания
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 4000

        recognized_text = None

        # Пробуем разные движки распознавания
        with sr.AudioFile(voice_wav) as source:
            audio_data = recognizer.record(source)

            # Пробуем Google Speech Recognition
            try:
                recognized_text = recognizer.recognize_google(audio_data, language="ru-RU")
                bot.reply_to(message, f"Распознано через Google: {recognized_text}")
            except sr.UnknownValueError:
                try:
                    # Пробуем Sphinx если Google не сработал
                    recognized_text = recognizer.recognize_sphinx(audio_data, language="ru-RU")
                    bot.reply_to(message, f"Распознано через Sphinx: {recognized_text}")
                except:
                    try:
                        # Пробуем Google Cloud если предыдущие не сработали
                        client = speech.SpeechClient()
                        audio = speech.RecognitionAudio(content=audio_data.get_raw_data())
                        config = speech.RecognitionConfig(
                            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                            sample_rate_hertz=16000,
                            language_code="ru-RU",
                        )
                        response = client.recognize(config=config, audio=audio)
                        if response.results:
                            recognized_text = response.results[0].alternatives[0].transcript
                            bot.reply_to(message, f"Распознано через Google Cloud: {recognized_text}")
                    except Exception as e:
                        bot.reply_to(message, f"Ошибка при распознавании через Google Cloud: {str(e)}")
            except sr.RequestError as e:
                bot.reply_to(message, f"Ошибка сервиса распознавания речи: {str(e)}")
            except Exception as e:
                bot.reply_to(message, f"Неизвестная ошибка: {str(e)}")

        # Если текст распознан, обрабатываем команду
        if recognized_text:
            process_command(message, recognized_text)
        else:
            bot.reply_to(message, "Извините, не удалось распознать речь. Пожалуйста, попробуйте еще раз.")

    except Exception as e:
        bot.reply_to(message, f"Ошибка при обработке голосового сообщения: {str(e)}")

    finally:
        # Удаляем временные файлы
        for temp_file in [voice_ogg, voice_wav]:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Ошибка при удалении временного файла {temp_file}: {str(e)}")

def process_command(message, command):
    if not command:
        bot.reply_to(message, "Не удалось распознать команду")
        return

    command = command.lower().strip()
    user_id = message.from_user.id

    # Если первое слово "астрис" - генерируем ответ
    if command.startswith("астрис"):
        context = command.split("астрис", 1)[1].strip()
        response = generate_response(user_id, context)
        bot.send_message(message.chat.id, response)
        return

    # Обработка команд
    if "запусти" in command:
        app_name = command.split("запусти")[-1].strip().lower()
        if app_name in dict_directory:
            os.startfile(dict_directory[app_name])
            bot.reply_to(message, f"Запускаю {app_name}")
        else:
            bot.reply_to(message, f"Приложение {app_name} не найдено в списке")

    elif "курсор" in command:
        parts = command.split()
        if len(parts) >= 3:
            direction = parts[1]
            try:
                distance = int(parts[2])
                if direction == "вверх":
                    pyautogui.moveRel(0, -distance)
                elif direction == "вниз":
                    pyautogui.moveRel(0, distance)
                elif direction == "влево":
                    pyautogui.moveRel(-distance, 0)
                elif direction == "вправо":
                    pyautogui.moveRel(distance, 0)
                elif direction in ["клик", "click"]:
                    pyautogui.click()
                elif direction == "двойной":
                    pyautogui.doubleClick()
                else:
                    bot.reply_to(message, "Неизвестное направление. Используйте: вверх, вниз, влево, вправо, клик или двойной.")
                    return
                bot.reply_to(message, f"Курсор перемещен на {distance} пикселей {direction}")
            except ValueError:
                bot.reply_to(message, "Неверный формат команды. Используйте: курсор [направление] [расстояние]")
        else:
            bot.reply_to(message, "Неверный формат команды. Используйте: курсор [направление] [расстояние]")

    elif "список приложений" in command:
        keyboard = InlineKeyboardMarkup()
        for app in list_apps:
            keyboard.add(InlineKeyboardButton(app[1], callback_data=f"start_app_{app[1].lower()}"))
        bot.send_message(message.chat.id, "Выберите приложение:", reply_markup=keyboard)

    elif "клавиша" in command:
        key = command.split("клавиша")[-1].strip()
        try:
            keyboard.send(key)
            bot.reply_to(message, f"Нажимаю клавишу {key}")
        except Exception as e:
            bot.reply_to(message, f"Не удалось нажать клавишу {key}: {str(e)}")

    elif "напиши" in command:
        text = command.split("напиши")[-1].strip()
        try:
            keyboard.write(text)
            bot.reply_to(message, f"Ввожу текст: {text}")
        except Exception as e:
            bot.reply_to(message, f"Не удалось ввести текст: {str(e)}")

    elif "скриншот" in command:
        try:
            with mss.mss() as sct:
                screen = sct.shot(mon=-1, output='fullscreen.jpg')
                bot.send_photo(message.chat.id, open("fullscreen.jpg", "rb"))
                os.remove("fullscreen.jpg")
        except Exception as e:
            bot.reply_to(message, f"Ошибка при создании скриншота: {str(e)}")

    elif "зажми" in command:
        parts = command.split()
        if len(parts) >= 4 and parts[2] == "нажми":
            key1 = parts[1]
            if key1 == "альт": key1 = "alt"
            key2 = parts[3]
            count = int(parts[4]) if len(parts) > 4 else 1
            try:
                keyboard.press(key1)
                for _ in range(count):
                    keyboard.send(key2)
                keyboard.release(key1)
                bot.reply_to(message, f"Зажимаю {key1}, нажимаю {key2} {count} раз(а)")
            except Exception as e:
                bot.reply_to(message, f"Не удалось выполнить команду: {str(e)}")
        else:
            bot.reply_to(message, "Неправильный формат команды. Используйте: зажми [клавиша1] нажми [клавиша2] [количество]")

    elif "статистика" in command:
        send_system_stats(message)

    elif "bluetooth" in command.lower():
        if "включи" in command.lower() or "включить" in command.lower():
            result = toggle_bluetooth(True)
            if result is True:
                bot.reply_to(message, "Bluetooth включен")
            else:
                bot.reply_to(message, f"Ошибка при включении Bluetooth: {result}")
        elif "выключи" in command.lower() or "выключить" in command.lower():
            result = toggle_bluetooth(False)
            if result is True:
                bot.reply_to(message, "Bluetooth выключен")
            else:
                bot.reply_to(message, f"Ошибка при выключении Bluetooth: {result}")
        else:
            status = get_bluetooth_status()
            if status is not None:
                bot.reply_to(message, f"Bluetooth {'включен' if status else 'выключен'}")
            else:
                bot.reply_to(message, "Не удалось получить статус Bluetooth")

    elif "процессы" in command or "приложения" in command:
        show_running_processes(message)

    elif "что на фото" in command.lower() and hasattr(message, 'reply_to_message') and message.reply_to_message.photo:
        # Получаем фото из пересланного сообщения
        file_info = bot.get_file(message.reply_to_message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        result = analyze_image(downloaded_file)
        bot.reply_to(message, result)

    elif "текст на фото" in command.lower() and hasattr(message, 'reply_to_message') and message.reply_to_message.photo:
        # Получаем фото из пересланного сообщения
        file_info = bot.get_file(message.reply_to_message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        result = extract_text_from_image(downloaded_file)
        bot.reply_to(message, result)

    else:
        bot.reply_to(message, "Извините, я не понял команду. Доступные команды:\n" +
                    "- запусти [приложение]\n" +
                    "- курсор [направление] [расстояние]\n" +
                    "- список приложений\n" +
                    "- клавиша [название]\n" +
                    "- напиши [текст]\n" +
                    "- скриншот\n" +
                    "- зажми [клавиша1] нажми [клавиша2] [количество]\n" +
                    "- статистика\n" +
                    "- bluetooth [включить|выключить|статус]\n" +
                    "- процессы\n" +
                    "- что на фото\n" +
                    "- текст на фото\n" +
                    "Или начните сообщение со слова 'Астрис' для общения")

@bot.message_handler(func=lambda message: message.content_type == 'text')  # Изменено условие
def handle_text(message):
    entered_password = message.text.strip()
    hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
    if check_password(message):
        user_id = message.from_user.id
        user_input = message.text.strip()
        if user_input and hashed_password != PASSWORD_HASH:
            response = generate_response(user_id, user_input)
            if user_input == '📱 Список приложений':
                ListAppsForStart(message)
            elif user_input == '🖥 Скриншот':
                SendSctFull(message)
            elif user_input == '🖱 Управление курсором':
                handle_cursor_command(message)
            elif user_input == '⌨️ Ввод текста':
                Itxt(message)
            elif user_input == '📊 Статистика системы':
                send_system_stats(message)
            elif user_input == '📶 Bluetooth':
                bluetooth_control(message)
            elif user_input == '📋 Запущенные процессы':
                show_running_processes(message)
            else:
                if flag == True:
                    if response:  # Проверяем, что ответ не пустой
                        bot.send_message(message.chat.id, response)
                    else:
                        bot.send_message(message.chat.id, "Извините, я не смогла сгенерировать ответ.")
                else:
                    bot.send_message(message.chat.id, "Генератор отключен.")

def get_size(bytes):
    """
    Преобразует байты в читаемый формат
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def get_system_stats():
    """
    Собирает статистику о системе
    """
    try:
        # Информация о системе
        uname = platform.uname()
        boot_time = datetime.fromtimestamp(psutil.boot_time())

        # CPU информация
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=1)

        # Память
        memory = psutil.virtual_memory()

        # Диски
        partitions = psutil.disk_partitions()
        disk_info = []
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'device': partition.device,
                    'total': get_size(partition_usage.total),
                    'used': get_size(partition_usage.used),
                    'free': get_size(partition_usage.free),
                    'percent': partition_usage.percent
                })
            except:
                continue

        # Сеть
        net_io = psutil.net_io_counters()

        stats = {
            "Загрузка CPU": f"{cpu_percent}%",
            "Память всего": get_size(memory.total),
            "Память использовано": f"{memory.percent}%",
            "Память свободно": get_size(memory.available),
            "Время работы": f"{datetime.now() - boot_time}",
            "Сеть отправлено": get_size(net_io.bytes_sent),
            "Сеть получено": get_size(net_io.bytes_recv),
            "Диски": disk_info
        }

        return stats
    except Exception as e:
        return f"Ошибка при получении статистики: {str(e)}"

@bot.message_handler(commands=['stats'])
def send_system_stats(message):
    if check_password(message):
        try:
            stats = get_system_stats()
            if isinstance(stats, dict):
                response = "📊 Статистика системы:\n\n"
                for key, value in stats.items():
                    if key != "Диски":
                        response += f"📌 {key}: {value}\n"

                response += "\n💾 Информация о дисках:\n"
                for disk in stats["Диски"]:
                    response += f"\nДиск {disk['device']}:\n"
                    response += f"Всего: {disk['total']}\n"
                    response += f"Использовано: {disk['used']} ({disk['percent']}%)\n"
                    response += f"Свободно: {disk['free']}\n"

                bot.reply_to(message, response)
            else:
                bot.reply_to(message, stats)
        except Exception as e:
            bot.reply_to(message, f"Ошибка при получении статистики: {str(e)}")

def toggle_bluetooth(turn_on=True):
    """
    Включает или выключает Bluetooth
    """
    try:
        # Команды для включения/выключения Bluetooth
        if turn_on:
            cmd = 'runas /user:Administrator "sc start bthserv"'
            powershell_cmd = 'Start-Process powershell -Verb RunAs -ArgumentList \'-Command "Enable-PnpDevice -InstanceId (Get-PnpDevice -Class Bluetooth).InstanceId -Confirm:$false"\''
        else:
            cmd = 'runas /user:Administrator "sc stop bthserv"'
            powershell_cmd = 'Start-Process powershell -Verb RunAs -ArgumentList \'-Command "Disable-PnpDevice -InstanceId (Get-PnpDevice -Class Bluetooth).InstanceId -Confirm:$false"\''

        # Выполняем команды через PowerShell с повышенными привилегиями
        subprocess.run(['powershell', '-Command', f'Start-Process cmd -Verb RunAs -ArgumentList \'/c {cmd}\''], shell=True)
        subprocess.run(['powershell', '-Command', powershell_cmd], shell=True)

        # Даем время на выполнение команд
        time.sleep(2)

        # Проверяем статус после выполнения команд
        status = get_bluetooth_status()
        if status is not None and status == turn_on:
            return True
        else:
            return "Не удалось изменить состояние Bluetooth"

    except Exception as e:
        return str(e)

def get_bluetooth_status():
    """
    Получает текущий статус Bluetooth
    """
    try:
        # Используем PowerShell для получения статуса с повышенными привилегиями
        cmd = 'Get-Service bthserv | Select-Object -ExpandProperty Status'
        result = subprocess.run(['powershell', '-Command', cmd],
                              capture_output=True,
                              text=True,
                              shell=True)

        # Проверяем статус службы
        return "Running" in result.stdout

    except Exception as e:
        print(f"Ошибка при получении статуса Bluetooth: {e}")
        return None

@bot.message_handler(commands=['bluetooth'])
def bluetooth_control(message):
    if check_password(message):
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("Включить", callback_data="bluetooth_on"),
            InlineKeyboardButton("Выключить", callback_data="bluetooth_off")
        )
        keyboard.row(
            InlineKeyboardButton("Статус", callback_data="bluetooth_status")
        )

        bot.reply_to(message, "Управление Bluetooth:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('bluetooth_'))
def callback_bluetooth(call):
    action = call.data.split('_')[1]
    if action == "status":
        status = get_bluetooth_status()
        if status is not None:
            status_text = "включен" if status else "выключен"
            bot.answer_callback_query(call.id, f"Bluetooth {status_text}")
        else:
            bot.answer_callback_query(call.id, "Не удалось получить статус Bluetooth. Убедитесь, что скрипт запущен с правами администратора.")
    elif action in ["on", "off"]:
        result = toggle_bluetooth(action == "on")
        if result is True:
            bot.answer_callback_query(call.id, f"Bluetooth успешно {'включен' if action == 'on' else 'выключен'}")
        else:
            bot.answer_callback_query(call.id, f"Ошибка: {result}. Убедитесь, что скрипт запущен с правами администратора.")

def get_running_processes():
    """
    Получает список запущенных приложений
    """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                # Получаем информацию о процессе
                proc_info = proc.info
                if proc_info['name'] != 'System Idle Process':  # Пропускаем системный процесс простоя
                    processes.append({
                        'name': proc_info['name'],
                        'pid': proc_info['pid'],
                        'memory': get_size(proc_info['memory_info'].rss),
                        'cpu': proc_info['cpu_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Сортируем по использованию CPU
        processes.sort(key=lambda x: x['cpu'], reverse=True)
        return processes[:15]  # Возвращаем топ-15 процессов
    except Exception as e:
        return f"Ошибка при получении списка процессов: {str(e)}"

@bot.message_handler(commands=['processes'])
def show_running_processes(message):
    if check_password(message):
        try:
            processes = get_running_processes()
            if isinstance(processes, list):
                response = "🖥 Запущенные приложения (топ-15 по загрузке CPU):\n\n"
                for proc in processes:
                    response += f"📌 {proc['name']}\n"
                    response += f"   PID: {proc['pid']}\n"
                    response += f"   Память: {proc['memory']}\n"
                    response += f"   CPU: {proc['cpu']}%\n\n"

                bot.reply_to(message, response)
            else:
                bot.reply_to(message, processes)
        except Exception as e:
            bot.reply_to(message, f"Ошибка при получении списка процессов: {str(e)}")

def analyze_image(image_data):
    """
    Анализирует изображение и возвращает описание того, что на нем изображено
    """
    try:
        # Загружаем модель и процессор
        processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
        model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")

        # Открываем изображение
        image = Image.open(io.BytesIO(image_data))

        # Предобработка изображения
        inputs = processor(image, return_tensors="pt")

        # Получаем предсказание
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = outputs.logits.softmax(dim=-1)

        # Получаем топ-5 предсказаний
        top_predictions = torch.topk(predictions[0], 5)

        response = "🖼 На изображении я вижу:\n\n"
        for score, idx in zip(top_predictions.values, top_predictions.indices):
            label = model.config.id2label[idx.item()]
            confidence = score.item() * 100
            response += f"📌 {label} (уверенность: {confidence:.2f}%)\n"

        return response

    except Exception as e:
        return f"Ошибка при анализе изображения: {str(e)}"

def extract_text_from_image(image_data):
    """
    Извлекает текст из изображения
    """
    try:
        # Открываем изображение
        image = Image.open(io.BytesIO(image_data))

        # Устанавливаем путь к исполняемому файлу tesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # Распознаем текст с поддержкой русского и английского языков
        text = pytesseract.image_to_string(image, lang='rus+eng')

        if text.strip():
            response = "📝 Распознанный текст:\n\n"
            response += text
            return response
        else:
            return "На изображении не удалось обнаружить текст."

    except Exception as e:
        return f"Ошибка при распознавании текста: {str(e)}"

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    if user_id in authorized_users and authorized_users[user_id]:
        try:
            # Получаем информацию о фото
            file_info = bot.get_file(message.photo[-1].file_id)

            # Скачиваем фото
            downloaded_file = bot.download_file(file_info.file_path)

            # Создаем клавиатуру для выбора действия
            keyboard = InlineKeyboardMarkup()
            keyboard.row(
                InlineKeyboardButton("Распознать объекты", callback_data=f"photo_objects_{message.message_id}"),
                InlineKeyboardButton("Распознать текст", callback_data=f"photo_text_{message.message_id}")
            )

            # Сохраняем фото во временный словарь для последующего использования
            if not hasattr(bot, 'temp_photos'):
                bot.temp_photos = {}
            bot.temp_photos[message.message_id] = downloaded_file

            # Отправляем сообщение с кнопками
            bot.reply_to(message, "Выберите действие:", reply_markup=keyboard)

        except Exception as e:
            bot.reply_to(message, f"Ошибка при обработке изображения: {str(e)}")
    else:
        bot.reply_to(message, "Пожалуйста, сначала авторизуйтесь, отправив пароль.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('photo_'))
def callback_photo(call):
    try:
        action, action_type, message_id = call.data.split('_')
        message_id = int(message_id)

        if not hasattr(bot, 'temp_photos') or message_id not in bot.temp_photos:
            bot.answer_callback_query(call.id, "Изображение больше недоступно. Отправьте фото заново.")
            return

        image_data = bot.temp_photos[message_id]

        if action_type == 'objects':
            result = analyze_image(image_data)
        else:  # action_type == 'text'
            result = extract_text_from_image(image_data)

        # Удаляем сообщение с кнопками
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=result
        )

        # Очищаем временное хранилище
        del bot.temp_photos[message_id]

    except Exception as e:
        bot.answer_callback_query(call.id, f"Ошибка при обработке: {str(e)}")

#___________________________________________________________________________________________________
#Запускаем бота
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as _ex:
            print(_ex)
            time.sleep(15)
