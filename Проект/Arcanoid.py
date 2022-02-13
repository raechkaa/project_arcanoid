from random import*
from tkinter import*
from time import*
class ball:
    def __init__(s,x,y,p,r,c):
        s.x=x
        s.y=y
        s.p=p
        s.r=r
        s.n=randint(1,2)
        s.c=c
        s.o=w.create_oval(x-r,y-r,x+r,y+r,fill=c,outline='#000000')
    def move(s):
        s.p=spb
        if s.n==1:
            s.x-=s.p
            s.y-=s.p
            return(-s.p,-s.p)
        elif s.n==2:
            s.x+=s.p
            s.y-=s.p
            return(s.p,-s.p)
        elif s.n==3:
            s.x+=s.p
            s.y+=s.p
            return(s.p,s.p)
        elif s.n==4:
            s.x-=s.p
            s.y+=s.p
            return(-s.p,s.p)
    def wall(s):
        if s.x-s.r<=0:
            if s.n==1:s.n=2
            if s.n==4:s.n=3
        elif s.x+s.r>=wid:
            if s.n==2:s.n=1
            if s.n==3:s.n=4
        if s.y-s.r<=0:
            if s.n==2:s.n=3
            if s.n==1:s.n=4
        elif s.y+s.r>=heg:
            if s.n==3:s.n=2
            if s.n==4:s.n=1
    def plat(s,pl):
        if s.y+s.r>pl.y-pl.he/2 and s.y-s.r<pl.y+pl.he/2:
            if s.x+s.r-(pl.x-pl.wi/2)>0 and s.x+s.r-(pl.x-pl.wi/2)<0.005*wid:
                if s.n==3:s.n=4
                if s.n==2:s.n=1
            elif pl.x+pl.wi/2-(s.x-s.r)>0 and pl.x+pl.wi/2-(s.x-s.r)<0.005*wid:
                if s.n==4:s.n=3
                if s.n==1:s.n=2
        if s.y+s.r-(pl.y-pl.he/2)>0 and s.y+s.r-(pl.y-pl.he/2)<0.005*wid:
            if s.x>pl.x-pl.wi/2 and s.x<pl.x+pl.wi/2:
                if s.n==3:s.n=2
                if s.n==4:s.n=1
    def inr(s,a,b,c):
        if a>=b and a<=c or a>=c and a<=b:return True
    def box(s,bx):
        if s.inr(s.x+s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
            if s.n==2:s.n=1
            if s.n==3:s.n=4
            '''
            odc=bx.c
            nwc='#'+('00'+hex(max(0,int(odc[1:3],16)-srt))[2:])[-2:]+('00'+hex(max(0,int(odc[3:5],16)-srt))[2:])[-2:]+('00'+hex(max(0,int(odc[5:],16)-srt))[2:])[-2:]
            bx.c=nwc
            if nwc!='#000000':
                w.delete(bx.o)
                bx.o=w.create_rectangle(bx.x-bxw/2,bx.y-bxh/2,bx.x+bxw/2,bx.y+bxh/2,fill=nwc,outline="#888888")
            else:
            '''
            w.delete(bx.o)
            bx.x=-9999
            bx.y=-9999
        if s.inr(s.x-s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
            if s.n==1:s.n=2
            if s.n==4:s.n=3
            '''
            odc=bx.c
            nwc='#'+('00'+hex(max(0,int(odc[1:3],16)-srt))[2:])[-2:]+('00'+hex(max(0,int(odc[3:5],16)-srt))[2:])[-2:]+('00'+hex(max(0,int(odc[5:],16)-srt))[2:])[-2:]
            bx.c=nwc
            if nwc!='#000000':
                w.delete(bx.o)
                bx.o=w.create_rectangle(bx.x-bxw/2,bx.y-bxh/2,bx.x+bxw/2,bx.y+bxh/2,fill=nwc,outline="#888888")
            else:
            '''
            w.delete(bx.o)
            bx.x=-9999
            bx.y=-9999
        if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y+s.r,bx.y-bxh/2,bx.y+bxh/2):
            if s.n==3:s.n=2
            if s.n==4:s.n=1
            '''
            odc=bx.c
            nwc='#'+('00'+hex(max(0,int(odc[1:3],16)-srt))[2:])[-2:]+('00'+hex(max(0,int(odc[3:5],16)-srt))[2:])[-2:]+('00'+hex(max(0,int(odc[5:],16)-srt))[2:])[-2:]
            bx.c=nwc
            if nwc!='#000000':
                w.delete(bx.o)
                bx.o=w.create_rectangle(bx.x-bxw/2,bx.y-bxh/2,bx.x+bxw/2,bx.y+bxh/2,fill=nwc,outline="#888888")
            else:
            '''
            w.delete(bx.o)
            bx.x=-9999
            bx.y=-9999
        if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y-s.r,bx.y-bxh/2,bx.y+bxh/2):
            if s.n==2:s.n=3
            if s.n==1:s.n=4
            '''
            odc=bx.c
            #nwc='#'+('00'+hex(max(0,int(odc[1:3],16)-srt))[2:])[-2:]+('00'+hex(max(0,int(odc[3:5],16)-srt))[2:])[-2:]+('00'+hex(max(0,int(odc[5:],16)-srt))[2:])[-2:]
            bx.c='#000000'
            if nwc!='#000000':
                w.delete(bx.o)
                bx.o=w.create_rectangle(bx.x-bxw/2,bx.y-bxh/2,bx.x+bxw/2,bx.y+bxh/2,fill=nwc,outline="#888888")
            else:
            '''
            w.delete(bx.o)
            bx.x=-9999
            bx.y=-9999
