from random import*
from tkinter import*
from time import*
from winsound import* #импортируем музыку
from threaded import* #импортируем поток
import webbrowser

boxes=[]
bonuses=[]
srt,spp,spb,tx,ty,plat,bal,r,m=0,0,0,0,0,0,0,0,0

tk=Tk()
wid=tk.winfo_screenwidth()
heg=tk.winfo_screenheight()

bxm=[[PhotoImage(file='box%d.gif'%(j+1),format = 'gif -index %d'%i)for i in range([35,37,49,1][j])]for j in range(0,4)]#двумерный список смены кадров
                                                                            #количество кадров в гифках
#ратягивание и сужение разных гифок
for i in range(35):
    bxw=bxm[0][i].width()
    bxm[0][i]=bxm[0][i].zoom(int((wid/10)/5),int((wid/10)/5))
    bxm[0][i]=bxm[0][i].subsample(int(bxw/5),int(bxw/5))
for i in range(37):
    bxw=bxm[1][i].width()
    bxm[1][i]=bxm[1][i].zoom(int((wid/10)/5),int((wid/10)/5))
    bxm[1][i]=bxm[1][i].subsample(int(bxw/5),int(bxw/5))
for i in range(49):
    bxw=bxm[2][i].width()
    bxm[2][i]=bxm[2][i].zoom(int((wid/10)/5),int((wid/10)/5))
    bxm[2][i]=bxm[2][i].subsample(int(bxw/5),int(bxw/5))
for i in range(1):
    bxw=bxm[3][i].width()
    bxm[3][i]=bxm[3][i].zoom(int((wid/10)/5),int((wid/10)/5))
    bxm[3][i]=bxm[3][i].subsample(int(bxw/5),int(bxw/5))
