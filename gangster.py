import pygame, sys, bg, random


global gangsterSprite
gangsterSprite= pygame.image.load('assets/gangstersheet.png')
global gangsterDeathSprite
gangsterDeathSprite = pygame.image.load('assets/gangsterdeathsheet.png')

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
    self.hp=50
    self.aware=False
    self.frame=0
    self.facing=Facing.Left
    self.shooting=False
    self.ammos=50
    self.clips=[pygame.Rect(0,0,50,75),pygame.Rect(50,0,50,75),pygame.Rect(100,0,50,75),pygame.Rect(150,0,50,75),pygame.Rect(200,0,50,75)]
    self.deathClips=[pygame.Rect(0,0,80,75),pygame.Rect(80,0,80,75),pygame.Rect(160,0,80,75)]
    self.framesPacer=4
    self.xvelocity=0
    self.yvelocity=0
    self.sprite=sprite
  
  def setXVelocity(self, velocity):
    self.xvelocity+=velocity
    self.rightfacing()

  def rightfacing(self,):
    if (self.xvelocity < 0) and (self.facing != Facing.Left):
      self.facing = Facing.Left
      self.sprite = pygame.transform.flip(self.sprite, True, False)
    elif (self.xvelocity > 0) and (self.facing != Facing.Right):
      self.facing = Facing.Right
      self.sprite = pygame.transform.flip(self.sprite, True, False)

  def setYVelocity(self, velocity):
    self.yvelocity+=velocity

  def ai (self,gang,bg,window):
    turn=random.randint(1,30)
    if turn==1:
      self.xvelocity=5
    if turn==2:
      self.xvelocity=-5
    if turn==3 or turn==4:
      self.xvelocity=0
    if turn>29:
      self.shoot_general(bg,window,self,gang.player)
    self.rightfacing()

  def move(self,background,window,gang):
    #Handle x
    if self.pc==False and self.alive:
      self.ai(gang,background,window)
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
    if background.is_stairs(self.x,self.y):    
      self.y+=self.yvelocity
      if not background.is_stairs(self.x,self.y):
        self.y-=self.yvelocity
    for i in range(10):
      if background.is_falling(self.x,self.y):
        self.y+=1
    return self.x

  def draw(self,window):
    tmpsurface=self.sprite.subsurface(self.clips[(self.frame/self.framesPacer)])
    window.blit(tmpsurface,(self.x,self.y))

  def muzzleFlash_general(self,window,shooter):
    clips = [pygame.Rect(0, 0, 15, 10), pygame.Rect(15, 0, 15, 10)]
    muzzleFlashSprite = pygame.image.load("assets/muzzleflash.png")
    if shooter.facing == Facing.Right:
      muzzleFlashSprite = pygame.transform.flip(muzzleFlashSprite, True, False)
    window.blit(muzzleFlashSprite.subsurface(clips[random.randint(0,1)]), (shooter.x - 10 + (shooter.facing * 60), shooter.y + 33 + random.randint(-1,1)))

  def shoot_general(self,background,window,shooter,shootee):
    if shooter.ammos==0 or not shootee.alive:
      return False
    if (shootee.x>shooter.x and shooter.facing==Facing.Right) or (shootee.x<shooter.x and shooter.facing==Facing.Left):
      shooter.shooting=True
      damage = random.randint(0,4)
      if damage > 2:
        self.muzzleFlash_general(window,shooter)
      shooter.ammos-=1
      shootee.hp-=damage
      background.tinysplatter(shootee.x,shootee.y)
      if shootee.hp<1:
        shootee.die()

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

  def changePlayerCharacter(self,target):
    self.player.die()
    self.player.pc = False
    self.player = target
    target.pc = True
    self.badguys.remove(target)
