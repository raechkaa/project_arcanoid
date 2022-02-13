from tkinter import*
from time import*
from random import*
def motion(e):
    global x,y
    x=e.x
def move(n):
    if n==1:w.move(ball,-speed,-speed)
    if n==2:w.move(ball,speed,-speed)
    if n==3:w.move(ball,speed,speed)
    if n==4:w.move(ball,-speed,speed)
def wind():
    global n
    x=(w.coords(ball)[0]+w.coords(ball)[2])/2
    y=(w.coords(ball)[1]+w.coords(ball)[3])/2
    if x-r<=0:
        if n==1:n=2
        if n==4:n=3
    elif x+r>=width:
        if n==2:n=1
        if n==3:n=4
    if y-r<=0:
        if n==2:n=3
        if n==1:n=4
    elif y+r>=height:
        if n==3:n=2
        if n==4:n=1
def platest():
    global n
    x=(w.coords(ball)[0]+w.coords(ball)[2])/2
    y=(w.coords(ball)[1]+w.coords(ball)[3])/2
    px=(w.coords(platform)[0]+w.coords(platform)[2])/2
    py=(w.coords(platform)[1]+w.coords(platform)[3])/2
    if y+r>=py-plheight/2:
        if x+r>=px-plwidth/2 and x-r<=px+plwidth/2: 
            if x>px-plwidth/2.05 and x<px+plwidth/2.05:
                if n==3:n=2
                if n==4:n=1
            elif abs(x-(px-plwidth/2))<abs(x-(px+plwidth/2)):
                if n==3:n=4
                if n==2:n=1
            elif abs(x-(px-plwidth/2))>abs(x-(px+plwidth/2)):
                if n==4:n=3
                if n==1:n=2
def breaking():
    global n
    global blocks
    global ball
    for i in range(8):
        for j in range(5):
            x1=blocks[i][j][0]-blwidth/2
            x2=blocks[i][j][0]+blwidth/2
            y1=blocks[i][j][1]-blheight/2
            y2=blocks[i][j][1]+blheight/2
            x=(w.coords(ball)[0]+w.coords(ball)[2])/2
            y=(w.coords(ball)[1]+w.coords(ball)[3])/2
            v=[abs(x-r-x1),abs(x+r-x2),abs(y+r-y1),abs(y-r-y2)]
            if(y-r<=y2 and y-r>y1 and x1<=x and x<=x2)or(y+r<y2 and y+r>=y1 and x1<=x and x<=x2)or(x+r>=x1 and x+r<x2 and y1<=y and y<=y2)or(x-r<=x2 and x-r>x1 and y1<=y and y<=y2):
                if v[0]==min(v):
                    if n==2:n=1
                    if n==3:n=4
                    w.create_rectangle(blocks[i][j][0]-blwidth/2,blocks[i][j][1]-blheight/2,blocks[i][j][0]+blwidth/2,blocks[i][j][1]+blheight/2,fill='#FFFFFF',outline='#FFFFFF')
                    w.move(ball,-999999,-999999)
                    ball=w.create_oval(x-r,y-r,x+r,y+r,fill='#FF0088',outline='#FFFFFF')
                    blocks[i][j]=(-1000,-1000)
                    return None
                if v[1]==min(v):
                    if n==1:n=2
                    if n==4:n=3
                    w.create_rectangle(blocks[i][j][0]-blwidth/2,blocks[i][j][1]-blheight/2,blocks[i][j][0]+blwidth/2,blocks[i][j][1]+blheight/2,fill='#FFFFFF',outline='#FFFFFF')
                    w.move(ball,-999999,-999999)
                    ball=w.create_oval(x-r,y-r,x+r,y+r,fill='#FF0088',outline='#FFFFFF')
                    blocks[i][j]=(-1000,-1000)
                    return None
                if v[2]==min(v):
                    if n==4:n=1
                    if n==3:n=2
                    w.create_rectangle(blocks[i][j][0]-blwidth/2,blocks[i][j][1]-blheight/2,blocks[i][j][0]+blwidth/2,blocks[i][j][1]+blheight/2,fill='#FFFFFF',outline='#FFFFFF')
                    w.move(ball,-999999,-999999)
                    ball=w.create_oval(x-r,y-r,x+r,y+r,fill='#FF0088',outline='#FFFFFF')
                    blocks[i][j]=(-1000,-1000)
                    return None
                if v[3]==min(v):
                    if n==1:n=4
                    if n==2:n=3
                    w.create_rectangle(blocks[i][j][0]-blwidth/2,blocks[i][j][1]-blheight/2,blocks[i][j][0]+blwidth/2,blocks[i][j][1]+blheight/2,fill='#FFFFFF',outline='#FFFFFF')
                    w.move(ball,-999999,-999999)
                    ball=w.create_oval(x-r,y-r,x+r,y+r,fill='#FF0088',outline='#FFFFFF')
                    blocks[i][j]=(-1000,-1000)
                    return None
tk=Tk()
width=tk.winfo_screenwidth()
height=tk.winfo_screenheight()
tk.geometry('%dx%d+0+0'%(width,height))
w=Canvas(tk,width=tk.winfo_screenwidth(),height=tk.winfo_screenwidth())
w.pack()
w.create_rectangle(0,0,width,height,fill='#FFFFFF')
#platform stats
x=0.5*width
y=0.95*height
plwidth=0.15*width
plheight=0.15*height
reac=3
#ball stats
r=width/120
speed=3
if randint(1,2)==1:n=1
#blocks stats
blheight=height/10
blwidth=width/8
blocks=[[(width/16+i*blwidth,height/20+j*blheight)for j in range(5)]for i in range(8)]
for line in blocks:
    for block in line:
        w.create_rectangle(block[0]-blwidth/2,block[1]-blheight/2,block[0]+blwidth/2,block[1]+blheight/2,fill=('#%2x%2x%2x'%(randint(1,200),randint(1,200),randint(1,200))).replace(' ','0'),outline='#FFFFFF')
else:n=2
platform=w.create_rectangle(x-plwidth/2,y-plheight/2,x+plwidth/2,y+plheight/2,fill='#FF0088',outline='#FFFFFF')
ball=w.create_oval(width/2-r,0.8*height-r,width/2+r,0.8*height+r,fill='#FF0088',outline='#FFFFFF')
w.bind_all("<Motion>",motion)
while True:
    sleep(0.02)
    move(n)
    wind()
    platest()
    breaking()
    if x<(w.coords(platform)[0]+w.coords(platform)[2])/2:w.move(platform,-reac,0)
    if x>(w.coords(platform)[0]+w.coords(platform)[2])/2:w.move(platform,reac,0)
    w.update()
