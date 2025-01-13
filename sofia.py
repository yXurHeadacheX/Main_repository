import sqlite3

v = 2
i = 1

connection = sqlite3.connect('basa_sofia.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    Дата TEXT,
    Тип_корма TEXT,
    Сколько_съела INTEGER,
    Доп_инфо TEXT
)
""")
connection.commit()

def New_info(Data, Type, How_much, Addit_info):
    cursor.execute("INSERT INTO users VALUES(?,?,?,?)", (Data, Type, How_much, Addit_info))
    connection.commit()

ask = int(input('Запуск базы данных: basa_sofia.db\n'
            'Хотите записать новые данные в базу?\n'
            'Да - 1\n'
            'Нет - 2\n'))

if ask == 1:
    new_info = []
    a = input('Введите данные в таком формате:\n'
                     '1)Дата(пример: 13.04.24) 2)Тип корма; 3)Сколько съела; 4)Доп.инфо(если нет, то "-")\n'
                     'P.S. Записывать необходимо без пробелов после скобки(пример: 1)11.02.24\n')
    while v != 5:
        data = a.find(f'{i})')
        after_data = a.find(f'{v})')
        new_info.append(a[data+2:after_data])
        v += 1
        i += 1
    new_info.append(a[after_data+2:])
    New_info(new_info[0], new_info[1], new_info[2], new_info[3])

elif ask == 2:
    print('Хорошо, тогда до свидания!')

else:
    print('Команда не читается, повторите попытку ещё раз!')
