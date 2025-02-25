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
#______________________________________________________________________
# Токены и переменные
MISTRAL_API_TOKEN = os.getenv("mistral_api_token")
PASSWORD_HASH = str(os.getenv("hash_pass"))
MODEL = "mistral-large-latest"
bot = telebot.TeleBot(token=os.getenv("token_jarvis"))
flag = True

#ДОБАВИТЬ ВОЗМОЖНОСТЬ ИНИЦИАЛИЗАЦИИ ФОТО, Т.Е. РАСПОЗНАВАНИЕ ТЕКСТА ПО ФОТО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#_______________________________________________________________________
# Словари и списки
authorized_users = {}
hotkeys = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    "`", "[", "]", ";", "'", ",", ".", "/",
    "Space", "Ctrl", "Alt", "Shift", "Tab", "Win", "Enter", "Backspace", "Del", "Insert", "Escape",
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

def check_password(message): # Проверка пароля
    user_id = message.from_user.id
    entered_password = message.text.strip()
    hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
    if user_id in authorized_users and authorized_users[user_id]:
        print("Пользователь {} уже авторизован.".format(user_id))
        return True
    if hashed_password == PASSWORD_HASH:
        authorized_users[user_id] = True
        bot.reply_to(message, "Пароль верный. Доступ разрешен.")
        bot.delete_message(user_id, message.message_id)
        bot.send_message("5555053905", f"Пользователь {user_id} пытается функционировать с ботом.")
        return True
    else:
        bot.reply_to(message, "Пожалуйста, введите пароль.")
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

@bot.message_handler(content_types=['voice']) # Обработка голосовых сообщений
def handle_voice(message):
    if check_password(message):
        try:
            # Получаем информацию о голосовом сообщении
            file_info = bot.get_file(message.voice.file_id)
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"

            # Скачиваем файл
            response = requests.get(file_url)
            with open('voice_message.ogg', 'wb') as f:
                f.write(response.content)

            # Конвертируем .ogg в .wav
            audio = AudioSegment.from_ogg("voice_message.ogg")
            audio.export("voice_message.wav", format="wav")

            # Инициализируем распознаватель
            r = sr.Recognizer()

            # Список движков распознавания речи для использования
            engines = ['google', 'sphinx', 'google_cloud']

            recognized_text = None

            for engine in engines:
                try:
                    with sr.AudioFile("voice_message.wav") as source:
                        audio_data = r.record(source)
                        if engine == 'google':
                            recognized_text = r.recognize_google(audio_data, language="ru-RU")
                        elif engine == 'sphinx':
                            recognized_text = r.recognize_sphinx(audio_data, language="ru-RU")
                        elif engine == 'google_cloud':
                            client = speech.SpeechClient()
                            audio = speech.RecognitionAudio(content=audio_data.get_raw_data())
                            config = speech.RecognitionConfig(
                                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                sample_rate_hertz=16000,
                                language_code="ru-RU",
                            )
                            response = client.recognize(config=config, audio=audio)
                            recognized_text = response.results[0].alternatives[0].transcript
                        if recognized_text:
                            break
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    continue
            if recognized_text:
                bot.reply_to(message, f"Вы сказали: {recognized_text}")
                process_command(message, recognized_text)
            else:
                bot.reply_to(message, "Извините, я не смог распознать речь. Попробуйте еще раз.")
            # Удаляем временные файлы
            os.remove("voice_message.ogg")
            os.remove("voice_message.wav")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка при обработке голосового сообщения: {str(e)}")

def process_command(message, command): # Обработка комманд
    command = command.lower()
    user_id = message.from_user.id
    if "астрис" in command: # Команда для генерации текста Астриса
        context = command.split("астрис", 1)[1].strip()
        response = generate_response(user_id, context)
        bot.send_message(message.chat.id, response)
    elif "запусти" in command: # Команда для запуска приложения
        app_name = command.split("запусти")[-1].strip()
        if app_name in dict_directory:
            os.startfile(dict_directory[app_name])
            bot.reply_to(message, f"Запускаю {app_name}")
        else:
            # Попытка запустить приложение, которого нет в словаре
            print(f"Не найдено приложения в словаре с именем {app_name}")
    elif "курсор" in command or "cursor" in command: # Команда для перемещения курсора
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
                elif direction == "click":
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
    elif "список приложений" in command: # Команда для вывода списка приложений
        ListAppsForStart(message)
    elif "клавиша" in command: # Команда для нажатия клавиши
        key = command.split("клавиша")[-1].strip()
        try:
            keyboard.send(key)
            bot.reply_to(message, f"Нажимаю клавишу {key}")
        except:
            bot.reply_to(message, f"Не удалось нажать клавишу {key}")
    elif "напиши" in command: # Команда для ввода текста
        text = command.split("напиши")[-1].strip()
        try:
            keyboard.write(text)
            bot.reply_to(message, f"Ввожу текст: {text}")
        except:
            bot.reply_to(message, "Не удалось ввести текст")
    elif "скриншот" in command: # Команда для сохранения скриншота
        SendSctFull(message)
    elif "зажми" in command: # Команда для зажатия клавиши
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
            except:
                bot.reply_to(message, "Не удалось выполнить команду")
        else:
            bot.reply_to(message, "Неправильный формат команды. Используйте: зажми [клавиша1] нажми [клавиша2] [количество]")
    else:
        bot.reply_to(message, "Извините, я не понял команду. Повторите попытку.")

@bot.message_handler(func=lambda message: True) # Обработка текстовых сообщений
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
            else:
                if flag == True:
                    if response:  # Проверяем, что ответ не пустой
                        bot.send_message(message.chat.id, response)
                    else:
                        bot.send_message(message.chat.id, "Извините, я не смогла сгенерировать ответ.")
                else:
                    bot.send_message(message.chat.id, "Генератор отключен.")
#___________________________________________________________________________________________________
#Запускаем бота
if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as _ex:
            print(_ex)
            time.sleep(15)
