# -*- coding: utf-8 -*-
# (CC BY-SA) Aija Trimdale
import pygame, sys
from math import*
from time import*
from random import*
from pygame.locals import *
#-----Mainīgo daļa-----
for statuss_info in range(0,1):
	# Statuss
	# 0 -nekas vēl nav saspaidīts, 1.bilde
	# 1 -ir nospiests līmenis, sākam ģenerēt, message
	# 2 -ir uzģenerēts laukums, parādās 2.bilde
	# 3 -ir nospiests sakt spēli, spēles laukums, pati spēle
	# 4 -laukums ir aizpildīts, iespējams, ir kļūdas
	# 5 -spēle beidzas. Fanfaras!
	#12 -instrukcija
	statuss =0

cimage = "/opt/sudokulv/images/"
cfont = "/opt/sudokulv/fonts/font.otf"

#-----Smadzenes!!!-----
sudo = [[0 for row in xrange(9)] for col in xrange(9)] #Ģenerētais laukums, spēlē netiek mainīts
sudo2= [[0 for row in xrange(9)] for col in xrange(9)] #Redzamais  laukums, spēlētājs maina.
sudo3= [[0 for row in xrange(9)] for col in xrange(9)] #Informācijas "slanis" 1-pareizi, 2-kļūda 3-def.lk, 0-tukšs, 4-HINTS
def kubiks(ra,rb,ka,kb):  
	kubs=[1,2,3,4,5,6,7,8,9] #Aizpilda laukumu pa diagonali. Tos 3 kvadrātus. /rinda a(starts), rinda b(beigas). Šī ideja arī tālak.
	for r in xrange(ra,rb):
		for k in xrange(ka,kb):
			var=(len(kubs))-1
			indekss=randint(0,var)
			sudo[r][k]=kubs[indekss]
			del kubs[indekss]
def pilda(kra,krb,kka,kkb): 
	rinda=[] #aizpilda pārējos.
	kolona=[]
	kubs=[]
	for R in xrange(kra,krb): #R-rinda K-kol-kolona, j
		for K in xrange(kka,kkb):
			for k in xrange(0,9):
				rinda.append(sudo[R][k]) #Magic :) Nesaprotu, kādā sakarā, bet šitais strāda. for row in sudo neiet.
			for col in sudo:
				kolona.append(col[K])
			if sudo[R][K]==0:
				for In in xrange(1,10):
					if In not in rinda:
						if In not in kolona:
							if In not in kubs:
								sudo[R][K]=In
								kubs.append(In)
								break
				if sudo[R][K]==0:
					break
			rinda,kolona=[],[]
			if sudo[R][K]==0:
				break
		rinda,kolona=[],[]			
		if sudo[R][K]==0:
			return "halt"
			break
def random_lauki():
	izpilde=0
	while izpilde==0:
		Ran1=randint(0,8)
		Ran2=randint(0,8)
		if sudo2[Ran1][Ran2]==0:
			sudo2[Ran1][Ran2]=sudo[Ran1][Ran2]	
			sudo3[Ran1][Ran2]=3	
			izpilde=100
def generators():
	global sudo
	Generation="y" #ģenerē spēles laukumu	
	while Generation=="y":
		
		Q=[6,9,0,3, 3,6,3,6, 0,3,6,9]
		for i in xrange(0,12,4):
			kubiks(Q[i], Q[i+1],Q[i+2], Q[i+3])
		
		W=[3,6,0,3 ,3,6,6,9, 6,9,3,6, 6,9,6,9, 0,3,0,3, 0,3,3,6]
		for i in xrange(0,24,4):
			Generation= pilda(W[i], W[i+1],W[i+2], W[i+3])
			if Generation=="halt":
				Generation="y"
				break

		for row in sudo:  #ja sudo ir kāda nulle-ģenerē pa jaunu visu laukumu
			if 0 in row:
				Generation="y" #Neiskaidrojamu iemeslu dēļ bez šitā nestrādā.
				sudo=[[0 for row in xrange(9)] for col in xrange(9)]
				break
			else:
				Generation="n"
