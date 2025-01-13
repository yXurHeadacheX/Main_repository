import math

def Square_equation():
    print('//КВАДРАТНОЕ УРАВНЕНИЕ//')
    a = float(input('Введите значение первого коэффициента:'))
    b = float(input('Введите значение второго коэффициента:'))
    c = float(input('Введите значение третьего коэффициента:'))

    d = (b ** 2) - (4 * a * c)

    print('D=', d)
    if d > 0: print(   'Первый корень =', round((-b + math.sqrt(d)) / (2 * a), 2),
                     '\nВторой корень =', round((-b - math.sqrt(d)) / (2 * a), 2))
    elif d == 0: print('Уравнение имеет только один корень =', round(-b / 2 * a))
    else: print('Нет корней!')

if __name__ == "__main__":
    print('Запуск из main...')
    Square_equation()
