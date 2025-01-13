from random import *

f = open('C:/Users/stakh/Documents/Орфоэпия_словарь.txt', 'r', encoding='utf_8')
lst_f = f.read().splitlines()

q = open('C:/Users/stakh/Documents/Орфоэпия_проверка.txt', 'r', encoding='utf_8')
lst_q = q.read().splitlines()
proverka = ''
num_f = randint(0, 308)

def Print():
    global proverka
    if num_f < 9:
        print('Слово:', lst_f[num_f][3:])
    if num_f >= 9 and num_f < 99:
        print('Слово:', lst_f[num_f][4:])
    if num_f >= 99:
        print('Слово:', lst_f[num_f][5:])
    proverka = input('Поставьте ударение в этом слове (пример: тОрт)(стоп - остановить процесс).\n')


while proverka.lower() != 'стоп':
    Print()
    if proverka.lower() == 'стоп':
        print('Удачи!')
        break
    if num_f < 9:
        if lst_q[num_f][3:] == proverka: print('Правильно. Молодец!')
        else: print('Неверно! Правильно:', lst_q[num_f][3:])
    if num_f >= 9 and num_f < 99:
        if lst_q[num_f][4:] == proverka:  print('Правильно. Молодец!')
        else: print('Неверно! Правильно:', lst_q[num_f][4:])
    if num_f >= 99:
        if lst_q[num_f][5:] == proverka:  print('Правильно. Молодец!')
        else: print('Неверно! Правильно:', lst_q[num_f][5:])
    print('-----------------------------------------')
    num_f = randint(0, 308)
