five = int(input('Сколько пятерок:'))
four = int(input('Сколько четверок:'))
three = int(input('Сколько троек:'))
two = int(input('Сколько двоек:'))

all_mark = five + four + three + two
middle_mark = (five * 5) + (four * 4) + (three * 3) + (two * 2)
need_five = 0
need_four = 0
need_three = 0

print('Средний балл:', round(middle_mark/all_mark, 2))

ask_need = int(input('Какая оценка вас интересует?\n1) 5\n2) 4\n3) 3\n'))
if ask_need == 1:
    while middle_mark/all_mark < 4.5:
        all_mark += 1
        middle_mark += 5
        need_five += 1
    print('До пятерки осталось заработать ещё', need_five, 'пятерок(-ку).')
if ask_need == 2:
    while middle_mark/all_mark < 3.5:
        all_mark += 1
        middle_mark += 5
        need_four += 1
    print('До четверки осталось заработать ещё', need_four, 'четверок(-ку).')
if ask_need == 3:
    while middle_mark / all_mark < 3.5:
        all_mark += 1
        middle_mark += 5
        need_three += 1
    print('До тройки осталось заработать ещё', need_three, 'троек(-йку).')