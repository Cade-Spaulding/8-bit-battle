import pygame,sys,time,random
from pygame.locals import*
stoPt='School'
pygame.init()
lives=3
ori=[0,0]
grab=[]
choise=1
ti=0
mode='select'
progress=0
storyMode=False
pc='continue'
die=[False,'no']
antiAir=[]
strike=[]
normal=[]
def laserHit(person,check,die):
    if (person[7] <= check[4] and check[4] <= person[7]+50):
        if not person[2]=='block':
            person[9]-=check[5][0]
            person[11][0]=check[5][9]
            person[11][1]=['stun',check[5][8],check[5][7]]
            if check[1]=='R':
                person[11][1][1]*=-1
            if person[9]<=0:
                die[0]=True
                die[1]=person[1]
                return None
        else:
            person[11][0]=check[3][10]
    die[0]=False
    die[1]=None
def strikeHit(person,check,die):
    if not person[2]=='block':
            person[9]-=check[3][0]
            person[11][0]=check[3][9]
            person[11][1]=['stun',check[3][8],check[3][7]]
            if check[4]=='R':
                person[11][1][1]*=-1
            if person[9]<=0:
                die[0]=True
                die[1]=person[1]
                return None
    else:
        person[11][0]=check[3][10]
    die[0]=False
    die[1]=None
def antiAirHit(person,check,die):
    if  (person[7] >= check[2]-check[3][7]):
        if not person[2]=='block':
            person[9]-=check[3][0]
            person[11][0]=check[3][6]
            person[11][1]=['stun',check[3][5],check[3][4]]
            if check[4]=='R':
                person[11][1][1]*=-1
            if person[9]<=0:
                die[0]=True
                die[1]=person[1]
                return None
        else:
            person[11][0]=check[3][9]
    die[0]=False
    die[1]=None
def normalHit(person,check,die):
    if (person[7] <= check[2] and check[2] < person[7]+25):
        if not person[2]=='block':
            person[9]-=check[3][0]
            person[11][0]=check[3][6]
            person[11][1]=['stun',check[3][5],check[3][4]]
            if check[4]=='R':
                person[11][1][1]*=-1
            if person[9]<=0:
                die[0]=True
                die[1]=person[1]
                return None
        else:
            person[11][0]=check[3][8]
    die[0]=False
    die[1]=None
def grabHit(person,check,die):
    if (person[7] <= check[2] and check[2] < person[7]+25):
            person[2]=None
            person[7]=check[2]
            person[0]=check[0]
            person[9]-=check[3][0]
            person[11][0]=check[3][7]
            person[11][1]=['KD-air',check[3][6],check[3][5]]
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
                if loc[11][1]==loc[10][4] and loc[2]=='L':
                    loc[11]=[loc[11][1][4],['stun',loc[11][1][6],loc[11][1][5]]]
                elif loc[11][1]==loc[10][4]:
                    loc[11]=[loc[11][1][4],['stun',-loc[11][1][6],loc[11][1][5]]]
            if not loc[11][1][0]=='KD-air':
                loc[11][0]-=1
                if loc[11][1][0]=='KD' and loc[11][0]==0:
                    loc[11][1][0]='stun'
            if loc[11][1][0]=='KD-air' and loc[7]==450:
                loc[11][1]=['KD',0,0]
            if loc[11][1][0]=='stun' or loc[11][1][0]=='KD-air':
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
            if loc[11][1]==loc[10][4] and loc[11][0]<=(-1*loc[11][1][3]):
                if loc[1]=='man':
                    strike.append([location[0][0],'man',location[0][7]+20,location[0][10][4],location[0][2]])
                else:
                    strike.append([location[1][0],'AI',location[1][7]+20,location[1][10][4],location[1][2]])
                if loc[2]=='L':
                    loc[0]-=loc[11][1][2]
                else:
                    loc[0]+=loc[11][1][2]
                loc[7]+=loc[11][1][1]
            if (loc[11][1]==loc[10][5] or loc[11][1]==loc[10][6]) and loc[11][0]>=loc[11][1][3] and loc[11][0]<=loc[11][1][3]+loc[11][1][2]:
                if loc[1]=='man':
                    normal.append([location[0][0],'man',location[0][7]+20,location[0][11][1],location[0][2]])
                else:
                    normal.append([location[1][0],'AI',location[1][7]+20,location[1][11][1],location[1][2]])
            if (loc[11][1]==loc[10][11]) and loc[11][0]>=loc[11][1][4] and loc[11][0]<=loc[11][1][4]+loc[11][1][2]:
                if loc[1]=='man':
                    grab.append([location[0][0],'man',location[0][7],location[0][11][1],location[0][2]])
                else:
                    grab.append([location[1][0],'AI',location[1][7],location[1][11][1],location[1][2]])
            if loc[11][1]==loc[10][10] and loc[11][0]<=loc[11][1][1]+loc[11][1][2] and loc[11][0]>=loc[11][1][2]:
                if loc[2]=='L':
                    loc[0]-=loc[11][1][3]
                else:
                    loc[0]+=loc[11][1][3]
       