#актуальная ширина и высота гифки
bxw=bxm[3][-1].width()
bxh=bxm[3][-1].height()
#tk.destroy()
def classic():
    global boxes,bonuses,srt,spp,spb,tx,ty,plat,bxw,bxh,bxm,tk,wid,heg,bal
    class ball:
        def __init__(s,x,y,p,r,c):
            s.x=x
            s.y=y
            s.p=p #скорость шарика
            s.r=r #радиус
            s.n=randint(1,2)#направление движения шарика
            s.o=w.create_image(x,y,image=blm)#рисуем объект
            s.t=w.create_text(x,y,text=str(srt),font='ComicSansMS 12 bold',fill='#000000')
        def move(s):
            s.p=spb #spb глобальная переменная
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
            global srt,plat
            if s.x-s.r<=0:
                if s.n==1:s.n=2
                if s.n==4:s.n=3
            elif s.x+s.r>=wid: #ширина экрана
                if s.n==2:s.n=1
                if s.n==3:s.n=4
            if s.y-s.r<=0:
                if s.n==2:s.n=3
                if s.n==1:s.n=4
            elif s.y+s.r>=heg: #высота экрана
                if s.n==3:s.n=2
                if s.n==4:s.n=1
                srt-=1
                if srt==0:
                    gameover()
                w.itemconfig(s.t,text=str(srt))
                w.move(s.o,plat.x-s.x,plat.y-plat.he-s.y)
                w.move(s.t,plat.x-s.x,plat.y-plat.he-s.y)
                s.x=plat.x
                s.y=plat.y-plat.he
        def plat(s,pl):
            global boxes
            if s.y+s.r>pl.y-pl.he/2: #and s.y-s.r<pl.y+pl.he/2:
                if s.x+s.r-(pl.x-pl.wi/2)>0 and s.x+s.r-(pl.x-pl.wi/2)<0.005*wid: #проверка, что бы шарик по абсциссе был внутри платформы
                    if s.n==3:s.n=4
                    if s.n==2:s.n=1
                elif pl.x+pl.wi/2-(s.x-s.r)>0 and pl.x+pl.wi/2-(s.x-s.r)<0.005*wid:
                    if s.n==4:s.n=3
                    if s.n==1:s.n=2
            if s.y+s.r-(pl.y-pl.he/2)>0 and s.y+s.r-(pl.y-pl.he/2)<0.005*wid:#отталкивание от бока платформы
                if s.x>pl.x-pl.wi/2 and s.x<pl.x+pl.wi/2:
                    if s.n==3:s.n=2
                    if s.n==4:s.n=1
            if [sum([e.x for e in el])for el in boxes]==[-99990]*4:
                gamewin()
        def inr(s,a,b,c):
            if a>=b and a<=c or a>=c and a<=b:
                return True
        def box(s,bx,i,j): #шарик внутри коробки
            global srt,bonuses,boxes
            if s.inr(s.x+s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==2:#левый бок коробки
                    s.n=1
                if s.n==3:#левый бок с другой стороны
                    s.n=4
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                        
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x-s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==1:#правый бок
                    s.n=2
                if s.n==4:
                    s.n=3
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                        
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y+s.r,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==3:#верх
                    s.n=2
                if s.n==4:
                    s.n=1
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y-s.r,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==2: #низ
                    s.n=3
                if s.n==1:
                    s.n=4
                    
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))
                    
                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999

                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
                    
    class box:
        def __init__(s,x,y,a,t): #создание коробки
            s.x=x
            s.y=y
            s.a=a #текущая анимация
            s.t=t #тип коробки
            s.o=w.create_image(x,y,image=bxm[t][a]) #создание картинки для коробки
    class platform:
        def __init__(s,x,y,wi,he,p):
            s.x=x
            s.y=y
            s.wi=wi
            s.he=he
            s.p=p #скорость платформы
            s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="#000000",outline="#FFEE00", width = 3)
        def move(s,x):
            s.p=spp
            if s.x>x: #х положение мышки s.x положение платформы
                m=-min(s.x-x,s.p)
                s.x+=m #перемещение платформы
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
            s.e=e #эффекты от бонуса
            s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="",outline="#FFFFFF",width=3)
            s.t=w.create_text(x,y,text=names[e],font='ComicSansMS 24 bold',fill='#FFFFFF')
        def inr(s,a,b,c): #вспомогательная функция
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
                if s.e==1: #увеличение платформы на 100
                    pl.wi+=100
                    w.delete(pl.o)
                    pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#000000",outline="#FFEE00",width=3)
                if s.e==-1:#уменьшение платформы на 100
                    pl.wi-=100
                    w.delete(pl.o)
                    pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#000000",outline="#FFEE00",width=3)
                if s.e==2:#ускорение платформы на 33%
                    spp/=0.75
                if s.e==-2: #замедление на 25%
                    spp*=0.75
                if s.e==3: # ускорение и замедление шарика 
                    spb/=0.75
                if s.e==-3:
                    spb*=0.75
        def down(s,pl): #бонус падает
            w.move(s.o,0,heg/400) #объект бонуса
            w.move(s.t,0,heg/400) #рисунок бонуса
            s.y+=heg/400
            s.plat(pl) #бонус упал на платформу
            if s.y>heg: 
                w.delete(s.o)
                w.delete(s.t)
                s.o=0
                s.t=0
                global bonuses
                bonuses=[e for e in bonuses if e.o!=0] #генератор с фильтром

    def gameover():
        w.create_text(wid/2-10,heg/2-10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2-10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2-10,heg/2+10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2+10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2,heg/2,text='GAME OVER',font='ComicSansMS 72',fill='#000000')
        w.delete(bal.o)
        w.delete(bal.t)
        w.update()
        sleep(5)
        PlaySound(None,SND_FILENAME)
        start()
        #tk.destroy()

    def gamewin():
        w.create_text(wid/2-10,heg/2-10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2-10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2-10,heg/2+10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2+10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2,heg/2,text='YOU WON',font='ComicSansMS 72',fill='#000000')
        w.delete(bal.o)
        w.delete(bal.t)
        w.update()
        sleep(5)
        PlaySound(None,SND_FILENAME)
        start()
        #tk.destroy()

    def motion(e):
        global tx,ty #положение мышки
        tx=e.x
    #tk=Tk() #создаем окошко
    #wid=tk.winfo_screenwidth()
    #heg=tk.winfo_screenheight()

    blm=PhotoImage(file='ball.gif',format = 'gif -index 0')
    blw=blm.width()
    blm=blm.zoom(int(wid*0.015),int(wid*0.015))
    blm=blm.subsample(int(bxw),int(bxw))
    #актуальная ширина и высота the ball of the gym
    blw=blm.width()
    blh=blm.height()

    tx=wid/2
    ty=0
    srt=3 #количество жизней
    spb=0.0015*wid #скорость шарика
    spp=0.002*wid #скорость платформы
    tk.geometry('%dx%d+0+0'%(wid,heg))#положение и размер формы
    w=Canvas(tk,width=wid,height=heg) #окошко для рисования
    w.pack()
    w.create_rectangle(0,0,wid,heg,fill='#000000',outline="#000000")
    plat=platform(0.4*wid,0.95*heg,0.25*wid,0.15*heg,0.002*wid) #ФОРМИРОВАНИЕ ПЛАТФОРМЫ
    bal=ball(wid/2,heg/2,blw/2,0.008*wid,'#880088')
    boxes=[[(lambda rr:(box(bxw/2+j*bxw,bxh/2+bxh*i,randint(0,[34,36,48,0][rr]),rr)))(randint(0,3))for j in range(10)]for i in range(4)]
                                        #каждая гифка с разного кадра начинается
    bonuses=[]
    w.bind_all("<Motion>",motion)#привязываем мышку, каждый раз проверяем положение мышки
    bonv=[i for i in range(-3,3+1)] #для эффектов бонусов, чтобы можно было брать случайные бонусы
    bonv.remove(0)
    at=time() #начальное время

    @Threaded #новый поток для музыки
    def music():
        PlaySound("fone.wav",SND_FILENAME|SND_LOOP|SND_ASYNC)
    thread = music()
    thread.start()

    while True:
        t=time() #текущее время

        #tk.title(str(bal.n)+' '+str(bal.y))
        w.move(plat.o,plat.move(tx),0)
        (lambda rr:(w.move(bal.o,*rr),w.move(bal.t,*rr)))(bal.move())
        bal.wall() #проверка врезания в стену
        bal.plat(plat) #врезался в платформу
        if time()-at>=0.05: #если прошло больше 50мс, запускаем следующий кадр
            for i in range(4):
                for j in range(10):
                    if boxes[i][j].t!=3:
                        a=boxes[i][j].a+1
                        if boxes[i][j].t==0:
                            a=a%35
                        if boxes[i][j].t==1:
                            a=a%37
                        if boxes[i][j].t==2:
                            a=a%49
                        boxes[i][j].a=a
                        w.itemconfig(boxes[i][j].o,image=bxm[boxes[i][j].t][a])#меняем картинки всех коробочек
            at=time()#перезаписываем время
            
        for i in range(4): #проверка шарика на врезание в коробочки
            for j in range(10):
                bal.box(boxes[i][j],i,j) 
        if randint(1,350)==1 and len(bonuses)<4: #если равно 1, то падает бонус их может быть только <=4 свободных бонусов
            bonuses+=[bonus(randint(0,wid),0,wid*0.05,heg*0.07,bonv[randint(0,5)])]
        for b in bonuses: #передвижение бонусов
            if b.o!=0:
                b.down(plat)
        w.update() #перерисовка, обновление окошка
        while time()-t<0.013: #каждое следующее действие происходит через 13 мс
            pass

