import pygame
from pygame.locals import *
import random
import time
import threading
import gc
from pygame import mixer

#threading

sem = threading.Semaphore()
mutex = threading.Semaphore()

pygame.init()                       # initialize all imported pygame modules

pygame.mixer.init()                 # initialize the mixer module

#pygame.event.wait()
clock = pygame.time.Clock()         # create an object to help track time

# RGB Values for different colors

black=(0,0,0)
gold=(255,215,0)
light_gold=(218,165,32)
blue=(0,0,255)
bright_blue=(0,0,128)
bright_green=(0,255,0)
bright_red=(255,50,50)
green=(0,200,0)
red=(200,0,0)
keys=[False,False]

screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN )    # Initialize a window or screen for display
width,height = screen.get_width(),screen.get_height()

player1=pygame.image.load("resources/resized_basket.png")   # load new image from a file
player2=pygame.image.load("resources/resized_maxresdefault.jpg")
player=player1
playerpos=[0,height-player.get_height()]
grass=pygame.image.load("resources/resized_maxresdefault.jpg")
egg=pygame.image.load("resources/resized_egg.png")
eggsil=pygame.image.load("resources/resized_eggsil.png")
eggblack=pygame.image.load("resources/resized_eggblack.png")
eggx=[random.randint(0,width-eggsil.get_width()),random.randint(0,width-eggblack.get_width())]
eggy=[-1*random.randint(0,eggsil.get_height()),-1*random.randint(0,eggsil.get_height())]

high=0
pause=True
speed=0
speed1=0
beg=True
r=0
mode=-1
c=10
d=13


def unpause():
    global pause
    pause=False


def easy():
    global c,d,speed,speed1,mode,grass
    grass=pygame.image.load("resources/resized_grass.png")
    mode=0
    c=5
    d=7
    speed=c
    speed1=d
    unpause()

def med():
    global speed1,speed,c,d,mode,grass
    grass=pygame.image.load("resources/mnn.jpg")
    mode=1
    c=9
    d=12
    speed=c
    speed1=d
    unpause()

def hard():
    global speed,speed1,c,d,mode,grass
    grass=pygame.image.load("resources/gf.jpg")
    mode=2
    c=13
    d=15
    speed=c
    speed1=d
    unpause()

def quitgame():
    pygame.quit()                    # uninitialize all pygame modules
    exit(0)

def button(msg,x,y,w,h,ic,ac,action):
    global screen
    mouse = pygame.mouse.get_pos()        # get the mouse cursor position
    click = pygame.mouse.get_pressed()    # get the state of the mouse buttons

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))        # draw rectangle

        if click[0] == 1 and action != None:
            pygame.draw.rect(screen, ac,(x,y,w,h))
            action()
            pygame.mixer.music.load("/home/mohnish/newegg/resources/"+"dt.wav")       # Load a music file for playback
            pygame.mixer.music.play()         # Start the playback of the music stream

    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)                 # draw one image on another


