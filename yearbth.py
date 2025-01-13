import turtle as t
import math
import random
t.screensize(2000, 2000)
t.width(2)

def xt(t):
    return 15 * math.sin(t) ** 3

def yt(t):
    return 10 * math.cos(t) - 5 \
    * math.cos(2*t) - 2 * \
    math.cos(3*t) - math.cos(4*t)

def x_half_circle(t):
    return 20 * math.sin(t)

def y_half_circle(t):
    return 38 * math.cos(t)

def circle(t, x, y, r):
    t.up()
    t.setpos(x, y)
    t.color("black", "white")
    t.down()
    t.begin_fill()
    t.circle(r)
    t.end_fill()
    t.up()

def Stars(t):
    t.up()
    for i in range(2000):
        t.setpos(random.randint(-2000, 2000), random.randint(-2000, 2000))
        t.colormode(255)
        color = (255-50)%255, i%255, (5*i) // 2 % 25
        t.dot(4, color)
    t.down()


t.tracer(0)
Stars(t)
t.tracer(5)
t.width(1)
circle(t, 305, 203, 7)
circle(t, 305, 243, 7)
t.up()
t.setpos(352, 231)
t.dot(6, "white")
for i in range(4):
    t.setpos( x_half_circle(i) +330, y_half_circle(i) +228 )
    t.dot(6, "white")


t.speed(500)
t.colormode(255)
t.Screen().bgcolor(0,0,0)

t.width(2)
for n in range(3):
    for i in range(150):
        t.goto( (xt(i) * 20, yt(i)*20) )
        t.down()
    #    t.dot(3, 'white')
        t.pencolor((255-50)%255, i%255, (5*i) // 5 % 250)
        t.goto(0, 0)
    for i in range(100):
        t.goto( (xt(i) * 20, yt(i)*20) )
        t.down()
    #    t.dot(3, 'white')
        t.pencolor(10, i%5, 255-i)
        t.goto(0, 0)
    for i in range(50):
        t.goto( (xt(i) * 20, yt(i)*20) )
        t.down()
    #    t.dot(3, 'white')
        t.pencolor(i%255, (255-50)%255, (5*i) // 2 % 25)
        t.goto(0, 0)

for n in range(20):
    for i in range(100):
        t.goto( (xt(i) * 20, yt(i)*20) )
        t.down()
    #    t.dot(3, 'white')
        t.pencolor((255-50)%255, i%255, (5*i) // 2 % 25)
        t.goto(0, 0)
    for i in range(50):
        t.goto( (xt(i) * 20, yt(i)*20) )
        t.down()
    #    t.dot(3, 'white')
        t.pencolor(255, i%255, 25*2%i)
        t.goto(0, 0)
    for i in range(100):
        t.goto( (xt(i) * 20, yt(i)*20) )
        t.down()
    #    t.dot(3, 'white')
        t.pencolor(i%255, (255-50)%255, (5*i) // 2 % 25)
        t.goto(0, 0)

#for i in range(2000):
#        t.goto( (xt(i) * 20, yt(i)*20) )
#        t.down()
#    #    t.dot(3, 'white')
#        t.pencolor(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
#        t.goto(0, 0)

t.hideturtle()
t.update()
t.done()
