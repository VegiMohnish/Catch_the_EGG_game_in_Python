import pygame
from pygame.locals import *
import random
import time
import threading



pygame.init()
clock = pygame.time.Clock()
black=(0,0,0)
bright_green=(0,255,0)
bright_red=(255,50,50)
green=(0,200,0)
red=(200,0,0)
keys=[False,False]
screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN  )
width,height = screen.get_width(),screen.get_height()
player=pygame.image.load("resources/resized_basket.png")
playerpos=[0,height-player.get_height()]
grass=pygame.image.load("resources/resized_grass.png")
egg=pygame.image.load("resources/resized_egg.png")
eggsil=pygame.image.load("resources/resized_eggsil.png")
eggblack=pygame.image.load("resources/resized_eggblack.png")
eggx=[random.randint(0,width-eggsil.get_width()),random.randint(0,width-eggblack.get_width())]
eggy=[-1*random.randint(0,eggsil.get_height()),-1*random.randint(0,eggsil.get_height())]
pause=True
speed=10
speed1=15
r=0

def unpause():
	global pause
	pause=False
def quitgame():
	pygame.quit()
	exit(0)
def button(msg,x,y,w,h,ic,ac,action):
	global screen
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(screen, ac,(x,y,w,h))
		if click[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(screen, ic,(x,y,w,h))
	smallText = pygame.font.SysFont("comicsansms",20)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	screen.blit(textSurf, textRect)
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
		
def update_score_lives(text,count,lives):
	global width
	font = pygame.font.SysFont(None, 50)
	text1 = font.render(text+str(int(count)), True, black)
	screen.blit(text1,(50,50))
	text2 = font.render("Lives: "+str(int(lives)), True, black)
	screen.blit(text2,(width-200,50))
def updatepos(i):
	global eggx,eggy,speed,speed1
	if(i%2==0):
		eggy[i]=eggy[i]+speed
		if(r==5 or r==7):
			screen.blit(egg,(eggx[i],eggy[i]))
		else:
			screen.blit(eggsil,(eggx[i],eggy[i]))
	else:
		eggy[i]=eggy[i]+speed1
		screen.blit(eggblack,(eggx[i],eggy[i]))

def loadbg():
	global width,height,screen
	for x in range(width//grass.get_width()+1):
			for y in range(height//grass.get_height()+1):			
				screen.blit(grass,(x*grass.get_width(),y*grass.get_height()))

def gameloop():
	global eggx,eggy,r,pause,speed,speed1
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
		t0=threading.Thread(target=loadbg(),args=())
		t0.start()
		screen.blit(player,playerpos)
		#update_score_lives(count,lives)
		if(beg==True):
			paused("EGG CATCHER","Start Game",t0,t4,t3)		
			beg=False
			count=5
			while count:
				timer(count)
				
				count=count-1

		if(flagy==1):
			eggx[0]=random.randint(20,width-egg.get_width()-20)
			eggy[0]=-1*random.randint(0,eggsil.get_height()*2)
			eggx[1]=random.randint(20,width-eggsil.get_width()-20)
			eggy[1]=-1*random.randint(0,eggsil.get_height()*2)
			r=random.randint(0,10)
			if(r==5):
				screen.blit(egg,(eggx[0],eggy[0]))
			else:
				screen.blit(eggsil,(eggx[0],eggy[0]))
			flagy=0
		e1=0
		e2=1
		t3 = threading.Thread(target=updatepos, args=(e1,)) 
		t3.start()
		#t3.join()
		t4 = threading.Thread(target=updatepos, args=(e2,)) 
		t4.start()
		#t4.join()

		t2 = threading.Thread(target=update_score_lives, args=("Score: ",count,lives)) 
		t2.start()
		t2.join()
		if(playerpos[0]<eggx[0] and eggx[0]+egg.get_width()<=playerpos[0]+player.get_width()+5 and eggy[0]>=playerpos[1]+player.get_height()//2-egg.get_height() and eggy[0]+egg.get_height()<=playerpos[1]+player.get_height()):
			eggy[0]=10000
			if(r==5):
				count=count+5
			else:
				count=count+1
		if(playerpos[0]<eggx[1] and eggx[1]+eggsil.get_width()<=playerpos[0]+player.get_width()+5 and eggy[1]>=playerpos[1]+player.get_height()//2-eggsil.get_height() and eggy[1]+eggsil.get_height()<=playerpos[1]+player.get_height()):
			eggy[1]=10000
			count=count-5
	
		if(eggy[0]+egg.get_height()>playerpos[1]+player.get_height() and eggy[0]<10000):
			eggy[0]=10000
			lives=lives-1
			if(lives<0):
				lives=0

	
			
		if(count!=0):
			speed=10+count//10
			speed1=13+count//5
			


		if(eggy[0]>=height):
			flagy=1
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
				exit(0)
		if(lives==0):
			pause=True
			paused("Gameover","Restart",t0,t3,t4)		
			gameloop()
		keys=pygame.key.get_pressed()
		if keys[pygame.K_x]:
			t0.join()
			t3.join()
			t4.join()
			pygame.quit()
			exit(0)
		if keys[pygame.K_ESCAPE]:
			pause=True
			paused("PAUSE","Resume",t0,t3,t4)
			temp=3
			while temp:
				timer(temp)
				temp=temp-1
		if keys[pygame.K_LEFT]:
			if playerpos[0]>=30:
				playerpos[0]-=2*speed
		elif keys[pygame.K_RIGHT]:
			if playerpos[0]<=width-30-player.get_width():
				playerpos[0]+=2*speed


	
def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()

def timer(i):
	loadbg()
	largeText = pygame.font.Font('freesansbold.ttf',115)
	TextSurf, TextRect = text_objects("Game Starts in: "+str(i), largeText)
	TextRect.center = ((width//2),(height//2))
	screen.blit(TextSurf, TextRect)
	pygame.display.update()
	time.sleep(1)
	

t1 = threading.Thread(target=gameloop, args=()) 

t1.start()
t1.join()