def at(attack,stun,types):
    stun[1]=attack
    if types=='laser':
        stun[0]=attack[4]+attack[5]
    elif types=='antiAir' or types=='normal':
        stun[0]=attack[1]+attack[2]+attack[3]
    elif types=='strike':
        stun[0]=-1
    elif types=='dash':
        stun[0]=attack[0]+attack[1]+attack[2]
    elif types=='grab':
        stun[0]=attack[1]+attack[2]+attack[4]
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
        if person[11][0]==0 or person[11][1]==person[10][4]:
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
        elif person[11][1]==person[10][5]:
            pygame.draw.ellipse(windowSurface,person[10][1][4],(person[0]+direction*2.8-15,person[7]+45,20,20),10)
        elif person[11][1]==person[10][6]:
            pygame.draw.ellipse(windowSurface,person[10][1][4],(person[0]+direction*1.2-15,person[7]+15,20,20),10)
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
brown=(128,63,0)
sky=(0,128,255)
lightBlue=(0,255,255)
tan=(255,255,127)
#      character formating                      [name,colors,gun attack,anti air,strike,kick,punch,HP,jump strength,speed,dash,grab]
#      jun formtion                             [damage,speed,crash check,decay speed,startup,endlag,colors,y knockback,x knockback,hit stun]
#      anti air format                          [damage,start up,active,endlag,y knockback,x knockback,hitstun,y size,x size]
#      strike formating                         [damage,y speed,x speed,startup,endlag,y bounce,x bounce,y knockback,x knockback,hitstun]
#      nutral formating                         [damage,start up,active,endlag,y knockback,x knockback,hitstun,range]
#      dash format                              [startup,active,endlag,speed]
#      grab format                              [damage,startup,active,endlag-succsess,endlag-whif,y knockback,x knockback,knockdown time]
characters=[['bit man v.1',[blue,darkBlue,red,darkRed,orenge],[2,1,'hi',.002,10,220,[green,darkGreen],.5,.3,10,10],[3,19,7,78,.8,.2,10,50,32,3],[2,.6,.6,15,57,.35,.1,.18,.59,65,5],[3,16,1,5,.9,.9,19,188,3],[1,7,2,5,.55,.43,25,31,7],6.25,1.25,.5,[15,104,6,1.2],[3,37,12,5,62,1.6,1.6,30]],
            ['quin',[grey,grey,blue,darkBlue,black],[1,1.5,'hi',.005,7,150,[blue,darkBlue],1,.5,17,45],[2,25,7,52,1.2,.5,15,35,53,41],[3,1.2,.39,20,80,.25,.6,.24,.7,72,66],[2,15,3,19,.8,1.3,20,198,15],[1,10,4,22,.6,1.5,18,12,20],5.5,1.675,.688,[2,92,4,2.1],[2,26,19,1,106,1.2,1.3,22]],
            ['bit man v.2',[yellow,orenge,orenge,orenge,grey],[3,.6,'hi',.001,10,290,[yellow,orenge],1.2,.8,20,12],[2,15,6,36,.8,.75,12,30,61,21],[2,.8,.5,14,48,.22,.56,.55,.2,61,31],[2,7,5,16,.6,.3,22,205,20],[2,5,6,15,.5,.32,13,52,5],2.75,1.35,.58,[1,132,16,1.35],[2,21,22,3,65,.5,1.0,25]],
            ['BOT MAN',[red,darkRed,grey,grey,darkBlue],[3,.97,'hi',.08,25,462,[darkGreen,darkGreen],1.6,2.4,43,33],[5,46,22,76,.8,2.6,52,52,34,20],[2,1.5,1.95,52,254,.116,.328,.675,.05,63,19],[4,25,2,31,1.8,2.67,35,106,15],[3,15,5,18,.9,2.6,31,25,18],6.25,1.545,.438,[21,122,0,.62],[4,33,4,5,98,.89,2.0,56]],
            ['police',[brown,brown,grey,grey,blue],[2,1.45,'hi',.003,15,426,[darkBlue,darkBlue],1.67,.98,35,22],[3,19,10,97,1.6,.35,41,97,57,52],[2,.25,1.2,5,19,.12,1.1,1.3,.98,18,15],[3,18,3,5,.78,.431,56,98,1],[3,9,4,9,.4,.01,14,23,11],8.75,1.1,.29,[6,103,2,.51],[2,26,19,1,106,1,1.25,102]],
            ['BOT BOY',[darkBlue,darkBlue,grey,grey,red],[5,2.3,'hi',0.0001,9,300,[red,red],.88,.51,56,49],[1,15,7,22,0.9,2.6,9,2,15,3],[3,.5,.75,26,92,1.6,2.1,0.5,1.2,18,15],[4,21,5,13,1.4,1.4,19,22,10],[2,18,4,26,.8,2.6,5,29,5],7.25,1.198,.53,[3,97,2,.97],[1,52,6,15,200,1.5,1,27]],
            ['grunt',[yellow,orenge,tan,tan,lightBlue],[2,1.1,'hi',0.005,13,150,[black,black],.56,.82,35,12],[4,26,8,35,0.9,9.8,13,46,48,44],[2,.67,.67,52,90,1.6,0,.5,1.2,19,18],[3,31,3,15,.8,1.7,6,50,2],[1,5,13,25,.9,1.9,20,10,20],7.5,1.4,.34,[14,52,30,1.6],[6,30,3,1,180,.8,1.3,56]],
            ['porta',[orenge,orenge,yellow,yellow,brown],[2,1.3,'hi',0.01,22,310,[orenge,orenge],.72,.13,51,9],[3,25,3,46,1.6,6.2,19,21,23,19],[1,100,1,100,100,1,1.2,.75,.65,23,15],[4,36,2,116,.97,.77,13,102,11],[2,19,2,31,1,.8,19,15,15],4.25,1.5,.32,[100,1,100,100],[3,25,2,6,202,.5,.96,62]]]