def easywin():
    global boxes,bonuses,srt,spp,spb,tx,ty,plat,bxw,bxh,bxm,tk,wid,heg,bal
    class ball:
        def __init__(s,x,y,p,r,c):
            s.x=x
            s.y=y
            s.p=p #скорость шарика
            s.r=r #радиус
            s.n=randint(1,2)#направление движения шарика
            s.o=w.create_image(x,y,image=blm)#рисуем объект
            s.t=w.create_text(x,y,text=str(srt),font='ComicSansMS 12 bold',fill='#000000')
        def move(s):
            s.p=spb #spb глобальная переменная
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
            global srt,plat
            if s.x-s.r<=0:
                if s.n==1:s.n=2
                if s.n==4:s.n=3
            elif s.x+s.r>=wid: #ширина экрана
                if s.n==2:s.n=1
                if s.n==3:s.n=4
            if s.y-s.r<=0:
                if s.n==2:s.n=3
                if s.n==1:s.n=4
            elif s.y+s.r>=heg: #высота экрана
                if s.n==3:s.n=2
                if s.n==4:s.n=1
                srt-=1
                if srt==0:
                    gameover()
                w.itemconfig(s.t,text=str(srt))
                w.move(s.o,plat.x-s.x,plat.y-plat.he-s.y)
                w.move(s.t,plat.x-s.x,plat.y-plat.he-s.y)
                s.x=plat.x
                s.y=plat.y-plat.he
        def plat(s,pl):
            global boxes
            if s.y+s.r>pl.y-pl.he/2: #and s.y-s.r<pl.y+pl.he/2:
                if s.x+s.r-(pl.x-pl.wi/2)>0 and s.x+s.r-(pl.x-pl.wi/2)<0.005*wid: #проверка, что бы шарик по абсциссе был внутри платформы
                    if s.n==3:s.n=4
                    if s.n==2:s.n=1
                elif pl.x+pl.wi/2-(s.x-s.r)>0 and pl.x+pl.wi/2-(s.x-s.r)<0.005*wid:
                    if s.n==4:s.n=3
                    if s.n==1:s.n=2
            if s.y+s.r-(pl.y-pl.he/2)>0 and s.y+s.r-(pl.y-pl.he/2)<0.005*wid:#отталкивание от бока платформы
                if s.x>pl.x-pl.wi/2 and s.x<pl.x+pl.wi/2:
                    if s.n==3:s.n=2
                    if s.n==4:s.n=1
            if [sum([e.x for e in el])for el in boxes]==[-99990]*4:
                gamewin()
        def inr(s,a,b,c):
            if a>=b and a<=c or a>=c and a<=b:
                return True
        def box(s,bx,i,j): #шарик внутри коробки
            global srt,bonuses,boxes
            if s.inr(s.x+s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==2:#левый бок коробки
                    s.n=1
                if s.n==3:#левый бок с другой стороны
                    s.n=4
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                        
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x-s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==1:#правый бок
                    s.n=2
                if s.n==4:
                    s.n=3
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                        
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y+s.r,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==3:#верх
                    s.n=2
                if s.n==4:
                    s.n=1
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y-s.r,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==2: #низ
                    s.n=3
                if s.n==1:
                    s.n=4
                    
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))
                    
                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999

                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
                    
    class box:
        def __init__(s,x,y,a,t): #создание коробки
            s.x=x
            s.y=y
            s.a=a #текущая анимация
            s.t=t #тип коробки
            s.o=w.create_image(x,y,image=bxm[t][a]) #создание картинки для коробки
    class platform:
        def __init__(s,x,y,wi,he,p):
            s.x=x
            s.y=y
            s.wi=wi
            s.he=he
            s.p=p #скорость платформы
            s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="#000000",outline="#FFEE00", width = 3)
        def move(s,x):
            s.p=spp
            if s.x>x: #х положение мышки s.x положение платформы
                m=-min(s.x-x,s.p)
                s.x+=m #перемещение платформы
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
            s.e=e #эффекты от бонуса
            s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="",outline="#FFFFFF",width=3)
            s.t=w.create_text(x,y,text=names[e],font='ComicSansMS 24 bold',fill='#FFFFFF')
        def inr(s,a,b,c): #вспомогательная функция
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
                if s.e==1: #увеличение платформы на 100
                    pl.wi+=100
                    w.delete(pl.o)
                    pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#000000",outline="#FFEE00",width=3)
                if s.e==-1:#уменьшение платформы на 100
                    pl.wi-=100
                    w.delete(pl.o)
                    pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#000000",outline="#FFEE00",width=3)
                if s.e==2:#ускорение платформы на 33%
                    spp/=0.75
                if s.e==-2: #замедление на 25%
                    spp*=0.75
                if s.e==3: # ускорение и замедление шарика 
                    spb/=0.75
                if s.e==-3:
                    spb*=0.75
        def down(s,pl): #бонус падает
            w.move(s.o,0,heg/400) #объект бонуса
            w.move(s.t,0,heg/400) #рисунок бонуса
            s.y+=heg/400
            s.plat(pl) #бонус упал на платформу
            if s.y>heg: 
                w.delete(s.o)
                w.delete(s.t)
                s.o=0
                s.t=0
                global bonuses
                bonuses=[e for e in bonuses if e.o!=0] #генератор с фильтром

    def gameover():
        w.create_text(wid/2-10,heg/2-10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2-10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2-10,heg/2+10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2+10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2,heg/2,text='GAME OVER',font='ComicSansMS 72',fill='#000000')
        w.update()
        sleep(5)
        PlaySound(None,SND_FILENAME)
        start()

    def gamewin():
        w.create_text(wid/2-10,heg/2-10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2-10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2-10,heg/2+10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2+10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2,heg/2,text='YOU WON',font='ComicSansMS 72',fill='#000000')
        w.update()
        sleep(5)
        PlaySound(None,SND_FILENAME)
        start()

    def motion(e):
        global tx,ty #положение мышки
        tx=e.x
    wid=tk.winfo_screenwidth()
    heg=tk.winfo_screenheight()

    blm=PhotoImage(file='ball.gif',format = 'gif -index 0')
    blw=blm.width()
    blm=blm.zoom(int(wid*0.015),int(wid*0.015))
    blm=blm.subsample(int(bxw),int(bxw))
    #актуальная ширина и высота the ball of the gym
    blw=blm.width()
    blh=blm.height()

    tx=wid/2
    ty=0
    srt=3 #количество жизней
    spb=0.0015*wid #скорость шарика
    spp=0.002*wid #скорость платформы
    tk.geometry('%dx%d+0+0'%(wid,heg))#положение и размер формы
    w=Canvas(tk,width=wid,height=heg) #окошко для рисования
    w.pack()
    w.create_rectangle(0,0,wid,heg,fill='#000000',outline="#000000")
    plat=platform(0.4*wid,0.95*heg,0.25*wid,0.15*heg,0.002*wid) #ФОРМИРОВАНИЕ ПЛАТФОРМЫ
    bal=ball(wid/2,heg/2,blw/2,0.008*wid,'#880088')
    boxes=[[(lambda rr:(box(bxw/2+j*bxw,bxh/2+bxh*i,randint(0,[34,36,48,0][rr]),rr)))(randint(1,2))for j in range(10)]for i in range(4)]
                                        #каждая гифка с разного кадра начинается
    bonuses=[]
    w.bind_all("<Motion>",motion)#привязываем мышку, каждый раз проверяем положение мышки
    bonv=[i for i in range(-3,3+1)] #для эффектов бонусов, чтобы можно было брать случайные бонусы
    bonv=[1,2,3]
    at=time() #начальное время

    @Threaded #новый поток для музыки
    def music():
        PlaySound("fone.wav",SND_FILENAME|SND_LOOP|SND_ASYNC)
    thread = music()
    thread.start()

    while True:
        t=time() #текущее время

        #tk.title(str(bal.n)+' '+str(bal.y))
        w.move(plat.o,plat.move(tx),0)
        (lambda rr:(w.move(bal.o,*rr),w.move(bal.t,*rr)))(bal.move())
        bal.wall() #проверка врезания в стену
        bal.plat(plat) #врезался в платформу
        if time()-at>=0.05: #если прошло больше 50мс, запускаем следующий кадр
            for i in range(4):
                for j in range(10):
                    if boxes[i][j].t!=3:
                        a=boxes[i][j].a+1
                        if boxes[i][j].t==0:
                            a=a%35
                        if boxes[i][j].t==1:
                            a=a%37
                        if boxes[i][j].t==2:
                            a=a%49
                        boxes[i][j].a=a
                        w.itemconfig(boxes[i][j].o,image=bxm[boxes[i][j].t][a])#меняем картинки всех коробочек
            at=time()#перезаписываем время
            
        for i in range(4): #проверка шарика на врезание в коробочки
            for j in range(10):
                bal.box(boxes[i][j],i,j) 
        if randint(1,250)==1 and len(bonuses)<4: #если равно 1, то падает бонус их может быть только <=4 свободных бонусов
            bonuses+=[bonus(randint(0,wid),0,wid*0.05,heg*0.07,bonv[randint(0,2)])]
        for b in bonuses: #передвижение бонусов
            if b.o!=0:
                b.down(plat)
        w.update() #перерисовка, обновление окошка
        while time()-t<0.013: #каждое следующее действие происходит через 13 мс
            pass

