<<<<<<< HEAD
import pygame, sys, bg


global gangsterSprite
gangsterSprite= pygame.image.load('assets/gangstersheet.png')
=======
import pygame, bg
>>>>>>> 1fb07426b29f282619c56854dc48f79fe37f4e16

class Facing:
  Left, Right, Back = range(3)

class Tier:
  Sewer, Street, Rooftops = range(3)


class gangster:
  def __init__(self,sprite, x = 200, y=300):
    self.pc=False
    self.alive=True
    self.tier=Tier.Street
    self.x=x
    self.y=y
    self.hp=7
    self.aware=False
    self.frame=0
    self.facing=Facing.Left
    self.ammos=100
    self.clips=[pygame.Rect(0,0,50,75),pygame.Rect(50,0,50,75),pygame.Rect(100,0,50,75),pygame.Rect(150,0,50,75),pygame.Rect(200,0,50,75)]
    self.xvelocity=0
    self.yvelocity=0
    self.sprite=sprite
  
  def setXVelocity(self, velocity):
    self.xvelocity+=velocity
    if (velocity != 0):
      if (self.xvelocity < 0) and (self.facing != Facing.Left):
        self.facing = Facing.Left
        self.sprite = pygame.transform.flip(self.sprite, True, False)
      elif (self.xvelocity > 0) and (self.facing != Facing.Right):
        self.facing = Facing.Right
        self.sprite = pygame.transform.flip(self.sprite, True, False)

  def setYVelocity(self, velocity):
    self.yvelocity+=velocity


  def move(self,bg):
    #Handle x
    if (self.xvelocity != 0):
      self.x=self.x+self.xvelocity
      if self.x < 0 or self.x>799:
        self.x-=self.xvelocity
      self.frame+=1
      if self.frame>8:
        self.frame=0
    else:
      if self.facing == Facing.Left:
        self.frame=0
      if self.facing == Facing.Right:
        self.frame=8
    #Handle y
    if bg.is_stairs(self.x,self.y):    
      self.y+=self.yvelocity
      if not bg.is_stairs(self.x,self.y):
        self.y-=self.yvelocity
    for i in range(10):
      if bg.is_falling(self.x,self.y):
        self.y+=1
    return self.x

  def draw(self,window):
    tmpsurface=self.sprite.subsurface(self.clips[self.frame/2])
<<<<<<< HEAD
    window.blit(tmpsurface,(self.move(),(500-self.tier*100)))


class gang:
  def __init__(self):
    self.characters = []
    tempx = 10
    for g in range(5):
      self.characters.append(gangster(gangsterSprite, tempx))
      tempx += 100
    self.characters[0].pc = True
    self.player = filter(lambda g: g.pc, self.characters)[0]
    self.badguys = filter(lambda g: g.alive and not g.pc, self.characters)

  def changePlayerCharacter(targetID):
    self.player.pc = False;
    self.characters[targetID].pc = True;
    self.player = gang[TargetID];
=======
    window.blit(tmpsurface,(self.x,self.y))
>>>>>>> 1fb07426b29f282619c56854dc48f79fe37f4e16
