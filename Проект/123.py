from tkinter import*
from PIL import Image, ImageTk
tk=Tk()
p=PhotoImage(file='box1.gif')
w=p.width()
h=p.width()
p=p.zoom(x=18,y=18)
p=p.subsample(round(w/10),round(h/10))
a=Label(tk,image=p)
a.pack()
a.place(relx=0,rely=0,width=180,height=100)
