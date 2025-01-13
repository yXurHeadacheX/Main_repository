
from turtle import Turtle
from numpy import arange
import math

#-------------------------------------------

t = Turtle()
t.screen.screensize(2000, 2000)
m = 20
FONT_coord = ("Montserrat", 8, "bold")
FONT_function = ("Montserrat", 12, "bold")
t.screen.tracer(0)

#-------------------------------------------

def Rendering():
    t.color('gray')
    t.width(1)
    y = 2000
    while y != -2200:
        t.up()
        t.setpos(-2000, y)
        t.down()
        t.forward(2000*m)
        y -= m
    t.up()
    t.right(90)
    t.setpos(-2000, 2000)
    x = -2000
    while x != 2000:
        t.up()
        t.setpos(x, 2000)
        t.down()
        t.forward(2000*m)
        x += m
    t.left(90)


def system_coordinates(x, y, m):
    t.color('black')
    t.width(2)
    t.up()
    t.setpos(0, 0)
    t.down()
    t.forward(x*m)
    t.left(180)
    t.forward(2*x*m)
    for x in arange(-x, x+0.5, .5):
        t.setpos(x=x*m, y=0)
        t.dot(6, 'red')
        t.up()
        t.setpos(x=x*m, y=-15)
        t.write(x, align='center', font=FONT_coord)
    t.up()
    t.setpos(0, 0)
    t.down()
    t.left(90)
    t.forward(y*m)
    t.left(180)
    t.forward(2*y*m)
    for y in arange(-y, y+0.5, .5):
        t.setpos(x=0, y=y*m)
        t.dot(6, 'red')
        t.write(y, align='center', font=FONT_coord)


def Theme_Screen(color="white", color_turtle="black"): t.screen.bgcolor(color); t.color(color_turtle)


def Linear_function(x, y, m, k, b):
    cnt = 0
    t.color('black')
    for i in arange(-x, x, .25):
        for v in arange(-y, y, .25):
            if (i*k)+b==v:
                if cnt == 0: t.up();   t.setpos(i*m, v*m); t.dot(6, 'purple'); cnt += 1
                else:        t.down(); t.setpos(i*m, v*m); t.dot(6, 'purple')
    t.color('red')
    if b > 0 and (k > 0 or k < 0): t.write(f'y = {k}x + {b}', align='center', font=FONT_function)
    if b < 0 and (k > 0 or k < 0): t.write(f'y = {k}x - {abs(b)}', align='center', font=FONT_function)
    if b == 0:                     t.write(f'y = {k}x', align='center', font=FONT_function)
    if k == 0 and b > 0:           t.write(f'y = {b}', align='center', font=FONT_function)
    if k == 0 and b < 0:           t.write(f'y = - {abs(b)}', align='center', font=FONT_function)



def Parabola_function(x, y, m, a, b, c):
    cnt = 0
    t.color('black')
    for i in arange(-x, x, .25):
        for v in arange(-y, y, .25):
            if (i*i*a)+(b*i)+c==v:
                if cnt == 0: t.up();   t.setpos(i*m, v*m); t.dot(6, 'purple'); cnt += 1
                else:        t.down(); t.setpos(i*m, v*m); t.dot(6, 'purple')
    t.color('red')
    if b > 0 and c > 0:   t.write(f'y = {a}x² + {b}x + {c}', align='center', font=FONT_function)
    if b < 0 and c > 0:   t.write(f'y = {a}x² - {abs(b)}x + {c}', align='center', font=FONT_function)
    if b > 0 and c < 0:   t.write(f'y = {a}x² + {b}x - {abs(c)}', align='center', font=FONT_function)
    if b < 0 and c < 0:   t.write(f'y = {a}x² - {abs(b)}x - {abs(c)}', align='center', font=FONT_function)
    if b == 0 and c > 0:  t.write(f'y = {a}x² + {c}', align='center', font=FONT_function)
    if b == 0 and c < 0:  t.write(f'y = {a}x² - {abs(c)}', align='center', font=FONT_function)
    if c == 0 and b > 0:  t.write(f'y = {a}x² + {b}x', align='center', font=FONT_function)
    if c == 0 and b < 0:  t.write(f'y = {a}x² - {abs(b)}x', align='center', font=FONT_function)
    if c == 0 and b == 0: t.write(f'y = {a}x²', align='center', font=FONT_function)

#-------------------------------------------

if __name__ == '__main__':
    #Theme_Screen("black", "white")
    Rendering()
    system_coordinates(10, 10, 60)
    Linear_function(10, 10, 60, 2, 0)
    Parabola_function(10, 10, 60, 4, 0, 2)
    t.hideturtle()
    #Proiz(12, 12, 60)


t.screen.mainloop()

#-------------------------------------------

#Разобраться с масштабом
#Создать определяющий алгоритм функцию
#def Function(x, y, a, b, c, k):
#--> y = 4x^2 + 7x + 4
#x = ans.replace('x^2', 'i')
#x =
#Function()

#-------------------------------------------