def kludu_skaititajs():
	global Wrong, kluda, statuss
	Wrong=0 #Ķļūdu skaitītājs
	kluda=[]
	for rowo in range(0,9):
		for colo in range(0,9):
			if sudo3[rowo][colo]==2:
				kluda.append(rowo)
				kluda.append(colo)
				Wrong=1
	if statuss==4 and Wrong==0:
		statuss=5
def tuksumu_skaititajs():
	global statuss, tukss, tuksums
	tukss=[]	
	tuksums=0
	for rowo in range(0,9):
		for colo in range(0,9):
			if sudo3[rowo][colo]==0:
				tukss.append(rowo)
				tukss.append(colo)	
				tuksums=1
	if tuksums==0:
		statuss=4
def refresh(level):
	global statuss,HINTS,start
	statuss=3
	for i in range(0,9):
		for j in range(0,9):
			if sudo3[i][j]!=3:
				sudo3[i][j]=0
				sudo2[i][j]=0
	if level== 30:
		HINTS=5
	elif level ==40:
		HINTS=7
	elif level==50 or level==71:
		HINTS=10
	start=time()
				
#-----Smukuma daļa-----
pygame.init()
window =pygame.display.set_mode((1000, 625), 0, 32 )
ikona  = pygame.image.load(cimage + "icon.png").convert_alpha()
pygame.display.set_icon(ikona)
pygame.display.set_caption("Sudoku")
fonts =pygame.font.Font(cfont, 36)
fonts2=pygame.font.Font(cfont, 46)
for vnk_lai_var_savilk in range(0,1):
	kvadro = pygame.image.load(cimage + "kvadratins.png").convert_alpha()
	z1 = pygame.image.load(cimage + "1z.png").convert_alpha()
	z2 = pygame.image.load(cimage + "2z.png").convert_alpha()
	z3 = pygame.image.load(cimage + "3z.png").convert_alpha()
	z4 = pygame.image.load(cimage + "4z.png").convert_alpha()
	z5 = pygame.image.load(cimage + "5z.png").convert_alpha()
	z6 = pygame.image.load(cimage + "6z.png").convert_alpha()
	z7 = pygame.image.load(cimage + "7z.png").convert_alpha()
	z8 = pygame.image.load(cimage + "8z.png").convert_alpha()
	z9 = pygame.image.load(cimage + "9z.png").convert_alpha()

	m1 = pygame.image.load(cimage + "1m.png").convert_alpha()
	m2 = pygame.image.load(cimage + "2m.png").convert_alpha()
	m3 = pygame.image.load(cimage + "3m.png").convert_alpha()
	m4 = pygame.image.load(cimage + "4m.png").convert_alpha()
	m5 = pygame.image.load(cimage + "5m.png").convert_alpha()
	m6 = pygame.image.load(cimage + "6m.png").convert_alpha()
	m7 = pygame.image.load(cimage + "7m.png").convert_alpha()
	m8 = pygame.image.load(cimage + "8m.png").convert_alpha()
	m9 = pygame.image.load(cimage + "9m.png").convert_alpha()

	fons1 =pygame.image.load(cimage + "fons1.png").convert_alpha()
	fons2 =pygame.image.load(cimage + "fons2.png").convert_alpha()
	fons3 =pygame.image.load(cimage + "fons3.png").convert_alpha()
	fons4 =pygame.image.load(cimage + "fons4.png").convert_alpha()
CIPARI_ZALI =[0,z1,z2,z3,z4,z5,z6,z7,z8,z9]
CIPARI_MELNI=[0,m1,m2,m3,m4,m5,m6,m7,m8,m9]
def zime_zalie():
	for rin in range(0,9):
		for col in range (0,9):
			if sudo3[col][rin]==3 or sudo3[col][rin]==4 :
				cipars=sudo[col][rin]
				bildez=CIPARI_ZALI[cipars]
				XX=round(rin*40 +327,0)
				YY=round(col*40 +120,0)
				window.blit(bildez, (XX,YY))