class box:
    def __init__(s,x,y,a):
        s.x=x
        s.y=y
        s.a=a
        s.c="#%s%s%s"%tuple(('00'+hex(randint(15,255))[2:])[-2:]for i in range(3))
        s.o=w.create_image(x,y,image=bxm[a])
class platform:
    def __init__(s,x,y,wi,he,p):
        s.x=x
        s.y=y
        s.wi=wi
        s.he=he
        s.p=p
        s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="#FF8888",outline="#000000")
    def move(s,x):
        s.p=spp
        if s.x>x:
            m=-min(s.x-x,s.p)
            s.x+=m
            return m
        elif s.x<x:
            m=min(x-s.x,s.p)
            s.x+=m
            return m
        else:
            return 0
class bonus:
    def __init__(s,x,y,wi,he,e):
        names=['end','<_>','+_+','+.+','-.-','-_-','>_<']
        s.x=x
        s.y=y
        s.he=he
        s.wi=wi
        s.e=e
        s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="#FFFFFF",outline="#FFFFFF")
        s.t=w.create_text(x,y,text=names[e],font='ComicSansMS 24')
    def inr(s,a,b,c):
        return(a>=b and a<=c)or(a>=c and a<=b)
    def plat(s,pl):
        global spb,spp
        if s.y+s.he/2>=pl.y-pl.he/2 and s.inr(s.x,pl.x-pl.wi/2,pl.x+pl.wi/2):
            w.delete(s.o)
            w.delete(s.t)
            s.o=0
            s.t=0
            global bonuses
            bonuses=[e for e in bonuses if e.o!=0]
            if s.e==1:
                pl.wi+=100
                w.delete(pl.o)
                pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#FF8888",outline="#000000")
            if s.e==-1:
                pl.wi-=100
                w.delete(pl.o)
                pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#FF8888",outline="#000000")
            if s.e==2:
                spp/=0.85
            if s.e==-2:
                spp*=0.85
            if s.e==3:
                spb/=0.85
            if s.e==-3:
                spb*=0.85
    def down(s,pl):
        w.move(s.o,0,heg/400)
        w.move(s.t,0,heg/400)
        s.y+=heg/400
        s.plat(pl)
        if s.y>heg:
            w.delete(s.o)
            w.delete(s.t)
            s.o=0
            s.t=0
            global bonuses
            bonuses=[e for e in bonuses if e.o!=0]
    def draw(s):
        ###
        pass
def motion(e):
    global tx,ty
    tx=e.x
tk=Tk()
wid=tk.winfo_screenwidth()
heg=tk.winfo_screenheight()

bxm=[PhotoImage(file='1box.gif',format = 'gif -index %d'%i)for i in range(24)]
for i in range(24):
    bxw=bxm[i].width()
    bxm[i]=bxm[i].zoom(round((wid/10)/10),round((wid/10)/10))
    bxm[i]=bxm[i].subsample(round(bxw/10),round(bxw/10))
bxw=bxm[-1].width()
bxh=bxm[-1].height()

tx=wid/2
ty=0
srt=500 #пробивная способность шариков
spb=0.0015*wid #скорость шарика
spp=0.002*wid #скорость платформы
tk.geometry('%dx%d+0+0'%(wid,heg))
w=Canvas(tk,width=wid,height=heg)
w.pack()
w.create_rectangle(0,0,wid,heg,fill='#000000',outline="#000000")
plat=platform(0.4*wid,0.95*heg,0.25*wid,0.15*heg,0.002*wid)
bal=ball(wid/2,heg/2,0.0015*wid,0.01*wid,'#880088')
boxes=[[box(bxw/2+j*bxw,bxh/2+bxh*i,randint(0,23))for j in range(10)]for i in range(4)]
bonuses=[]
w.bind_all("<Motion>",motion)
bonv=[i for i in range(-3,3+1)]
bonv.remove(0)
#tk.mainloop()
at=time()
while True:
    t=time()
    #tk.title(str(bal.n)+' '+str(bal.y))
    w.move(plat.o,plat.move(tx),0)
    w.move(bal.o,*bal.move())
    bal.wall()
    bal.plat(plat)
    
    if time()-at>=0.045:
        for i in range(4):
            for j in range(10):
                a=boxes[i][j].a+1
                a=a%24
                boxes[i][j].a=a
                w.itemconfig(boxes[i][j].o,image=bxm[a])
        at=time()
        
    for i in range(4):
        for j in range(10):
            bal.box(boxes[i][j])
    if randint(1,350)==1 and len(bonuses)<2:
        bonuses+=[bonus(randint(0,wid),0,wid*0.05,heg*0.07,bonv[randint(0,5)])]
    for b in bonuses:
        if b.o!=0:
            b.down(plat)
        else:
            print(len(bonuses))
    w.update()
    while time()-t<0.013:pass

