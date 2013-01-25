##imports
import pygame, sys
from pygame.locals import *

##initialization
pygame.init()
fps = pygame.time.Clock()
aimingReticuleSurfaceObj = pygame.image.load('reticule.png')
windowSurfaceObj = pygame.display.set_mode((800, 600))
pygame.display.set('Heartless Killer')
mousex, mousey = 0, 0


##control loop
while True:
  windowSurfaceObj.fill(whiteColor)
  windowSurfaceObj.blit(aimingReticuleSurfaceObj, (mousex, mousey))
	
  for event in pygame.event.get():
    if event.type == QUIT():
      pygame.quit()
      sys.exit()
    elif event.type == KEYDOWN:
     ## move reticule between enemies
      if event.key == K_UP:
        ##move reticule to nearest higher-level thug
      if event.key == K_DOWN:
        ##move reticule to nearest lower-level thug
      if event.key == K_LEFT:
        ##move reticule to nearest thug to the left
      if event.key == K_RIGHT:
        ##move reticule to neartest thug to the right
     ## move left, right, ladders
      if event.key == K_w:
        ##climb a ladder up
      if event.key == K_s:
        ##climb a ladder down
      if event.key == K_a:
        ##move left
      if event.key == K_d:
        ##move right
     ##combat 
      if event.key == K_LSHIFT:
        ##shoot
      if event.key == K_SPACE:
	##heart jump