def zime_melnie():
	for rin in range(0,9):
		for col in range (0,9):
			if sudo3[col][rin]==1 or sudo3[col][rin]==2:
				cipars=sudo2[col][rin]
				bildez=CIPARI_MELNI[cipars]
				XX=round(rin*40 +327,0)
				YY=round(col*40 +120,0)
				window.blit(bildez, (XX,YY))
def laukums():
	global statuss,level,endtime, fonts, fonts2
	
	if statuss ==0:
		window.blit(fons1, (0,0) )
		insta =fonts.render(("Instrukcija"), True, (70,120,10) )
		window.blit(insta,(765,550))
		pygame.display.update()
	elif statuss==1:
		window.blit(fons1, (0,0) )
		message =fonts2.render(("Uzgaidiet"), True, (70,120,10) )
		window.blit(message,(330,500))
		pygame.display.update()
		generators()
		for Randomize in range(0,level):
			random_lauki()
		statuss=2	
	elif statuss ==2 :
		window.blit(fons2, (0,0) )  	
	elif statuss ==3 or statuss==4 or statuss==5:
		window.blit(fons3, (0,0) )
		#laika atskaite
		if statuss!=5:	
			endtime=time()
		sekundes=int(round(endtime - start,0))
		sekundes, minut   = sekundes%60, sekundes//60
		stundas,  minutes = minut//60, minut%60
		
		taimeris =fonts.render(( "Laiks: %.2d:%.2d:%.2d" % (stundas,minutes,sekundes)), True, (0,0,0) )
		window.blit(taimeris,(370, 550))
		#hinti
		hintprints=fonts.render(("Majieni: %.1d" %(HINTS) ), True, (0,0,0) )
		window.blit(hintprints,(370, 500))
		#cipariņi
		zime_zalie()
		zime_melnie()
		
		kludu_skaititajs()
		if statuss==3:	
			tuksumu_skaititajs()
		if statuss==5:
			fonts2=pygame.font.Font(cfont, 46, )
			message =fonts2.render(("Apsveicu!"), True, (70,120,10) )
			window.blit(message,(330,50))
			new =fonts.render(("Jauna"), True, (70,120,10) )
			window.blit(new,(650,50))	
			end =fonts.render(("Iziet"), True, (70,120,10) )
			window.blit(end,(650,80))
			pygame.display.update()
	elif statuss==12:
		window.blit(fons4, (0,0) )
		insta =fonts.render(("Iziet no instrukcijas"), True, (70,120,10) )
		window.blit(insta,(250,550))
		pygame.display.update()
		
#-----Beidzas defi un citi zvēri-----	