def mysterious():
    global boxes,bonuses,srt,spp,spb,tx,ty,plat,bxw,bxh,bxm,tk,wid,heg,bal
    class ball:
        def __init__(s,x,y,p,r,c):
            s.x=x
            s.y=y
            s.p=p #скорость шарика
            s.r=r #радиус
            s.n=randint(1,2)#направление движения шарика
            s.o=w.create_image(x,y,image=blm)#рисуем объект
            s.t=w.create_text(x,y,text=str(srt),font='ComicSansMS 12 bold',fill='#000000')
        def move(s):
            s.p=spb #spb глобальная переменная
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
            global srt,plat
            if s.x-s.r<=0:
                if s.n==1:s.n=2
                if s.n==4:s.n=3
            elif s.x+s.r>=wid: #ширина экрана
                if s.n==2:s.n=1
                if s.n==3:s.n=4
            if s.y-s.r<=0:
                if s.n==2:s.n=3
                if s.n==1:s.n=4
            elif s.y+s.r>=heg: #высота экрана
                if s.n==3:s.n=2
                if s.n==4:s.n=1
                srt-=1
                if srt==0:
                    gameover()
                w.itemconfig(s.t,text=str(srt))
                w.move(s.o,plat.x-s.x,plat.y-plat.he-s.y)
                w.move(s.t,plat.x-s.x,plat.y-plat.he-s.y)
                s.x=plat.x
                s.y=plat.y-plat.he
        def plat(s,pl):
            global boxes
            if s.y+s.r>pl.y-pl.he/2: #and s.y-s.r<pl.y+pl.he/2:
                if s.x+s.r-(pl.x-pl.wi/2)>0 and s.x+s.r-(pl.x-pl.wi/2)<0.005*wid: #проверка, что бы шарик по абсциссе был внутри платформы
                    if s.n==3:s.n=4
                    if s.n==2:s.n=1
                elif pl.x+pl.wi/2-(s.x-s.r)>0 and pl.x+pl.wi/2-(s.x-s.r)<0.005*wid:
                    if s.n==4:s.n=3
                    if s.n==1:s.n=2
            if s.y+s.r-(pl.y-pl.he/2)>0 and s.y+s.r-(pl.y-pl.he/2)<0.005*wid:#отталкивание от бока платформы
                if s.x>pl.x-pl.wi/2 and s.x<pl.x+pl.wi/2:
                    if s.n==3:s.n=2
                    if s.n==4:s.n=1
            if [sum([e.x for e in el])for el in boxes]==[-99990]*4:
                gamewin()
        def inr(s,a,b,c):
            if a>=b and a<=c or a>=c and a<=b:
                return True
        def box(s,bx,i,j): #шарик внутри коробки
            global srt,bonuses,boxes
            if s.inr(s.x+s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==2:#левый бок коробки
                    s.n=1
                if s.n==3:#левый бок с другой стороны
                    s.n=4
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                        
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x-s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==1:#правый бок
                    s.n=2
                if s.n==4:
                    s.n=3
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                        
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y+s.r,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==3:#верх
                    s.n=2
                if s.n==4:
                    s.n=1
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y-s.r,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==2: #низ
                    s.n=3
                if s.n==1:
                    s.n=4
                    
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))
                    
                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999

                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
                    
    class box:
        def __init__(s,x,y,a,t): #создание коробки
            s.x=x
            s.y=y
            s.a=a #текущая анимация
            s.t=t #тип коробки
            s.o=w.create_image(x,y,image=bxm[t][a]) #создание картинки для коробки
    class platform:
        def __init__(s,x,y,wi,he,p):
            s.x=x
            s.y=y
            s.wi=wi
            s.he=he
            s.p=p #скорость платформы
            s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="#000000",outline="#FFEE00", width = 3)
        def move(s,x):
            s.p=spp
            if s.x>x: #х положение мышки s.x положение платформы
                m=-min(s.x-x,s.p)
                s.x+=m #перемещение платформы
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
            s.e=e #эффекты от бонуса
            s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="",outline="#FFFFFF",width=3)
            s.t=w.create_text(x,y,text=names[e],font='ComicSansMS 24 bold',fill='#FFFFFF')
        def inr(s,a,b,c): #вспомогательная функция
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
                if s.e==1: #увеличение платформы на 100
                    pl.wi+=100
                    w.delete(pl.o)
                    pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#000000",outline="#FFEE00",width=3)
                if s.e==-1:#уменьшение платформы на 100
                    pl.wi-=100
                    w.delete(pl.o)
                    pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#000000",outline="#FFEE00",width=3)
                if s.e==2:#ускорение платформы на 33%
                    spp/=0.75
                if s.e==-2: #замедление на 25%
                    spp*=0.75
                if s.e==3: # ускорение и замедление шарика 
                    spb/=0.75
                if s.e==-3:
                    spb*=0.75
        def down(s,pl): #бонус падает
            w.move(s.o,0,heg/400) #объект бонуса
            w.move(s.t,0,heg/400) #рисунок бонуса
            s.y+=heg/400
            s.plat(pl) #бонус упал на платформу
            if s.y>heg: 
                w.delete(s.o)
                w.delete(s.t)
                s.o=0
                s.t=0
                global bonuses
                bonuses=[e for e in bonuses if e.o!=0] #генератор с фильтром

    def gameover():
        w.create_text(wid/2-10,heg/2-10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2-10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2-10,heg/2+10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2+10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2,heg/2,text='GAME OVER',font='ComicSansMS 72',fill='#000000')
        w.update()
        sleep(5)
        PlaySound(None,SND_FILENAME)
        start()

    def gamewin():
        w.create_text(wid/2-10,heg/2-10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2-10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2-10,heg/2+10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2+10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2,heg/2,text='YOU WON',font='ComicSansMS 72',fill='#000000')
        w.update()
        sleep(5)
        PlaySound(None,SND_FILENAME)
        start()

    def motion(e):
        global tx,ty #положение мышки
        tx=e.x

    blm=PhotoImage(file='ball.gif',format = 'gif -index 0')
    blw=blm.width()
    blm=blm.zoom(int(wid*0.015),int(wid*0.015))
    blm=blm.subsample(int(bxw),int(bxw))
    #актуальная ширина и высота the ball of the gym
    blw=blm.width()
    blh=blm.height()

    tx=wid/2
    ty=0
    srt=3 #количество жизней
    spb=0.0015*wid #скорость шарика
    spp=0.002*wid #скорость платформы
    tk.geometry('%dx%d+0+0'%(wid,heg))#положение и размер формы
    w=Canvas(tk,width=wid,height=heg) #окошко для рисования
    w.pack()
    w.create_rectangle(0,0,wid,heg,fill='#000000',outline="#000000")
    plat=platform(0.4*wid,0.95*heg,0.25*wid,0.15*heg,0.002*wid) #ФОРМИРОВАНИЕ ПЛАТФОРМЫ
    bal=ball(wid/2,heg/2,blw/2,0.008*wid,'#880088')
    boxes=[[(lambda rr:(box(bxw/2+j*bxw,bxh/2+bxh*i,randint(0,[34,36,48,0][rr]),rr)))(randint(3,3))for j in range(10)]for i in range(4)]
                                        #каждая гифка с разного кадра начинается
    bonuses=[]
    w.bind_all("<Motion>",motion)#привязываем мышку, каждый раз проверяем положение мышки
    bonv=[i for i in range(-3,3+1)] #для эффектов бонусов, чтобы можно было брать случайные бонусы
    bonv.remove(0)
    at=time() #начальное время

    @Threaded #новый поток для музыки
    def music():
        PlaySound("fone.wav",SND_FILENAME|SND_LOOP|SND_ASYNC)
    thread = music()
    thread.start()

    while True:
        t=time() #текущее время

        #tk.title(str(bal.n)+' '+str(bal.y))
        w.move(plat.o,plat.move(tx),0)
        (lambda rr:(w.move(bal.o,*rr),w.move(bal.t,*rr)))(bal.move())
        bal.wall() #проверка врезания в стену
        bal.plat(plat) #врезался в платформу
        if time()-at>=0.05: #если прошло больше 50мс, запускаем следующий кадр
            for i in range(4):
                for j in range(10):
                    if boxes[i][j].t!=3:
                        a=boxes[i][j].a+1
                        if boxes[i][j].t==0:
                            a=a%35
                        if boxes[i][j].t==1:
                            a=a%37
                        if boxes[i][j].t==2:
                            a=a%49
                        boxes[i][j].a=a
                        w.itemconfig(boxes[i][j].o,image=bxm[boxes[i][j].t][a])#меняем картинки всех коробочек
            at=time()#перезаписываем время
            
        for i in range(4): #проверка шарика на врезание в коробочки
            for j in range(10):
                bal.box(boxes[i][j],i,j) 
        if randint(1,350)==1 and len(bonuses)<4: #если равно 1, то падает бонус их может быть только <=4 свободных бонусов
            bonuses+=[bonus(randint(0,wid),0,wid*0.05,heg*0.07,bonv[randint(0,5)])]
        for b in bonuses: #передвижение бонусов
            if b.o!=0:
                b.down(plat)
        w.update() #перерисовка, обновление окошка
        while time()-t<0.013: #каждое следующее действие происходит через 13 мс
            pass

