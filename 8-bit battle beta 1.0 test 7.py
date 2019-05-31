import pygame,sys,time
from pygame.locals import*
stoPt='School'
pygame.init()
lives=3
ori=[0,0]
choise=1
ti=0
mode='select'
progress=0
storyMode=False
pc='continue'
die=[False,'no']
antiAir=[]
strike=[]
def laserHit(person,check,die):
    if not person[2]=='block' and (person[7] <= check[4] and check[4] <= person[7]+50):
            person[9]-=check[5][0]
            person[11][0]=check[5][9]
            person[11][1]=['stun',check[5][8],check[5][7]]
            if check[1]=='R':
                person[11][1][1]*=-1
            if person[9]<=0:
                die[0]=True
                die[1]=person[1]
                return None
    die[0]=False
    die[1]=None
def antiAirHit(person,check,die):
    if not person[2]=='block' and (person[7] <= check[2] and check[2] >= person[7]-check[3][7]):
            person[9]-=check[3][0]
            person[11][0]=check[3][6]
            person[11][1]=['stun',check[3][5],check[3][4]]
            if check[4]=='R':
                person[11][1][1]*=-1
            if person[9]<=0:
                die[0]=True
                die[1]=person[1]
                return None
    die[0]=False
    die[1]=None
def atac(location):
    for loc in location:
        if not loc[11][0]==0:
            if loc[7]==450:
                loc[5]=False
            loc[11][0]-=1
            if loc[11][1][0]=='stun':
                loc[0]-=loc[11][1][1]
                loc[7]-=loc[11][1][2]
            if loc[11][1]==loc[10][2] and loc[11][0]==loc[11][1][5]:
                if loc[1]=='man':
                    lasers.append([location[0][0],location[0][2],0,'man',location[0][7]+20,location[0][10][2]])
                else:
                    lasers.append([location[1][0],location[1][2],0,'AI',location[1][7]+20,location[1][10][2]])
            if loc[11][1]==loc[10][3] and loc[11][0]>=loc[11][1][3] and loc[11][0]<=loc[11][1][3]+loc[11][1][2]:
                if loc[1]=='man':
                    antiAir.append([location[0][0],'man',location[0][7]+20,location[0][10][3],location[0][2]])
                else:
                    antiAir.append([location[1][0],'AI',location[1][7]+20,location[1][10][3],location[1][2]])
            if loc[11][1]==loc[10][4] and loc[11][0]>=(-1*loc[11][1][3]):
                if loc[1]=='man':
                    strike.append([location[0][0],'man',location[0][7]+20,location[0][10][4],location[0][2]])
                else:
                    strike.append([location[1][0],'AI',location[1][7]+20,location[1][10][4],location[1][2]])
                if loc[2]=='L':
                    loc[0]+=loc[11][1][2]
                else:
                    loc[0]-=loc[11][1][2]
                loc[7]-=loc[11][1][1]
def at(attack,stun,types):
    stun[1]=attack
    if types=='laser':
        stun[0]=attack[4]+attack[5]
    elif types=='antiAir':
        stun[0]=attack[1]+attack[2]+attack[3]
    elif types=='strike':
        stun[0]=-1