while True :
	laukums()
	pygame.display.update()
	PELE=True
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			pygame.quit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			PELE = True
		elif event.type == pygame.MOUSEBUTTONUP:
			PELE = False 
		elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_ESCAPE):
			refresh(level)	
	pele  =pygame.mouse.get_pos()
	pelec =pygame.mouse.get_pressed() #peleclick
	
	if   PELE==False and  (pele[0] >=360 and pele[0]<=640 )  and   (pele[1] >= 275 and pele[1] <=360 )  and statuss ==2:
		statuss =3
		start = time()
	elif PELE==False and  (pele[0] >=650 and pele[0]<=750 )  and   (pele[1] >= 50  and pele[1] <=75  )  and statuss ==5:
		statuss=0
		sudo = [[0 for row in xrange(9)] for col in xrange(9)]
		sudo2= [[0 for row in xrange(9)] for col in xrange(9)] 
		sudo3= [[0 for row in xrange(9)] for col in xrange(9)] 
		PELE=True
	elif PELE==False and  (pele[0] >=650 and pele[0]<=750 )  and   (pele[1] >= 80  and pele[1] <=105 )  and statuss ==5:
		sys.exit()
		pygame.quit()
	elif PELE==False and  (pele[0] >=320 and pele[0]<=630 )  and   (pele[1] >= 270 and pele[1] <=330 )  and statuss ==0:
		statuss=1
		level = 50 #"v"	
		HINTS=10	
	elif PELE==False and  (pele[0] >=320 and pele[0]<=630 )  and   (pele[1] >= 340 and pele[1] <=400 )  and statuss ==0:
		statuss =1
		level= 30 #"g"	
		HINTS=5
	elif PELE==False and  (pele[0] >=320 and pele[0]<=630 )  and   (pele[1] >= 410 and pele[1] <=470 )  and statuss ==0:
		statuss =1
		level=40 #"n"
		HINTS=7
	elif PELE==False and  (pele[0] >=97  and pele[0]<=117 )  and   (pele[1] >= 540 and pele[1] <=550 )  and statuss ==0:
		statuss =1 
		level = 71 # "specialforkalvis"
		HINTS=10
	elif PELE==False and  (pele[0] >=370 and pele[0]<=530 )  and   (pele[1] >=490  and pele[1] <=550 )  and (statuss==3 or statuss==4):
		if HINTS>0:
			HINTS -= 1	
			if Wrong==1:
				RanDo = randrange(0,len(kluda),2)
				XX=kluda[RanDo]
				YY=kluda[RanDo+1]
				sudo2[XX][YY]=sudo[XX][YY]
				sudo3[XX][YY]=4
			elif tuksums!=0:
				RanDo = randrange(0,len(tukss),2)
				XX=tukss[RanDo]
				YY=tukss[RanDo+1]
				sudo2[XX][YY]=sudo[XX][YY]
				sudo3[XX][YY]=4
	elif PELE==False and  (pele[0] >=330 and pele[0]<=680 )  and   (pele[1] >=120  and pele[1] <=470 )  and (statuss==3 or statuss==4):
		PELE=True
		Tesla=0
		while PELE==True and Tesla==0:
			A= int(ceil((pele[1]-120)/40 ))
			B= int(ceil((pele[0]-330)/40 ))
			if sudo3[A][B]==3 or sudo3[A][B]==4:
				Tesla=12
				break
			else:
				C=10
				pygame.display.update()
				XX=int(round(B*39.5 +330,0))
				YY=int(round(A*39.5 +120,0))
				laukums()
				window.blit(kvadro, (XX,YY))
				pygame.display.update()
				
				for event in pygame.event.get():					
					if   event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_KP1) :
						C=1
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_2 or event.key == pygame.K_KP2) :
						C=2
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_3 or event.key == pygame.K_KP3) :
						C=3
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_4 or event.key == pygame.K_KP4) :
						C=4
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_5 or event.key == pygame.K_KP5) :
						C=5
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_6 or event.key == pygame.K_KP6) :
						C=6
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_7 or event.key == pygame.K_KP7) :
						C=7
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_8 or event.key == pygame.K_KP8) :
						C=8
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_9 or event.key == pygame.K_KP9) :
						C=9
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_0 or event.key == pygame.K_KP0) :
						C=0
					elif event.type == pygame.MOUSEBUTTONDOWN:
						PELE = True
					elif event.type == pygame.MOUSEBUTTONUP:
						PELE = False
					elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_ESCAPE):
						refresh(level)
					else:
						laukums()
						window.blit(kvadro, (XX,YY))
						pygame.display.update()
					
				if C>0 and C<10 and PELE==True:
					laukums()
					window.blit(kvadro, (XX,YY))
					pygame.display.update()
					sudo2[A][B]=C
					Tesla=1
					if sudo [A][B]==C:
						sudo3[A][B]=1
					else:
						sudo3[A][B]=2	
				elif PELE==False or ((pele[0] >=370 and pele[0]<=530 )  and   (pele[1] >=490  and pele[1] <=550 )  and (statuss==3 or statuss==4)):
					break
				elif C==0:
					Tesla=1
					sudo2[A][B]=0
					sudo3[A][B]=0
	elif PELE==False and  (pele[0] >=765 and pele[0]<=900 )  and   (pele[1] >=550  and pele[1] <=600 )  and statuss==0:
		statuss=12
	elif PELE==False and  (pele[0] >=250 and pele[0]<=500 )  and   (pele[1] >=550 and pele[1] <=600 )  and statuss==12:	
		statuss=0
