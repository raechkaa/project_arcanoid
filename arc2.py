from tkinter import *
from time import *
from random import *
from datetime import datetime, timedelta

def motion(e):
    global x, y
    
    x = e.x



def move(n):
    if n == 1: w.move(ball, -speed, -speed)
    if n == 2: w.move(ball, speed, -speed)
    if n == 3: w.move(ball, speed, speed)
    if n == 4: w.move(ball, -speed, speed)


def wind():
    global n
    if w.coords(ball)[0] <= 0:  # left side
        if n == 1:
            n = 2
        if n == 4:
            n = 3
    elif w.coords(ball)[2] >= width:  # right side
        if n == 2:
            n = 1
        if n == 3:
            n = 4
    if w.coords(ball)[1] <= 0:  # up side
        if n == 2:
            n = 3
        if n == 1:
            n = 4

def platest():
    global n
    ball_x_middle = (w.coords(ball)[0] + w.coords(ball)[2]) / 2.0
    if w.coords(ball)[3] >= w.coords(platform)[1] and w.coords(platform)[0] < ball_x_middle < \
            w.coords(platform)[2]:
        if n == 4:
            n = 1
        if n == 3:
            n = 2


def breaking():
    global n
    global ball
    x = (w.coords(ball)[0] + w.coords(ball)[2]) / 2
    y = (w.coords(ball)[1] + w.coords(ball)[3]) / 2
    for i in range(8):
        for j in range(5):
            x1 = blocks[i][j][0] - blwidth / 2
            x2 = blocks[i][j][0] + blwidth / 2
            y1 = blocks[i][j][1] - blheight / 2
            y2 = blocks[i][j][1] + blheight / 2
            if (x1 <= (w.coords(ball)[0] + w.coords(ball)[2]) / 2 <= x2) and (y1 <= (
                    w.coords(ball)[1] + w.coords(ball)[3]) / 2 <= y2):
                if 0 <= x - x1 <= r:
                    if n == 2: n = 1
                    if n == 3: n = 4
                    print("Sleva v pravo")
                elif 0 <= x - x2 <= r:
                    if n == 1: n = 2
                    if n == 4: n = 3
                    print("Sprava v levo")
                elif 0 <= y - y2 <= r:
                    if n == 1: n = 4
                    if n == 2: n = 3
                    print("Snizu v verh")
                elif 0 <= y1 - y <= r:
                    if n == 3: n = 2
                    if n == 4: n = 1
                    print("Sverhu v niz")
                w.create_rectangle(blocks[i][j][0] - blwidth / 2, blocks[i][j][1] - blheight / 2,
                                        blocks[i][j][0] + blwidth / 2, blocks[i][j][1] + blheight / 2,
                                        fill='#000000',
                                        outline='#000000')
                w.move(ball, -999999, -999999)
                ball = w.create_oval(x - r, y - r, x + r, y + r, fill='#FF0088', outline='#000000')
                blocks[i][j] = (-1000, -1000)
                return


tk = Tk()
width = tk.winfo_screenwidth() /2
height = tk.winfo_screenheight() /2
tk.geometry('%dx%d+0+0' % (width, height))
w = Canvas(tk, width=tk.winfo_screenwidth(), height=tk.winfo_screenwidth())
w.pack()
w.create_rectangle(0, 0, width, height, fill='#000000')
# platform stats
x = 0.5 * width
y = 0.95 * height
plwidth = 0.15 * width
plheight = 0.05 * height
reac = 12

# ball stats
r = width / 120
speed = 2
n = randint(1,2)
# blocks stats
blheight = height / 10
blwidth = width / 8
blocks = [[(width / 16 + i * blwidth, height / 20 + j * blheight) for j in range(5)] for i in range(8)]
for line in blocks:
    for block in line:
        w.create_rectangle(block[0] - blwidth / 2, block[1] - blheight / 2, block[0] + blwidth / 2,
                           block[1] + blheight / 2,
                           fill=('#%2x%2x%2x' % (randint(55, 255), randint(55, 255), randint(55, 255))).replace(' ', '0'),
                           outline='#000000')

platform = w.create_rectangle(x - plwidth / 2, y - plheight / 2, x + plwidth / 2, y + plheight / 2, fill='#FF0088',
                              outline='#000000')

ball = w.create_oval(width / 2 - r, 0.8 * height - r, width / 2 + r, 0.8 * height + r, fill='#FF0088',
                     outline='#000000')
w.bind_all("<Motion>", motion)

time_delay = timedelta(milliseconds=10)
now = datetime.now()
delay = datetime.now()

while w.coords(ball)[3] < w.coords(platform)[3]:
    move(n)
    wind()
    platest()
    breaking()
    if x < (w.coords(platform)[0] + w.coords(platform)[2]) / 2:
        w.move(platform, -reac, 0)
    if x > (w.coords(platform)[0] + w.coords(platform)[2]) / 2:
        w.move(platform, reac, 0)
    while delay - now < time_delay:
        delay = datetime.now()
    now = datetime.now()
    w.update()
