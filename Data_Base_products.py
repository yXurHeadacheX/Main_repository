import sqlite3
import datetime
from tabulate import tabulate
import Data_Base_product_tg
connection = sqlite3.connect('products_data_base.db', check_same_thread=False)
cursor = connection.cursor()

# cursor.execute("""CREATE TABLE IF NOT EXISTS products(
#     ID INTEGER,
#     Date TEXT,
#     Tag TEXT,
#     Product TEXT,
#     Count INTEGER,
#     Weight INTEGER
# )
#                """)

# connection.commit()

class DataBase():
    def __init__(self, filename):
        self.filename = filename

    def Insert_INFO_db(self):
        with open(self.filename, "r", encoding="utf_8") as file:
            lines = [line.rstrip() for line in file]
        for i in range(len(lines)):
            tag = lines[i].split(', ')[0]
            product = lines[i].split(', ')[1]
            count = lines[i].split(', ')[2]
            data = datetime.datetime.now().date()
            sqlite_select_query = """SELECT * from products"""
            cursor.execute(sqlite_select_query)
            result = cursor.fetchall()
            for row in result[-1]:
                Id = row
                break
            cursor.execute("INSERT INTO products VALUES(?,?,?,?,?,?)", (Id+1, data, tag, product, count, None))
            connection.commit()
        DataBase.WriteFile(self)

    def WriteFile(self):
        open(self.filename, 'w').close()

    def Insert_TG_db(self):
        Data_Base_product_tg.Start()

    def Delete_db(self):
        sqlite_select_query = """SELECT * from products"""
        cursor.execute(sqlite_select_query)
        result = cursor.fetchall()
        table = tabulate(result, headers=["ID", "Data" ,"Tag", "Product", "Count", "Weight"], tablefmt='grid')
        print(table)
        asking = input("Какие ID необходимо удалить?\n\
--- ")
        sqlite_update_query = """DELETE from products where id = ?"""
        cursor.executemany(sqlite_update_query, asking)
        connection.commit()
        print("Удалено записей:", cursor.rowcount)
        connection.commit()

    def OutputInfo_db(self):
        sqlite_select_query = """SELECT * from products"""
        cursor.execute(sqlite_select_query)
        result = cursor.fetchall()
        table = tabulate(result, headers=["ID", "Data" ,"Tag", "Product", "Count", "Weight"], tablefmt='grid')
        print(table)
        asking = input("Нужно отсортировать данные?\n\
    y\n\
    n\n\
--- ")
        if asking == 'y':
            key_sorted = input("По какому параметру сделать сортировку?\n\
    ID\n\
    Data\n\
    Tag\n\
    Product\n\
    Count\n\
    Weight\n\
--- ")
            query = cursor.execute(f"""SELECT * FROM products ORDER BY {key_sorted}""")
            result_query = cursor.fetchall()
            table_query = tabulate(result_query, headers=["ID", "Data" ,"Tag", "Product", "Count", "Weight"], tablefmt='grid')
            print(table_query)
try:
    print("~~Подключение к SQLite~~")
    Start = DataBase("Список_продуктов.txt")
    asking = int(input("Какая функция нужна?\n\
    1) запись c помощью текста\n\
    2) запись с помощью тг бота\n\
    3) удалить запись(-и)\n\
    4) посмотреть записи в базе данных\n\
--- "))

    if asking == 1: Start.Insert_INFO_db()
    elif asking == 2: Start.Insert_TG_db()
    elif asking == 3: Start.Delete_db()
    elif asking == 4: Start.OutputInfo_db()
    else: print('~~Неправильный ввод команды~~')

except sqlite3.Error as error:
        print("~~Ошибка при работе с SQLite~~", error)
finally:
    if connection:
        connection.close()
        print("~~Соединение с SQLite закрыто~~")
