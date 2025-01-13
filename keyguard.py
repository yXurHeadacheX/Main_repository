import sqlite3
from datetime import datetime

connection = sqlite3.connect('keyguard.db', check_same_thread=False)
cursor = connection.cursor()

#(
#cursor.execute("""CREATE TABLE IF NOT EXISTS value(
#    Date TEXT,
#    Tag TEXT,
#    Value TEXT
#)
#""")
#connection.commit()
#                                                                           )

cursor.execute("SELECT * FROM value")
result = cursor.fetchall()

def Answer():
    ans = input('Какая функция необходима?\n'
                    '1 - Добавить новую "секретную" информацию.\n'
                    '2 - Найти конкретную "секретную" информацию.\n')
    if ans == '1': Insert_INTO_db()
    elif ans == '2': Select_INTO_db()
    else: print('Вы ввели что-то кроме 1 и 2, повторите попытку ещё раз!')


def Insert_INTO_db():
    ans_ins = input('Добавить новую "секретную" информацию?\n'
                        'n - нет\n'
                        'y - да\n')
    if ans_ins == 'n': print('Хорошо, как пожелаете :)')
    elif ans_ins == 'y':
        insert_info = input('Введите данные в следующем формате:\n'
                            'Date(формат: 25.07.2023), Tag(TEXT), Value(TEXT)\n').replace(',', ' ').split()
        get_data = lambda d: datetime.strptime(d, '%d.%m.%Y').date() <= datetime.today().date()

        try: assert get_data(insert_info[0]); cursor.execute("INSERT INTO value VALUES(?,?,?)", (insert_info[0], insert_info[1], insert_info[2])); connection.commit()
        except: print('Неверно введена дата!\n'
                  'Повторите попытку ещё раз!\n'
                  'P.S. это возможно по двум причинам: 1) неверно введенная дата, допустим вместо 20.05.2023, ввели 20.05.23\n'
                  '2) Вы возможно ввели будущее время, то есть дату, которая еще даже не наступила, к примеру 20.05.2077')
    else: print('Вы ввели что-то кроме n и y, повторите попытку ещё раз!')


def Select_INTO_db():

    def Input_Date():
        flag = False
        select_info = input('Введите дату(формат: 20.05.2023)...\n')
        get_data = lambda d: datetime.strptime(d, '%d.%m.%Y').date() <= datetime.today().date()
        try:
            assert get_data(select_info)
            for i in range(len(result)):
                for n in range(0, 3):
                    if result[i][n] == select_info: print(result[i]); flag = True
            if flag == True:
                pass
            else: print('Увы! Информация по такому запросу не была найдена в базе данных.\n'
                        'Попробуйте ввести другой запрос или проверьте предыдущий!\n')
        except: print('Неверно введена дата!\n'
                  'Повторите попытку ещё раз!\n'
                  'P.S. это возможно по двум причинам: 1) неверно введенная дата, допустим вместо 20.05.2023, ввели 20.05.23\n'
                  '2) Вы возможно ввели будущее время, то есть дату, которая еще даже не наступила, к примеру 20.05.2077')

    def Input_Tag():
        flag = False
        select_info = input('Введите тег...\n')
        ans_registr = input('Учитывать ли регистр при поиске в базе данных?\n'
                        'n - нет\n'
                        'y - да\n')
        if ans_registr == 'n':
            for i in range(len(result)):
                for n in range(0, 3):
                    if result[i][n].lower() == select_info.lower(): print(result[i]); flag = True
            if flag == True: pass
            else: print('Увы! Информация по такому запросу не была найдена в базе данных.\n'
                        'Попробуйте ввести другой запрос или проверьте предыдущий!\n')
        elif ans_registr == 'y':
            for i in range(len(result)):
                for n in range(0, 3):
                    if result[i][n] == select_info: print(result[i]); flag = True
            if flag == True: pass
            else: print('Увы! Информация по такому запросу не была найдена в базе данных.\n'
                        'Попробуйте ввести другой запрос или проверьте предыдущий!\n')
        else: print('Вы ввели что-то кроме n и y, повторите попытку ещё раз!')


    ans_sel = input('Найти конкретную "секретную" информацию?\n'
                        'n - нет\n'
                        'y - да\n')
    if ans_sel == 'n':
          print('Хорошо, как пожелаете :)')
    elif ans_sel == 'y':
        #(
        select = input('Введите данные в следующем формате:\n'
                            'Если необходимо найти по дате - Введите слово "Date"\n'
                            'Если необходимо найти по тегу - Введите слово "Tag"\n').lower()
        if select == 'date': Input_Date()
        elif select == 'tag': Input_Tag()
        else: print('Неверно указана область поиска!\n'
                    'Повторите попытку ещё раз!')
    else: print('Вы ввели что-то кроме n и y, повторите попытку ещё раз!')


if __name__ == "__main__":
    print('Запуск из main...')
    Answer()