def impossible():

    global boxes,bonuses,srt,spp,spb,tx,ty,plat,bxw,bxh,bxm,tk,wid,heg,bal
    class ball:
        def __init__(s,x,y,p,r,c):
            s.x=x
            s.y=y
            s.p=p #скорость шарика
            s.r=r #радиус
            s.n=randint(1,2)#направление движения шарика
            s.o=w.create_image(x,y,image=blm)#рисуем объект
            s.t=w.create_text(x,y,text=str(srt),font='ComicSansMS 12 bold',fill='#000000')
        def move(s):
            s.p=spb #spb глобальная переменная
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
            global srt,plat
            if s.x-s.r<=0:
                if s.n==1:s.n=2
                if s.n==4:s.n=3
            elif s.x+s.r>=wid: #ширина экрана
                if s.n==2:s.n=1
                if s.n==3:s.n=4
            if s.y-s.r<=0:
                if s.n==2:s.n=3
                if s.n==1:s.n=4
            elif s.y+s.r>=heg: #высота экрана
                if s.n==3:s.n=2
                if s.n==4:s.n=1
                srt-=1
                if srt==0:
                    gameover()
                w.itemconfig(s.t,text=str(srt))
                w.move(s.o,plat.x-s.x,plat.y-plat.he-s.y)
                w.move(s.t,plat.x-s.x,plat.y-plat.he-s.y)
                s.x=plat.x
                s.y=plat.y-plat.he
        def plat(s,pl):
            global boxes
            if s.y+s.r>pl.y-pl.he/2: #and s.y-s.r<pl.y+pl.he/2:
                if s.x+s.r-(pl.x-pl.wi/2)>0 and s.x+s.r-(pl.x-pl.wi/2)<0.005*wid: #проверка, что бы шарик по абсциссе был внутри платформы
                    if s.n==3:s.n=4
                    if s.n==2:s.n=1
                elif pl.x+pl.wi/2-(s.x-s.r)>0 and pl.x+pl.wi/2-(s.x-s.r)<0.005*wid:
                    if s.n==4:s.n=3
                    if s.n==1:s.n=2
            if s.y+s.r-(pl.y-pl.he/2)>0 and s.y+s.r-(pl.y-pl.he/2)<0.005*wid:#отталкивание от бока платформы
                if s.x>pl.x-pl.wi/2 and s.x<pl.x+pl.wi/2:
                    if s.n==3:s.n=2
                    if s.n==4:s.n=1
            if [sum([e.x for e in el])for el in boxes]==[-99990]*4:
                gamewin()
        def inr(s,a,b,c):
            if a>=b and a<=c or a>=c and a<=b:
                return True
        def box(s,bx,i,j): #шарик внутри коробки
            global srt,bonuses,boxes
            if s.inr(s.x+s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==2:#левый бок коробки
                    s.n=1
                if s.n==3:#левый бок с другой стороны
                    s.n=4
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                        
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x-s.r,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==1:#правый бок
                    s.n=2
                if s.n==4:
                    s.n=3
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                        
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y+s.r,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==3:#верх
                    s.n=2
                if s.n==4:
                    s.n=1
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))

                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999
                
                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
            if s.inr(s.x,bx.x-bxw/2,bx.x+bxw/2) and s.inr(s.y-s.r,bx.y-bxh/2,bx.y+bxh/2):
                if s.n==2: #низ
                    s.n=3
                if s.n==1:
                    s.n=4
                    
                if bx.t==0:#если first тип коробки, то +1 PLOXOI BONUS
                    bonuses+=[bonus(bx.x,0,wid*0.05,heg*0.07,[-1,-2,3][randint(0,2)])]
                if bx.t==1 and randint(1,5)==1:#если второй тип коробки, то +1 жизнь с 20% вероятностью
                    srt+=1
                    w.itemconfig(s.t,text=str(srt))
                    
                if bx.t==2:#если third тип коробки, то yes, Rico, kaboom
                    if i-1>=0 and boxes[i-1][j].x>0 and boxes[i-1][j].y>0:
                        w.delete(boxes[i-1][j].o)
                        boxes[i-1][j].x=-9999
                        boxes[i-1][j].y=-9999
                    if j-1>=0 and boxes[i][j-1].x>0 and boxes[i][j-1].y>0:
                        w.delete(boxes[i][j-1].o)
                        boxes[i][j-1].x=-9999
                        boxes[i][j-1].y=-9999
                    if i+1<len(boxes) and boxes[i+1][j].x>0 and boxes[i+1][j].y>0:
                        w.delete(boxes[i+1][j].o)
                        boxes[i+1][j].x=-9999
                        boxes[i+1][j].y=-9999
                    if j+1<len(boxes[0]) and boxes[i][j+1].x>0 and boxes[i][j+1].y>0:
                        w.delete(boxes[i][j+1].o)
                        boxes[i][j+1].x=-9999
                        boxes[i][j+1].y=-9999

                if bx.t!=3:#если 4 тип коробки, то fuck you
                    w.delete(bx.o)
                    bx.x=-9999
                    bx.y=-9999
                else:
                    bx.t=randint(0,2)
                    bx.a=0
                    w.itemconfig(bx.o,image=bxm[bx.t][0])
                    
    class box:
        def __init__(s,x,y,a,t): #создание коробки
            s.x=x
            s.y=y
            s.a=a #текущая анимация
            s.t=t #тип коробки
            s.o=w.create_image(x,y,image=bxm[t][a]) #создание картинки для коробки
    class platform:
        def __init__(s,x,y,wi,he,p):
            s.x=x
            s.y=y
            s.wi=wi
            s.he=he
            s.p=p #скорость платформы
            s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="#000000",outline="#FFEE00", width = 3)
        def move(s,x):
            s.p=spp
            if s.x>x: #х положение мышки s.x положение платформы
                m=-min(s.x-x,s.p)
                s.x+=m #перемещение платформы
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
            s.e=e #эффекты от бонуса
            s.o=w.create_rectangle(x-wi/2,y-he/2,x+wi/2,y+he/2,fill="",outline="#FFFFFF",width=3)
            s.t=w.create_text(x,y,text=names[e],font='ComicSansMS 24 bold',fill='#FFFFFF')
        def inr(s,a,b,c): #вспомогательная функция
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
                if s.e==1: #увеличение платформы на 100
                    pl.wi+=100
                    w.delete(pl.o)
                    pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#000000",outline="#FFEE00",width=3)
                if s.e==-1:#уменьшение платформы на 100
                    pl.wi-=100
                    w.delete(pl.o)
                    pl.o=w.create_rectangle(pl.x-pl.wi/2,pl.y-pl.he/2,pl.x+pl.wi/2,pl.y+pl.he/2,fill="#000000",outline="#FFEE00",width=3)
                if s.e==2:#ускорение платформы на 33%
                    spp/=0.75
                if s.e==-2: #замедление на 25%
                    spp*=0.75
                if s.e==3: # ускорение и замедление шарика 
                    spb/=0.75
                if s.e==-3:
                    spb*=0.75
        def down(s,pl): #бонус падает
            w.move(s.o,0,heg/400) #объект бонуса
            w.move(s.t,0,heg/400) #рисунок бонуса
            s.y+=heg/400
            s.plat(pl) #бонус упал на платформу
            if s.y>heg: 
                w.delete(s.o)
                w.delete(s.t)
                s.o=0
                s.t=0
                global bonuses
                bonuses=[e for e in bonuses if e.o!=0] #генератор с фильтром

    def gameover():
        w.create_text(wid/2-10,heg/2-10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2-10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2-10,heg/2+10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2+10,text='GAME OVER',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2,heg/2,text='GAME OVER',font='ComicSansMS 72',fill='#000000')
        w.update()
        sleep(5)
        PlaySound(None,SND_FILENAME)
        start()

    def gamewin():
        w.create_text(wid/2-10,heg/2-10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2-10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2-10,heg/2+10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2+10,heg/2+10,text='YOU WON',font='ComicSansMS 72 bold',fill='#FFFFFF')
        w.create_text(wid/2,heg/2,text='YOU WON',font='ComicSansMS 72',fill='#000000')
        w.update()
        sleep(5)
        PlaySound(None,SND_FILENAME)
        start()

    def motion(e):
        global tx,ty #положение мышки
        tx=e.x

    #актуальная ширина и высота гифки
    bxw=bxm[3][-1].width()
    bxh=bxm[3][-1].height()

    blm=PhotoImage(file='ball.gif',format = 'gif -index 0')
    blw=blm.width()
    blm=blm.zoom(int(wid*0.015),int(wid*0.015))
    blm=blm.subsample(int(bxw),int(bxw))
    #актуальная ширина и высота the ball of the gym
    blw=blm.width()
    blh=blm.height()

    tx=wid/2
    ty=0
    srt=3 #количество жизней
    spb=0.0015*wid #скорость шарика
    spp=0.002*wid #скорость платформы
    tk.geometry('%dx%d+0+0'%(wid,heg))#положение и размер формы
    w=Canvas(tk,width=wid,height=heg) #окошко для рисования
    w.pack()
    w.create_rectangle(0,0,wid,heg,fill='#000000',outline="#000000")
    plat=platform(0.4*wid,0.95*heg,0.25*wid,0.15*heg,0.002*wid) #ФОРМИРОВАНИЕ ПЛАТФОРМЫ
    bal=ball(wid/2,heg/2,blw/2,0.008*wid,'#880088')
    boxes=[[(lambda rr:(box(bxw/2+j*bxw,bxh/2+bxh*i,randint(0,[34,36,48,0][rr]),rr)))(randint(0,0))for j in range(10)]for i in range(4)]
                                        #каждая гифка с разного кадра начинается
    bonuses=[]
    w.bind_all("<Motion>",motion)#привязываем мышку, каждый раз проверяем положение мышки
    bonv=[i for i in range(-3,3+1)] #для эффектов бонусов, чтобы можно было брать случайные бонусы
    bonv=[-1,-2,3]
    at=time() #начальное время

    @Threaded #новый поток для музыки
    def music():
        PlaySound("fone.wav",SND_FILENAME|SND_LOOP|SND_ASYNC)
    thread = music()
    thread.start()

    while True:
        t=time() #текущее время

        #tk.title(str(bal.n)+' '+str(bal.y))
        w.move(plat.o,plat.move(tx),0)
        (lambda rr:(w.move(bal.o,*rr),w.move(bal.t,*rr)))(bal.move())
        bal.wall() #проверка врезания в стену
        bal.plat(plat) #врезался в платформу
        if time()-at>=0.05: #если прошло больше 50мс, запускаем следующий кадр
            for i in range(4):
                for j in range(10):
                    if boxes[i][j].t!=3:
                        a=boxes[i][j].a+1
                        if boxes[i][j].t==0:
                            a=a%35
                        if boxes[i][j].t==1:
                            a=a%37
                        if boxes[i][j].t==2:
                            a=a%49
                        boxes[i][j].a=a
                        w.itemconfig(boxes[i][j].o,image=bxm[boxes[i][j].t][a])#меняем картинки всех коробочек
            at=time()#перезаписываем время
            
        for i in range(4): #проверка шарика на врезание в коробочки
            for j in range(10):
                bal.box(boxes[i][j],i,j) 
        if randint(1,350)==1 and len(bonuses)<4: #если равно 1, то падает бонус их может быть только <=4 свободных бонусов
            bonuses+=[bonus(randint(0,wid),0,wid*0.05,heg*0.07,bonv[randint(0,2)])]
        for b in bonuses: #передвижение бонусов
            if b.o!=0:
                b.down(plat)
        w.update() #перерисовка, обновление окошка
        while time()-t<0.013: #каждое следующее действие происходит через 13 мс
            pass



