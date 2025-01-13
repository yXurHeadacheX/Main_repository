import telebot
from tabulate import tabulate
import sqlite3
import datetime

connection = sqlite3.connect('products_data_base.db', check_same_thread=False)
cursor = connection.cursor()

bot = telebot.TeleBot("8003301365:AAHHXHfGKeGSv62olYIq6x8Ro0hlgwDX-b8")

@bot.message_handler(commands=["output"])
def OutputInfo_db(message):
    sqlite_select_query = """SELECT * from products"""
    cursor.execute(sqlite_select_query)
    result = cursor.fetchall()
    bot.send_message(message.chat.id, "~~По какому параметру сделать сортировку?~~\n\
Tag\n\
Product\n\
Count\n\
--- ")
    bot.register_next_step_handler_by_chat_id(message.chat.id, Result)

def Result(message):
    query = cursor.execute(f"""SELECT * FROM products ORDER BY {str(message.text)}""")
    result_query = cursor.fetchall()
    Product = []
    for row in result_query:
        Product.append((row[2], row[3], row[4]))
    table_query = tabulate(Product, headers=["Tag", "Product", "Count"], tablefmt="pipe")
    bot.send_message(message.chat.id, table_query)

@bot.message_handler(commands=["record"])
def Insert_INFO(message):
    bot.send_message(message.chat.id, "~~Введите Тег, Продукт, Кол-во~~")
    bot.register_next_step_handler_by_chat_id(message.chat.id, Record)

def Record(message):
    split_message = str(message.text).split(', ')
    tag = split_message[0]
    product = split_message[1]
    count = split_message[2]
    data = datetime.datetime.now().date()
    sqlite_select_query = """SELECT * from products"""
    cursor.execute(sqlite_select_query)
    result = cursor.fetchall()
    for row in result[-1]:
        Id = row
        break
    cursor.execute("INSERT INTO products VALUES(?,?,?,?,?,?)", (Id+1, data, tag, product, count, None))
    connection.commit()
    bot.send_message(message.chat.id, "~~Ваши данные были записаны в базу данных~~")


def Start():
    bot.polling(none_stop=False, interval=0)