def createGuy(person):
    if pause:
        if person[1]=='man' or not person[10]==location[0][10]:
            color=person[10][1][1]
        else:
            color=person[10][1][3]
    else:
        if person[1]=='man' or not person[10]==location[0][10]:
            color=person[10][1][0]
        else:
            color=person[10][1][2]
    pygame.draw.polygon(windowSurface,color,((person[0]-30,person[7]+50),(person[0],person[7]+50),(person[0],person[7]),(person[0]-30,person[7])))
    if not person[2]=='block' and not person[2]==None:
        if person[2]=='L':
            direction=-45
        else:
            direction=15
        if person[11][0]==0:
            pygame.draw.ellipse(windowSurface,person[10][1][4],(person[0]+direction*3/5-15,person[7]+15,20,20),10)
        elif person[11][1]==person[10][2]:
            direction+=ori[0]
            if person[2]=='AI':
                direction+=ori[1]
                ori[1]*=-1
            else:
                ori[0]*=-1
            pygame.draw.polygon(windowSurface,black,((person[0]-15,person[7]+18),(person[0]+direction,person[7]+18),(person[0]+direction,person[7]+22),(person[0]-15,person[7]+22)))
            pygame.draw.polygon(windowSurface,black,((person[0]-16,person[7]+18),(person[0]-14,person[7]+18),(person[0]-14,person[7]+30),(person[0]-16,person[7]+30)))
        elif person[11][1]==person[10][3]:
            if person[11][0]<=person[11][1][1]:
                pygame.draw.ellipse(windowSurface,person[10][1][4],(person[0]+direction*3/5-15,person[7]+15-(person[11][1][7]*(person[11][1][1]+person[11][1][2]+person[11][1][3]-person[11][0])/person[11][1][1]),20,20),10)
            elif person[11][0]<=person[11][1][1]+person[11][1][2]:
                pygame.draw.ellipse(windowSurface,person[10][1][4],(person[0]+direction*3/5-15,person[7]+15-(person[11][1][7]),20,20),10)
    if person[2]=='block':
        pygame.draw.ellipse(windowSurface,black,(person[0]-16,person[7]+18,20,20),10)
windowSurface=pygame.display.set_mode((700,600),0,32)
pygame.display.set_caption('8-bit Battle')

lasers=[]
black=(0,0,0)
grey=(100,100,100)
white=(255,255,255)
red=(255,0,0)
green=(0,128,0)
blue=(0,0,255)
yellow=(255,255,0)
darkRed=(100,0,0)
darkGreen=(0,50,0)
darkBlue=(0,0,100)
orenge=(255,120,0)
#      character formating   [name,colors,gun attack,anti air,strike,kick,punch,HP,jump strength,speed]
#      jun formtion          [damage,speed,crash check,decay speed,startup,endlag,colors,y knockback,x knockback,hit stun]
#      anti air format       [damage,start up,active,endlag,y knockback,x knockback,hitstun,y size,x size]
#      strike formating      [damage,y speed,x speed,startup,endlag,y bounce,x bounce,y knockback,x knockback,hitstun]
characters=[['bit man v.8',[blue,darkBlue,red,darkRed,orenge],[2,1,'hi',.002,10,240,[green,darkGreen],.5,.3,10],[3,19,7,48,.8,.2,10,50,15],[2,.3,.3,15,72,.35,.1,.32,.15,65],'TBD','TBD',5,1,.5],
            ['quin',[grey,grey,blue,darkBlue,black],[1,1.5,'hi',.005,7,150,[blue,darkBlue],1,.5,17],[2,25,5,52,1.2,.5,15,35,28],[3,.6,.09,20,80,.25,.6,.24,.7],'TBD','TBD',4,1.5,.7],'TBD','TBD','TBD']
