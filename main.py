##imports
import pygame, sys
from pygame.locals import *

aimingReticuleSurfaceObj=None
background=None
windowSurfaceObj=None


##initialization
def init():
  pygame.init()
  global aimingReticuleSurfaceObj
  aimingReticuleSurfaceObj= pygame.image.load('gangster1.png')
  global windowSurfaceObj
  windowSurfaceObj = pygame.display.set_mode((800, 600))
  global background
  background = pygame.image.load('background.png')
  pygame.display.set_caption('Heartless Killer')


##control loop
def game_loop():
  global windowSurfaceObj
  fpsClock=pygame.time.Clock()
  mousex, mousey = 600,200
  while True:
    #windowSurfaceObj.fill(pygame.Color(255,255,255))
    windowSurfaceObj.blit(background,(0,0))
    windowSurfaceObj.blit(aimingReticuleSurfaceObj, (mousex, mousey))
	
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == KEYDOWN:
        #move reticule between enemies
        if event.key == K_UP:
          #move reticule to nearest higher-level thug
          pass
        if event.key == K_DOWN:
          #move reticule to nearest lower-level thug
          pass
        if event.key == K_LEFT:
          #move reticule to nearest thug to the left
          pass
        if event.key == K_RIGHT:
          #move reticule to neartest thug to the right
          pass
        #move left, right, ladders
        if event.key == K_w:
          #climb a ladder up
          pass
        if event.key == K_s:
          #climb a ladder down
          pass
        if event.key == K_a:
          #move left
          pass
        if event.key == K_d:
          #move right
          pass
        #combat 
        if event.key == K_LSHIFT:
          #shoot
          pass
        if event.key == K_SPACE:
	  #heart jump
          pass


  ##Framerate control
    pygame.display.update()
    fpsClock.tick(30)

if __name__=='__main__':
	init()
	game_loop()	