def mod(text,text1,text2,text3,t2,t3,t0):
    mutex.acquire()

    global width,height,screen,pause
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((width//2),(height//2))
    screen.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t2.join()
                t3.join()
                t0.join()
                pygame.quit()
                quit()

        button(text1,(width//2)-300,(height//2)+100,100,50,green,bright_green,easy)
        button(text2,(width//2)-150,(height//2)+100,100,50,blue,bright_blue,med)
        button(text3,(width//2),(height//2)+100,100,50,gold,light_gold,hard)
        button("Quit",(width//2)+150,(height//2)+100,100,50,red,bright_red,quitgame)
        

        pygame.display.update()
    mutex.release()


def paused(text,text1,t2,t3,t0):

    global width,height,screen,pause
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((width//2),(height//2))
    screen.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t2.join()
                t3.join()
                t0.join()
                pygame.quit()
                quit()

        button(text1,(width//2)-150,(height//2)+100,100,50,green,bright_green,unpause)
        button("Quit",(width//2)+50,(height//2)+100,100,50,red,bright_red,quitgame)
        
        pygame.display.update()

        
def update_score_lives(text,count,lives,high):
    global width

    font = pygame.font.SysFont(None, 50)
    text1 = font.render(text+str(int(count)), True, black)
    screen.blit(text1,(50,50))
    text2 = font.render("Lives: "+str(int(lives)), True, black)
    screen.blit(text2,(width-200,50))
   # print(high)
    text3 = font.render("HIGH SCORE: "+str(int(high)), True, black)
    screen.blit(text3,(width//2,50))

def updatepos(i):
    global eggx,eggy,speed,speed1
    if(i%2==0):
        sem.acquire()
        eggy[i]=eggy[i]+speed
        sem.release()
        #blt(i)
    else:
        eggy[i]=eggy[i]+speed1
        screen.blit(eggblack,(eggx[i],eggy[i]))
        
def blt(i):
    sem.acquire()
    if(r==5 or r==7):
        screen.blit(egg,(eggx[i],eggy[i]))
    else:
        screen.blit(eggsil,(eggx[i],eggy[i]))
    sem.release()


def loadbg(grass):
    mutex.acquire()
    global width,height,screen
    for x in range(width//grass.get_width()+1):
            for y in range(height//grass.get_height()+1):           
                screen.blit(grass,(x*grass.get_width(),y*grass.get_height()))
    mutex.release()


def gameloop():
    global eggx,eggy,r,pause,speed,speed1,high,score_file,player,beg,c,d,mode,grass
    screen.fill(0)  
    flagy=1
    beg=True
    
    count=0
    lives=3

    t3 = threading.Thread(target=updatepos, args=(0,)) 
    t3.start()
    t4 = threading.Thread(target=updatepos, args=(1,)) 
    t4.start()

    while 1:

        t0=threading.Thread(target=loadbg(grass),args=(grass))
        t0.start()
        screen.blit(player,playerpos)
        #update_score_lives(count,lives)

        if(beg==True):
            mod("EGG CATCHER","EASY","NORMAL","HARD",t0,t4,t3)      
            beg=False
            count=5
            if(mode==0):
                               
                score_file=open('resources/easyhighscore.txt','br')
            elif(mode==1):
                score_file=open('resources/medhighscore.txt','br')
            elif(mode==2):
                score_file=open('resources/hardhighscore.txt','br')
            high=(score_file.read(1))
            result=0

            #print(high)
            for b in high:
                result = result * 256 + int(b)
            high=result
            prevhigh=high
            while count:
                timer(count,grass)
                #mutex.acquire()
                count=count-1
                #mutex.release()s
        #print(speed)

        if(flagy==1):
            #mutex.acquire()
            eggx[0]=random.randint(20,width-egg.get_width()-20)
            eggy[0]=-1*random.randint(0,eggsil.get_height()*2)
            eggx[1]=random.randint(20,width-eggsil.get_width()-20)
            eggy[1]=-1*random.randint(0,eggsil.get_height()*2)
            r=random.randint(0,10)

            if(r==5 or r==7):
                screen.blit(egg,(eggx[0],eggy[0]))
            else:
                screen.blit(eggsil,(eggx[0],eggy[0]))
            flagy=0

        e1=0
        e2=1

        t3 = threading.Thread(target=updatepos, args=(e1,)) 
        t3.start()
        t9 = threading.Thread(target=blt,args=(e1,))
        t9.start()
        #t3.join()
        t4 = threading.Thread(target=updatepos, args=(e2,)) 
        t4.start()
        #t4.join()
        t2 = threading.Thread(target=update_score_lives, args=("Score: ",count,lives,high)) 
        t2.start()
        t2.join()

        if(playerpos[0]<eggx[0] and eggx[0]+egg.get_width()<=playerpos[0]+player.get_width()+5 and eggy[0]>=playerpos[1]+player.get_height()//2-egg.get_height() and eggy[0]+egg.get_height()<=playerpos[1]+player.get_height()):
            eggy[0]=10000
            #mutex.acquire()

            if(r==5 or r==7):
                count=count+5
                pygame.mixer.music.load("/home/mohnish/newegg/resources/"+"bon.wav")
                pygame.mixer.music.play()
            else:
                count=count+1
                pygame.mixer.music.load("/home/mohnish/newegg/resources/"+"button.mp3")
                pygame.mixer.music.play()
            #mutex.release()

        if(playerpos[0]<eggx[1] and eggx[1]+eggsil.get_width()<=playerpos[0]+player.get_width()+5 and eggy[1]>=playerpos[1]+player.get_height()//2-eggsil.get_height() and eggy[1]+eggsil.get_height()<=playerpos[1]+player.get_height()):
            eggy[1]=10000
            #mutex.acquire()
            count=count-5
            pygame.mixer.music.load("/home/mohnish/newegg/resources/"+"bps.mp3")
            pygame.mixer.music.play()
            #mutex.release()

        if(count>high):
            high=count
        if(eggy[0]+egg.get_height()>playerpos[1]+player.get_height() and eggy[0]<10000):
            eggy[0]=10000
            lives=lives-1
            if(lives<0):
                lives=0

    
            
        if(count!=0):
            speed=c+count//10
            speed1=d+count//5
            


        if(eggy[0]>=height):
            flagy=1
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)

        if(lives==0):
            pygame.mixer.music.load("/home/mohnish/newegg/resources/"+"st.wav")
            pygame.mixer.music.play()
            pause=True
            score_file.close()

            if(high>prevhigh):
                if(mode==0):
                    score_file=open('resources/easyhighscore.txt','bw')
                elif(mode==1):
                    score_file=open('resources/medhighscore.txt','bw')
                elif(mode==2):
                    score_file=open('resources/hardhighscore.txt','bw')
                score_file.write(bytes([high]))
                score_file.close()

            paused("Gameover","Restart",t0,t3,t4)
            gc.collect()
      
            gameloop()
        keys=pygame.key.get_pressed()

        if keys[pygame.K_x]:
            t0.join()
            t3.join()
            t4.join()
            pygame.quit()
            exit(0)

        if keys[pygame.K_SPACE]:
            pause=True
            paused("PAUSE","Resume",t0,t3,t4)
            temp=3
            while temp:
                timer(temp,grass)
                temp=temp-1

        if keys[pygame.K_LEFT]:
            if playerpos[0]>=10:
                playerpos[0]-=2*speed
        elif keys[pygame.K_RIGHT]:
            if playerpos[0]<=width-10-player.get_width():
                playerpos[0]+=2*speed


    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def timer(i,grass):
    loadbg(grass)
    largeText = pygame.font.Font('freesansbold.ttf',115)               # create a new Font object from a file
    TextSurf, TextRect = text_objects("Game Starts in: "+str(i), largeText)
    TextRect.center = ((width//2),(height//2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()              # Update portions of the screen for software displays
    time.sleep(1)                        # Number of seconds for which the code is required to be stopped.
    

t1 = threading.Thread(target=gameloop, args=()) 

t1.start()
t1.join()