t=0
location=[[550,'man','L',25,0,False,0,450,250,5,characters[0],[0,None]],[150,'AI','R',25,0,False,0,450,250,5,characters[0],[0,None]]]
pause=False
inAGame=False
end=False
while True:
    even=None
    defend=False
    if pause:
        windowSurface.fill(grey)
        pygame.draw.polygon(windowSurface,darkRed,((700,600),(0,600),(0,500,),(700,500)))
        pygame.draw.polygon(windowSurface,black,((650,600),(50,600),(50,500),(650,500)))
        createGuy(location[0])
        createGuy(location[1])
        for l in lasers:
            pygame.draw.line(windowSurface,l[5][6][1],(l[0],l[4]),(l[0]-25,l[4]))
        if pc=='continue':
            text=basicFont.render('continue',True,blue,yellow)
        else:
            text=basicFont.render('continue',True,blue,grey)
        textRect=text.get_rect()
        textRect.centerx=300
        textRect.centery=280
        windowSurface.blit(text,textRect)
        if pc=='main menu':
            text=basicFont.render('main menu',True,blue,yellow)
        else:
            text=basicFont.render('main menu',True,blue,grey)
        textRect=text.get_rect()
        textRect.centerx=300
        textRect.centery=320
        windowSurface.blit(text,textRect)
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pause=False
                    pc='continue'
                if event.key==K_UP:
                    pc='continue'
                if event.key==K_DOWN:
                    pc='main menu'
                if event.key==K_RETURN:
                    if pc=='continue':
                        pause=False
                    else:
                        pause=False
                        inAGame=False
                        pc='continue'
                        location=[[550,'man','L',25,0,False,0,450,250,5,characters[0],[0,None]],[150,'AI','R',25,0,False,0,450,250,5,characters[0],[0,None]]]
        storyMode=False
    if inAGame and not end and not pause:
        strike=[]
        antiAir=[]
        if ti==0:
            location[0][9]=location[0][10][7]
            location[1][9]=location[1][10][7]
            ti+=1
        atac(location)
        windowSurface.fill(white)
        pygame.draw.polygon(windowSurface,red,((700,600),(0,600),(0,500,),(700,500)))
        pygame.draw.polygon(windowSurface,black,((650,600),(50,600),(50,500),(650,500)))
        createGuy(location[0])
        createGuy(location[1])

        for l in lasers:
            if l[1]=='R':
                l[0]=l[0]+l[5][1]
            else:
                l[0]=l[0]-l[5][1]
            pygame.draw.line(windowSurface,l[5][6][0],(l[0],l[4]),(l[0]-25,l[4]))
        if not difficulty=='PvP':
            action=False
            qwerty=True
            for lazer in lasers:
                if (lazer[0]-50<location[1][0] and lazer[0]+50>location[1][0]) and lazer[3]=='man':
                    qwerty=False
                if (lazer[0]-50<location[1][0] and lazer[0]+50>location[1][0]) and lazer[3]=='man' and (t>=((10-difficulty)/30)):
                    if location[1][4]<=.25:
                        location[1][2]='block'
                        action=True
                    if location[1][4]>.25 and difficulty>=7 and lazer[0]-50<location[1][0] and location[1][0]==450:
                        location[1][6]=1
                        action=True
                    if location[0][6]==location[1][6]:
                        location[1][2]='block'
                        action=True
                    if not location[0][6]==0 and not location[1][6]==0:
                        location[1][2]='block'
                        action=True
            if  not location[0][0]-location[1][0]>25*(10-difficulty) and action==False and (t>=.2 or t>=((10-difficulty)/20)) and not location[1][0]<=70:
                location[1][2]='L'
                location[1][5]=True
                t=0
                action==True
            elif location[0][0]-location[1][0]>25*(10-difficulty)+150 and action==False and (t>=.2 or t>=(((10-difficulty)/20))+.5) or (t>=1.75 and not difficulty>=3 and not difficulty<=7):
                t=0
                location[1][2]='R'
                location[1][5]=True
                action=True
            elif location[0][0]-location[1][0]>25*(10-difficulty)+150 and action==False and (t>=.2 or t>=(((10-difficulty)/20))+.5) or (t>=1.25 and difficulty==1):
                t=0
                location[1][2]='R'
                location[1][5]=True
                action=True
            elif (((t>=.5 or ((t>=((((10-difficulty))/20))+.3)))) and(( action==False or location[0][4]==0))) :
                if location[1][2]=='L':
                    location[1][2]='R'
                    location[1][5]=True
                    action==True
                    t=0
                elif (not difficulty==1) and (not location[1][3]==0) and not(location[1][2]==None or location[1][2]=='block') and (t>=.5 or t>=(((10-difficulty)/20))+.3)and location[1][8]==250:
                    lasers.append([location[1][0],location[1][2],0,'AI',location[1][7]+20])
                    location[1][8]=0
                    t=0
                    location[1][3]-=1
                    action=True
                elif difficulty==1 and t>=.6 and not location[1][3]==0 and not (location[1][2]==None or location[1][2]=='block')and location[1][8]==250:
                    lasers.append([location[1][0],location[1][2],0,'AI',location[1][7]+20])
                    location[1][8]=0
                    t=0
                    location[1][3]-=1
                elif t>=.7:
                    location[1][2]='L'
                    location[1][5]=True
                    action=True
                    t=0 
            if location[1][5] and t>=.2 or (location[1][0]<=70 and location[1][2]=='L') or (location[1][0]>=630 and location[1][2]=='R'):
                location[1][5]=False
            if location[1][7]==450 and (not location[1][2]=='block') and location[1][0]+100>=location[0][0] and location[1][0]-100<=location[0][0]:
                location[1][6]=1
            t=t+.002
            ti+=1
            if location[1][4]>=4.5 and location[1][2]=='block' and qwerty:
                location[1][2]='R'
                location[1][5]=True
            qwerty=True
        for x in lasers:
            if x[2]>=1:
                lasers.remove(x)
            else:
                x[2]=x[2]+x[5][3]
        death=False
        for n in location:
            if n[2]=='block':
                if n[4]>=n[10][7]:
                    n[2]=None
                else:
                    n[4]=n[4]+.035
            elif not n[4]<=0:
                n[4]=n[4]-.035
        for check in lasers:
            for person in location:
                if person[0]>=check[0]-5 and person[0]<=check[0]+5 and not check[3]==person[1]:
                    laserHit(person,check,die)
                    death=die[0]
                    if death:
                        dead=die[1]
                    lasers.remove(check)
        for check in antiAir:
            for person in location:
                if check[4]=='R':
                    if person[0]<=check[0]+check[3][8] and person[0]>=check[0] and not check[1]==person[1]:
                        location[0][11][1]=['stun',0,0]
                        location[1][11][1]=['stun',0,0]
                        antiAirHit(person,check,die)
                        death=die[0]
                        if death:
                            dead=die[1]
                        
                else:
                    if person[0]>=check[0]-check[3][8] and person[0]<=check[0] and not check[1]==person[1]:
                        location[0][11][1]=['stun',0,0]
                        location[1][11][1]=['stun',0,0]
                        antiAirHit(person,check,die)
                        death=die[0]
                        if death:
                            dead=die[1]
        for perkon in location:
                if (perkon[0]<50 or perkon[0]>680) and perkon[7]==450:
                    death=True
                    dead=perkon[1]
                if perkon[8]<250:
                    perkon[8]+=1
        if death==True:
            if not difficulty=='PvP':
                if dead=='AI':
                    text=basicFont.render('YOU WIN',True,green,white)
                    textRect=text.get_rect()
                    textRect.centerx=350
                    textRect.centery=300
                    windowSurface.blit(text,textRect)
                    progress+=1
                else:
                    text=basicFont.render('YOU LOSE',True,red,white)
                    textRect=text.get_rect()
                    textRect.centerx=350
                    textRect.centery=300
                    windowSurface.blit(text,textRect)
                    lives-=1
            else:
                if dead=='AI':
                    text=basicFont.render('P.1 WIN\'S',True,blue,white)
                    textRect=text.get_rect()
                    textRect.centerx=350
                    textRect.centery=300
                    windowSurface.blit(text,textRect)
                else:
                    text=basicFont.render('P.2 WIN\'S',True,red,white)
                    textRect=text.get_rect()
                    textRect.centerx=350
                    textRect.centery=300
                    windowSurface.blit(text,textRect)
            text=basicFont.render('play again',True,green,white)
            textRect=text.get_rect()
            textRect.centerx=350
            textRect.centery=400
            windowSurface.blit(text,textRect)
            pygame.display.update()
            end=True
            inAGame=False
        Lift=False
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if location[0][11][0]==0:
                    if event.key==K_ESCAPE:
                        pause=True
                    if event.key==K_LEFT:
                        Lift=True
                        location[0][5]=True
                        location[0][2]='L'
                    if event.key==K_RIGHT:
                        Lift=True
                        location[0][5]=True
                        location[0][2]='R'
                    if event.key==K_SPACE:
                       if not location[0][2]=='block' and not location[0][2]==None and location[0][11][0]==0:
                           at(location[0][10][2],location[0][11],'laser')
                           #lasers.append([location[0][0],location[0][2],0,'man',location[0][7]+20,location[0][10][2]])
                           location[0][3]-=1
                           location[0][8]=0
                           ori[0]=1
                           if location[0][7]==450:
                               location[0][5]=False
                    if event.key==K_DOWN and location[0][4]<=0:
                       location[0][2]='block'
                    if event.key==K_UP and location[0][7]==450:
                        location[0][6]=location[0][10][8]
                    if event.key==K_n and location[0][7]==450:
                        if not location[0][2]=='block' and not location[0][3]<=0 and not location[0][2]==None and location[0][11][0]==0 and location[0][7]==450:
                           at(location[0][10][3],location[0][11],'antiAir')
                           location[0][5]=False
                    elif event.key==K_n:
                        if not location[0][2]=='block' and not location[0][2]==None and location[0][11][0]==0:
                           at(location[0][10][3],location[0][11],'strike')
                if difficulty=='PvP' and location[1][11][0]==0:
                    if event.key==K_a:
                        location[1][5]=True
                        location[1][2]='L'
                        Lift=True
                    if event.key==K_d:
                        location[1][5]=True
                        location[1][2]='R'
                        Lift=True
                    if event.key==K_TAB:
                       if not location[1][2]=='block' and not location[0][2]==None and location[1][8]==250:
                           at(location[1][10][2],location[1][11],'laser')
                           #lasers.append([location[1][0],location[1][2],0,'AI',location[1][7]+20])
                           location[1][3]-=1
                           location[1][8]=0
                           ori[1]=15
                    if event.key==K_1:
                        if not location[1][2]=='block' and not location[1][3]<=0 and not location[1][2]==None and location[1][11][0]==0 and location[1][7]==450:
                           at(location[1][10][3],location[1][11],'antiAir')
                           location[1][5]=False
                    if event.key==K_w and location[1][7]==450:
                        location[1][6]=1
                    if event.key==K_s and location[1][4]<=0:
                        location[1][2]='block'
            if event.type==KEYUP:
                if event.key==K_LEFT and location[0][2]=='L' and not Lift:
                    location[0][5]=False
                if event.key==K_RIGHT and location[0][2]=='R' and not Lift:
                    location[0][5]=False
                if difficulty=='PvP':
                    if event.key==K_a and location[1][2]=='L' and not Lift:
                        location[1][5]=False
                    if event.key==K_d and location[1][2]=='R' and not Lift:
                        location[1][5]=False
        for movement in location:
            if not (movement[11][1]==movement[10][4] and movement[11][0]>=(-1*movement[11][1][3])):
                if movement[5]:
                    if movement[2]=='L':
                        movement[0]-=movement[10][9]
                    elif movement[2]=='R':
                        movement[0]+=movement[10][9]
                movement[7]-=movement[6]
                movement[6]-=.01
                if movement[7]>=450 and movement[6]<=0:
                    movement[6]=0
                    movement[7]=450
        if location[0][3]==0 and location[1][3]==0:
            location[0][3]=25
            location[1][3]=25
        for up in location:
            text=basicFont.render(str(up[3]),True,black,white)
            textRect=text.get_rect()
            if up[1]=='man':
                textRect.centerx=650
            else:
                textRect.centerx=50
            textRect.centery=100
            windowSurface.blit(text,textRect)
            text=basicFont.render(str(up[9]),True,black,white)
            textRect=text.get_rect()
            if up[1]=='man':
                textRect.centerx=650
            else:
                textRect.centerx=50
            textRect.centery=50
            windowSurface.blit(text,textRect)
    elif not end and not storyMode and not pause:
        windowSurface.fill(white)
        basicFont=pygame.font.SysFont(None,48)
        if mode=='quick play':
            if choise==1:
                text=basicFont.render('easy',True,green,yellow)
            else:
                text=basicFont.render('easy',True,green,white)
            textRect=text.get_rect()
            textRect.centerx=140
            textRect.centery=300
            windowSurface.blit(text,textRect)
            basicFont=pygame.font.SysFont(None,48)
            if choise==2:
                text=basicFont.render('normal',True,yellow,red)
            else:
                text=basicFont.render('normal',True,yellow,white)
            textRect=text.get_rect()
            textRect.centerx=280
            textRect.centery=300
            windowSurface.blit(text,textRect)
            basicFont=pygame.font.SysFont(None,48)
            if choise==3:
                text=basicFont.render('hard',True,red,yellow)
            else:
                text=basicFont.render('hard',True,red,white)
            textRect=text.get_rect()
            textRect.centerx=420
            textRect.centery=300
            windowSurface.blit(text,textRect)
        elif mode=='select':
            if choise==1:
                text=basicFont.render('PvP',True,blue,yellow)
            else:
                text=basicFont.render('PvP',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=90
            textRect.centery=300
            windowSurface.blit(text,textRect)
            if choise==2:
                text=basicFont.render('quick play',True,blue,yellow)
            else:
                text=basicFont.render('quick play',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=280
            textRect.centery=300
            windowSurface.blit(text,textRect)
            if choise==3:
                text=basicFont.render('story mode',True,blue,yellow)
            else:
                text=basicFont.render('story mode',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=500
            textRect.centery=300
            windowSurface.blit(text,textRect)
        elif mode=='easy':
            if choise==1:
                text=basicFont.render('lv-1',True,blue,yellow)
            else:
                text=basicFont.render('lv-1',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=140
            textRect.centery=300
            windowSurface.blit(text,textRect)
            if choise==2:
                text=basicFont.render('lv-2',True,blue,yellow)
            else:
                text=basicFont.render('lv-2',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=280
            textRect.centery=300
            windowSurface.blit(text,textRect)
            if choise==3:
                text=basicFont.render('lv-3',True,blue,yellow)
            else:
                text=basicFont.render('lv-3',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=420
            textRect.centery=300
            windowSurface.blit(text,textRect)
        elif mode=='normal':
            if choise==1:
                text=basicFont.render('lv-4',True,blue,yellow)
            else:
                text=basicFont.render('lv-4',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=140
            textRect.centery=300
            windowSurface.blit(text,textRect)
            if choise==2:
                text=basicFont.render('lv-5',True,blue,yellow)
            else:
                text=basicFont.render('lv-5',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=280
            textRect.centery=300
            windowSurface.blit(text,textRect)
            if choise==3:
                text=basicFont.render('lv-6',True,blue,yellow)
            else:
                text=basicFont.render('lv-6',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=420
            textRect.centery=300
            windowSurface.blit(text,textRect)
        elif mode=='hard':
            if choise==1:
                text=basicFont.render('lv-7',True,blue,yellow)
            else:
                text=basicFont.render('lv-7',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=140
            textRect.centery=300
            windowSurface.blit(text,textRect)
            if choise==2:
                text=basicFont.render('lv-8',True,blue,yellow)
            else:
                text=basicFont.render('lv-8',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=280
            textRect.centery=300
            windowSurface.blit(text,textRect)
            if choise==3:
                text=basicFont.render('lv-9',True,blue,yellow)
            else:
                text=basicFont.render('lv-9',True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=420
            textRect.centery=300
            windowSurface.blit(text,textRect)
        if not mode=='select':
            if choise==4:
                text=basicFont.render('back',True,black,yellow)
            else:
                text=basicFont.render('back',True,black,white)
            textRect=text.get_rect()
            textRect.centerx=550
            textRect.centery=300
            windowSurface.blit(text,textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_LEFT:
                    if choise==3 or choise==4:
                        choise-=1
                    else:
                        choise=1
                if event.key==K_RIGHT:
                    if choise==1 or choise==2:
                        choise+=1
                    elif not mode=='select':
                        choise=4
                    else:
                        choise=3
                if event.key==K_RETURN:
                    ti=0
                    if mode=='select':
                        if choise==1:
                            difficulty='PvP'
                            inAGame=True
                            mode='select'
                        elif choise==2:
                            mode='quick play'
                        elif choise==3:
                            storyMode=True
                            lives=3
                            progress=0
                            stoPt='school'
                    elif mode=='quick play':
                        if choise==1:
                            mode='easy'
                        elif choise==2:
                            mode='normal'
                        elif choise==3:
                            mode='hard'
                    elif mode=='easy':
                        if choise==1:
                            difficulty=1
                            inAGame=True
                            mode='select'
                        elif choise==2:
                            difficulty=2
                            inAGame=True
                            mode='select'
                        elif choise==3:
                            difficulty=3
                            inAGame=True
                            mode='select'
                    elif mode=='normal':
                        if choise==1:
                            difficulty=4
                            inAGame=True
                            mode='select'
                        elif choise==2:
                            difficulty=5
                            inAGame=True
                            mode='select'
                        elif choise==3:
                            difficulty=6
                            inAGame=True
                            mode='select'
                    elif mode=='hard':
                        if choise==1:
                            difficulty=7
                            inAGame=True
                            mode='select'
                        elif choise==2:
                            difficulty=8
                            inAGame=True
                            mode='select'
                        elif choise==3:
                            difficulty=9
                            inAGame=True
                            mode='select'
                    if choise==4:
                        if mode=='quick play':
                            mode='select'
                        else:
                            mode='quick play'
                    choise=1
                    ti=0
    elif storyMode and not end:
        if stoPt=='school':
            if lives==0:
                storyMode=False
                print(str(1+progress))
            elif progress==3:
                stoPt='locals'
                lives=2
                progress=0
            elif lives+progress==1:
                difficulty=1
                inAGame=True
            elif lives+progress==2:
                difficulty=2
                inAGame=True
            elif lives+progress==3:
                difficulty=3
                inAGame=True
            elif lives+progress==4:
                difficulty=5
                inAGame=True
            elif lives+progress==5:
                difficulty=7
                inAGame=True
        elif stoPt=='locals':
            if lives==0:
                storyMode=False
                print(str(progress+4))
            elif progress==2:
                stoPt='natinals'
                lives=2
                progress=0
            elif lives+progress==1:
                difficulty=4
                inAGame=True
            elif lives+progress==2:
                difficulty=5
                inAGame=True
            elif lives+progress==3:
                difficulty=7
                inAGame=True
        elif stoPt=='natinals':
            if lives==0:
                storyMode=False
                print(str(progress+6))
            elif progress==2:
                stoPt='internatinals'
                lives=1
                progress=0
            elif lives+progress==1:
                difficulty=6
                inAGame=True
            elif lives+progress==2:
                difficulty=7
                inAGame=True
            elif lives+progress==3:
                difficulty=8
                inAGame=True
        elif stoPt=='internatinals':
            if lives==0:
                storyMode=False
                print(str(progress+8))
            elif progress==2:
                storyMode=False
                print('10')
            elif progress==0:
                difficulty=8
                inAGame=True
            elif progress==1:
                difficulty=9
                inAGame=True
    else:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_RETURN:
                    end=False
                    inAGame=False
                    location=[[550,'man','L',25,0,False,0,450,250,characters[0][7],characters[1],[0,None]],[150,'AI','R',25,0,False,0,450,250,characters[0][7],characters[0],[0,None]]]
                    lasers=[]
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    time.sleep(0.002)