t=0
location=[[550,'man','L',25,0,False,0,450,250,5,characters[0],[0,None],0],[150,'AI','R',25,0,False,0,450,250,5,characters[0],[0,None],0]]
pause=False
inAGame=False
end=False
while True:
    even=None
    defend=False
    if pause:
        windowSurface.fill(blue)
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
                        location=[[550,'man','L',25,0,False,0,450,250,5,characters[0],[0,None],0],[150,'AI','R',25,0,False,0,450,250,5,characters[0],[0,None],0]]
        storyMode=False
    if inAGame and not end and not pause:
        grab=[]
        strike=[]
        antiAir=[]
        normal=[]
        if ti==0:
            location[0][9]=location[0][10][7]*4
            location[1][9]=location[1][10][7]*4
            ti+=1
        atac(location)
        windowSurface.fill(sky)
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
                    at(location[1][10][2],location[1][11],'laser')
                    location[1][8]=0
                    t=0
                    location[1][3]-=1
                    action=True
                elif difficulty==1 and t>=.6 and not location[1][3]==0 and not (location[1][2]==None or location[1][2]=='block')and location[1][8]==250:
                    at(location[1][10][2],location[1][11],'laser')
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
            n[12]-=1
            if n[2]=='block':
                if n[4]>=n[10][7]:
                    n[2]=None
                else:
                    n[4]=n[4]
            elif not n[4]<=0:
                n[4]=n[4]-.035
        for check in lasers:
            for person in location:
                if person[0]>=check[0]-5 and person[0]<=check[0]+5 and not check[3]==person[1] and not person[11][1][0]=='KD-air' and not person[11][1][0]=='KD':
                    laserHit(person,check,die)
                    death=die[0]
                    if death:
                        dead=die[1]
                    lasers.remove(check)
        for check in antiAir:
            for person in location:
                if check[4]=='R':
                    if person[0]<=check[0]+check[3][8] and person[0]>=check[0] and not check[1]==person[1] and not person[11][1][0]=='KD-air' and not person[11][1][0]=='KD':
                        location[0][11][1]=['stun',0,0]
                        location[1][11][1]=['stun',0,0]
                        antiAirHit(person,check,die)
                        death=die[0]
                        if death:
                            dead=die[1]
                        
                else:
                    if person[0]>=check[0]-check[3][8] and person[0]<=check[0] and not check[1]==person[1] and not person[11][1][0]=='KD-air' and not person[11][1][0]=='KD':
                        location[0][11][1]=['stun',0,0]
                        location[1][11][1]=['stun',0,0]
                        antiAirHit(person,check,die)
                        death=die[0]
                        if death:
                            dead=die[1]
        for check in strike:
            for person in location:
                for pernon in location:
                    if check[4]=='L' and not pernon==person:
                        if person[0]<=check[0] and person[0]>=check[0]-50 and not check[1]==person[1] and check[2]+5>person[7] and check[2]-5<person[7] and not person[11][1][0]=='KD-air' and not person[11][1][0]=='KD':
                            if pernon[11][1]==pernon[10][4] and pernon[2]=='L':
                                pernon[11]=[pernon[11][1][4],['stun',-pernon[11][1][6],pernon[11][1][5]]]
                            elif pernon[11][1]==pernon[10][4]:
                                pernon[11]=[pernon[11][1][4],['stun',pernon[11][1][6],pernon[11][1][5]]]
                            strikeHit(person,check,die)
                            death=die[0]
                            if death:
                                dead=die[1]

                    elif not pernon==person:
                        if person[0]>=check[0] and person[0]<=check[0]+50 and not check[1]==person[1] and check[2]+5>person[7] and check[2]-5<person[7] and not person[11][1][0]=='KD-air' and not person[11][1][0]=='KD':
                            if pernon[11][1]==pernon[10][4] and pernon[2]=='R':
                                pernon[11]=[pernon[11][1][4],['stun',pernon[11][1][6],pernon[11][1][5]]]
                            elif pernon[11][1]==pernon[10][4]:
                                pernon[11]=[pernon[11][1][4],['stun',-pernon[11][1][6],pernon[11][1][5]]]
                            strikeHit(person,check,die)
                            death=die[0]
                            if death:
                                dead=die[1]
        for check in normal:
            for person in location:
                if check[4]=='R':
                    if person[0]<=check[0]+check[3][7] and person[0]>=check[0] and not check[1]==person[1] and not person[11][1][0]=='KD-air' and not person[11][1][0]=='KD':
                        location[0][11][1]=['stun',0,0]
                        location[1][11][1]=['stun',0,0]
                        normalHit(person,check,die)
                        death=die[0]
                        if death:
                            dead=die[1]
                        
                else:
                    if person[0]>=check[0]-check[3][7] and person[0]<=check[0] and not check[1]==person[1] and not person[11][1][0]=='KD-air' and not person[11][1][0]=='KD':
                        location[0][11][1]=['stun',0,0]
                        location[1][11][1]=['stun',0,0]
                        normalHit(person,check,die)
                        death=die[0]
                        if death:
                            dead=die[1]
        for check in grab:
            for person in location:
                if check[4]=='R':
                    if person[0]<=check[0]+100 and person[0]>=check[0] and not check[1]==person[1] and not person[11][1][0]=='KD-air' and not person[11][1][0]=='KD':
                        location[0][11][1]=['stun',0,0]
                        if (person[7] <= check[2] and check[2] < person[7]+25):
                            location[0][11][0]=check[3][3]
                            location[1][11][0]=check[3][3]
                        location[1][11][1]=['stun',0,0]
                        grabHit(person,check,die)
                        death=die[0]
                        if death:
                            dead=die[1]
                        
                else:
                    if person[0]>=check[0]-100 and person[0]<=check[0] and not check[1]==person[1] and not person[11][1][0]=='KD-air' and not person[11][1][0]=='KD':
                        location[0][11][1]=['stun',0,0]
                        if (person[7] <= check[2] and check[2] < person[7]+25):
                            location[0][11][0]=check[3][3]
                            location[1][11][0]=check[3][3]
                        location[1][11][1]=['stun',0,0]
                        grabHit(person,check,die)
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
                        if location[0][12]>0 and location[0][7]==450:
                            at(location[0][10][10],location[0][11],'dash')
                    if event.key==K_RIGHT:
                        Lift=True
                        location[0][5]=True
                        location[0][2]='R'
                        if location[0][12]>0 and location[0][7]==450:
                            at(location[0][10][10],location[0][11],'dash')
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
                           at(location[0][10][4],location[0][11],'strike')
                           location[0][5]=False
                    if event.key==K_m and not location[0][2]=='block' and not location[0][3]<=0 and not location[0][2]==None and location[0][11][0]==0:
                        if location[0][5]:
                           at(location[0][10][5],location[0][11],'normal')
                           if location[0][7]==450:
                                location[0][5]=False
                        else:
                            at(location[0][10][6],location[0][11],'normal')
                    if event.key==K_k and not location[0][2]=='block' and not location[0][3]<=0 and not location[0][2]==None and location[0][11][0]==0:
                           at(location[0][10][11],location[0][11],'grab')
                           if location[0][7]==450:
                                location[0][5]=False
                if difficulty=='PvP' and location[1][11][0]==0:
                    if event.key==K_a:
                        location[1][5]=True
                        location[1][2]='L'
                        Lift=True
                        if location[1][12]>0 and location[1][7]==450:
                            at(location[1][10][10],location[1][11],'dash')
                    if event.key==K_d:
                        location[1][5]=True
                        location[1][2]='R'
                        Lift=True
                        if location[1][12]>0 and location[1][7]==450:
                            at(location[1][10][10],location[1][11],'dash')
                    if event.key==K_TAB:
                       if not location[1][2]=='block' and not location[0][2]==None and location[1][11][0]==0:
                           at(location[1][10][2],location[1][11],'laser')
                           #lasers.append([location[1][0],location[1][2],0,'AI',location[1][7]+20]
                           ori[1]=15
                    if event.key==K_1 and location[1][7]==450:
                        if not location[1][2]=='block' and not location[1][3]<=0 and not location[1][2]==None and location[1][11][0]==0 and location[1][7]==450:
                           at(location[1][10][3],location[1][11],'antiAir')
                           location[1][5]=False
                    elif event.key==K_1:
                        if not location[1][2]=='block' and not location[1][2]==None and location[1][11][0]==0:
                           at(location[1][10][4],location[1][11],'strike')
                           location[1][5]=False
                    if event.key==K_2 and not location[1][2]=='block' and not location[1][3]<=0 and not location[1][2]==None and location[1][11][0]==0:
                        if location[1][5]:
                           at(location[1][10][5],location[1][11],'normal')
                           if location[1][7]==450:
                                location[1][5]=False
                        else:
                            at(location[1][10][6],location[1][11],'normal')
                    if event.key==K_w and location[1][7]==450:
                        location[1][6]=location[1][10][8]
                    if event.key==K_s and location[1][4]<=0:
                        location[1][2]='block'
                    if event.key==K_3 and not location[1][2]=='block' and not location[1][3]<=0 and not location[1][2]==None and location[1][11][0]==0:
                           at(location[1][10][11],location[1][11],'grab')
                           if location[1][7]==450:
                                location[1][5]=False
            if event.type==KEYUP:
                if event.key==K_LEFT and location[0][2]=='L' and not Lift:
                    location[0][5]=False
                    location[0][12]=15
                if event.key==K_RIGHT and location[0][2]=='R' and not Lift:
                    location[0][5]=False
                    location[0][12]=15
                if difficulty=='PvP':
                    if event.key==K_a and location[1][2]=='L' and not Lift:
                        location[1][5]=False
                        location[1][12]=15
                    if event.key==K_d and location[1][2]=='R' and not Lift:
                        location[1][5]=False
                        location[1][12]=15
        for movement in location:
            if not movement[11][1]==movement[10][4]:
                if movement[5]:
                    if movement[2]=='L':
                        movement[0]-=movement[10][9]
                    elif movement[2]=='R':
                        movement[0]+=movement[10][9]
                movement[7]-=movement[6]
                movement[6]-=.01
            if movement[7]>=450:
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
        if (not mode=='select') and (not mode=='char1') and (not mode=='char2'):
            if choise==4:
                text=basicFont.render('back',True,black,yellow)
            else:
                text=basicFont.render('back',True,black,white)
            textRect=text.get_rect()
            textRect.centerx=550
            textRect.centery=300
            windowSurface.blit(text,textRect)
        if mode=='char1' or mode=='char2':
            if choise==1:
                text=basicFont.render(characters[0][0],True,blue,yellow)
            else:
                text=basicFont.render(characters[0][0],True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=140
            textRect.centery=320
            windowSurface.blit(text,textRect)
            if choise==2:
                text=basicFont.render(characters[1][0],True,blue,yellow)
            else:
                text=basicFont.render(characters[1][0],True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=280
            textRect.centery=320
            windowSurface.blit(text,textRect)
            if choise==3:
                text=basicFont.render(characters[2][0],True,blue,yellow)
            else:
                text=basicFont.render(characters[2][0],True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=420
            textRect.centery=320
            windowSurface.blit(text,textRect)
            if choise==4:
                text=basicFont.render(characters[3][0],True,blue,yellow)
            else:
                text=basicFont.render(characters[3][0],True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=140
            textRect.centery=370
            windowSurface.blit(text,textRect)
            if choise==5:
                text=basicFont.render(characters[4][0],True,blue,yellow)
            else:
                text=basicFont.render(characters[4][0],True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=280
            textRect.centery=370
            windowSurface.blit(text,textRect)
            if choise==6:
                text=basicFont.render(characters[5][0],True,blue,yellow)
            else:
                text=basicFont.render(characters[5][0],True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=420
            textRect.centery=370
            windowSurface.blit(text,textRect)
            if choise==7:
                text=basicFont.render(characters[6][0],True,blue,yellow)
            else:
                text=basicFont.render(characters[6][0],True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=200
            textRect.centery=420
            windowSurface.blit(text,textRect)
            if choise==7:
                text=basicFont.render(characters[7][0],True,blue,yellow)
            else:
                text=basicFont.render(characters[7][0],True,blue,white)
            textRect=text.get_rect()
            textRect.centerx=300
            textRect.centery=420
            windowSurface.blit(text,textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type==KEYDOWN:
                if not (mode=='char1' or mode=='char2'):
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
                else:
                    if event.key==K_LEFT:
                        if not choise==4 and not choise==1:
                           choise-=1
                    if event.key==K_RIGHT:
                        if not choise==3 and not choise==6:
                            choise+=1
                    if event.key==K_UP:
                        if choise>3:
                            choise-=3
                    if event.key==K_DOWN:
                        if choise<=5:
                            choise+=3
                if event.key==K_RETURN:
                    ti=0
                    if mode=='char1':
                            location[0]=[550,'man','L',25,0,False,0,450,250,characters[0][7],characters[choise-1],[0,None],0]
                            mode='char2'
                            choise=1
                    elif mode=='char2':
                            location[1]=[150,'AI','R',25,0,False,0,450,250,characters[0][7],characters[choise-1],[0,None],0]
                            difficulty='PvP'
                            mode='select'
                            choise=1
                            inAGame=True
                    elif mode=='select':
                        if choise==1:
                            difficulty='PvP'
                            mode='char1'
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
                    location=[[550,'man','L',25,0,False,0,450,250,characters[0][7],characters[random.randint(0,2)],[0,None]],[150,'AI','R',25,0,False,0,450,250,characters[0][7],characters[random.randint(0,2)],[0,None]]]
                    lasers=[]
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    time.sleep(0.002)
