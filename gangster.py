import pygame, sys, bg


global gangsterSprite
gangsterSprite= pygame.image.load('assets/gangstersheet.png')
global gangsterDeathSprite
gangsterDeathSprite = pygame.image.load('assets/gangsterdeathsheet.png')
global heartSprite
heartSprite = pygame.image.load('assets/heart.png')

class Facing:
  Left, Right, Back = range(3)

class Tier:
  Sewer, Street, Rooftops = range(3)


class gangster:
  def __init__(self,sprite, x = 200, y=300):
    self.pc=False
    self.alive=True
    #self.dying=False
    self.tier=Tier.Street
    self.x=x
    self.y=y
    self.hp=100
    self.aware=False
    self.frame=0
    self.facing=Facing.Left
    self.shooting=False
    self.ammos=100
    self.clips=[pygame.Rect(0,0,50,75),pygame.Rect(50,0,50,75),pygame.Rect(100,0,50,75),pygame.Rect(150,0,50,75),pygame.Rect(200,0,50,75)]
    self.deathClips=[pygame.Rect(0,0,80,75),pygame.Rect(80,0,80,75),pygame.Rect(160,0,80,75)]
    self.framesPacer=4
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
      if self.frame>16:
        self.frame=0
    elif self.alive:
      if self.facing == Facing.Left:
        self.frame=0
      if self.facing == Facing.Right:
        self.frame=8
    elif self.facing == Facing.Left:
      self.frame+=1
      if self.frame > 20:
        self.frame = 20
    else:
      self.frame-=1
      if self.frame < 0:
       self.frame = 0
       # self.dying = False
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
    tmpsurface=self.sprite.subsurface(self.clips[(self.frame/self.framesPacer)])
    window.blit(tmpsurface,(self.x,self.y))

  def die (self):
    self.xvelocity=0
    self.xvelocity=0
    self.sprite=gangsterDeathSprite
    self.clips = self.deathClips
    self.framesPacer=10
    self.alive = False
    #self.dying = True
    self.frame = 0
    self.x = self.x - 30 + (self.facing * 30) 
    if self.facing == Facing.Right:
      self.sprite = pygame.transform.flip(self.sprite, True, False)
      self.frame = 30


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
    self.heartFrame = 0
    self.heartAirborne = False
    self.heartX = self.player.x + 28 - (15 * self.player.facing)
    self.heartY = self.player.y + 23
    self.heartTarget = None
    self.heartStep = 0

  def changePlayerCharacter(self,target):
    self.player.die()
    self.player.pc = False
    self.player = target
    target.pc = True
    self.heartTarget = target
    self.heartStep = (self.heartTarget.x - self.heartX)/10
    self.heartAirborne = True
    self.player.velocity = 0
    self.badguys.remove(target)

  def drawHeart(self, window):
    clips = [pygame.Rect(0,0,10,20), pygame.Rect(10,0,10,20), pygame.Rect(20,0,10,20), pygame.Rect(30,0,10,20)]
    self.heartFrame += 1
    if self.heartFrame > 30:
      self.heartFrame = 0
    if not self.heartAirborne:
      self.heartX = self.player.x + 28 - (15 * self.player.facing)
      self.heartY = self.player.y + 23
      tmpsurface = heartSprite.subsurface(clips[self.heartFrame/15])
      window.blit(tmpsurface, (self.heartX, self.heartY))
    else:
      self.heartX += self.heartStep
      if abs(self.heartTarget.x - self.heartX) < abs(self.heartStep):
          self.heartAirborne = False
      tmpsurface = heartSprite.subsurface(clips[(self.heartFrame/15)+1])
      window.blit(tmpsurface, (self.heartX, self.heartY))