def start():
    global r,m,tk,wid,heg
    #tk=Tk() #создаем окошко

    r=1#rezhim

    tk.geometry('%dx%d+%d+%d'%(wid/3.3,5*wid/(3.3*4),(wid-wid/3.3)/2,(heg-5*wid/(3.3*4))/2))

    mbt=PhotoImage(file='mbt.gif')
    mbw=mbt.width()
    mbt=mbt.zoom(int((wid/30)/10),int((wid/30)/10))
    mbt=mbt.subsample(int(mbw/100),int(mbw/100))

    sbt=PhotoImage(file='sbt.gif')
    sbw=sbt.width()
    sbt=sbt.zoom(int((wid/30)/10),int((wid/30)/10))
    sbt=sbt.subsample(int(sbw/100),int(sbw/100))

    hbt=PhotoImage(file='hbt.gif')
    hbw=hbt.width()
    hbt=hbt.zoom(int((wid/30)/10),int((wid/30)/10))
    hbt=hbt.subsample(int(hbw/100),int(hbw/100))

    pbt=PhotoImage(file='pbt.gif')
    pbw=pbt.width()
    pbt=pbt.zoom(int((wid/30)/10),int((wid/30)/10))
    pbt=pbt.subsample(int(pbw/100),int(pbw/100))

    nbt=PhotoImage(file='nbt.gif')
    nbw=nbt.width()
    nbt=nbt.zoom(int((wid/30)/10),int((wid/30)/10))
    nbt=nbt.subsample(int(nbw/100),int(nbw/100))

    clb=PhotoImage(file='classic.gif')
    clw=clb.width()
    clb=clb.zoom(int((wid/30)/10),int((wid/30)/10))
    clb=clb.subsample(int(clw/100),int(clw/100))

    ewb=PhotoImage(file='easywin.gif')
    eww=ewb.width()
    ewb=ewb.zoom(int((wid/30)/10),int((wid/30)/10))
    ewb=ewb.subsample(int(eww/100),int(eww/100))

    msb=PhotoImage(file='mysterious.gif')
    msw=msb.width()
    msb=msb.zoom(int((wid/30)/10),int((wid/30)/10))
    msb=msb.subsample(int(msw/100),int(msw/100))

    imb=PhotoImage(file='impossible.gif')
    imw=imb.width()
    imb=imb.zoom(int((wid/30)/10),int((wid/30)/10))
    imb=imb.subsample(int(imw/100),int(imw/100))

    def begin():
        global boxes,bonuses,srt,spp,spb,tx,ty,plat,r,m,wid
        boxes=[]
        bonuses=[]
        srt,spp,spb,tx,ty,bal,plat=0,0,0,wid/2,0,0,0
        #tk.destroy()
        
        PlaySound(None,SND_FILENAME)
        if r==0:
            easywin()
        elif r==1:
            classic()
        elif r==2:
            mysterious()
        elif r==3:
            impossible()

    b=Button(tk,command=begin,relief=FLAT,image=mbt)
    b.pack()
    b.place(relx=0,rely=0,relheight=2/5,relwidth=1)

    def nx():
        global m,r
        if r==0:
            m.destroy()
            m=Button(tk,relief=FLAT,command=nx,image=clb)
            m.pack()
            m.place(relx=0,rely=1/2.5,relheight=1/5,relwidth=1)
            r=1
        elif r==1:
            m.destroy()
            m=Button(tk,relief=FLAT,command=nx,image=msb)
            m.pack()
            m.place(relx=0,rely=1/2.5,relheight=1/5,relwidth=1)
            r=2
        elif r==2:
            m.destroy()
            m=Button(tk,relief=FLAT,command=nx,image=imb)
            m.pack()
            m.place(relx=0,rely=1/2.5,relheight=1/5,relwidth=1)
            r=3
        elif r==3:
            m.destroy()
            m=Button(tk,relief=FLAT,command=nx,image=ewb)
            m.pack()
            m.place(relx=0,rely=1/2.5,relheight=1/5,relwidth=1)
            r=0

    m=Button(tk,relief=FLAT,command=nx,image=clb)
    m.pack()
    m.place(relx=0,rely=1/2.5,relheight=1/5,relwidth=1)

    h=Button(tk,text='Помощь',command=lambda:webbrowser.open("https://vk.com/akhvn"),relief=FLAT,image=hbt)
    h.pack()
    h.place(relx=0,rely=3/5,relheight=2/5,relwidth=1)

    @Threaded #новый поток для музыки
    def music():
        PlaySound("main.wav",SND_FILENAME|SND_LOOP|SND_ASYNC)
    thread = music()
    thread.start()

    tk.mainloop()
start()
