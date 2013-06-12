import pygame, sys, bg, random, sound


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
    self.channel=None
  
  def setXVelocity(self, velocity):
    self.xvelocity+=velocity
    if self.alive:
        self.rightfacing()

  def rightfacing(self,):
    if (self.xvelocity < 0) and (self.facing != Facing.Left):
      self.facing = Facing.Left
      self.sprite = pygame.transform.flip(self.sprite, True, False)
    elif (self.xvelocity > 0) and (self.facing != Facing.Right):
      self.facing = Facing.Right
      self.sprite = pygame.transform.flip(self.sprite, True, False)

  def can_affect(self,otherguy):
     if self.tier==Tier.Sewer:
       if otherguy.tier!=Tier.Sewer:
         return False
     elif otherguy.tier==Tier.Sewer:
       return False
     return True

  def setYVelocity(self, velocity):
    self.yvelocity+=velocity

  def ai (self,gang,bg,window):
    self.notice(gang.player)
    if self.aware:
      if self.shooting:
        self.xvelocity=0
      self.shoot(bg,window,gang.player)
    if not self.aware or not self.shooting:
      turn=random.randint(1,30)
      if turn==1:
        self.xvelocity=3
      if turn==2:
        self.xvelocity=-3
      if turn==3 or turn==4:
        self.xvelocity=0
      self.rightfacing()

  def move(self,background,window,gang):
    #Handle x
    if self.pc==False and self.alive:
      self.ai(gang,background,window)
    if (self.xvelocity != 0 and self.alive):
      self.x=self.x+self.xvelocity
      if self.x < 0 or self.x>760:
        self.x-=self.xvelocity
      elif self.pc==False and background.is_falling(self.x,self.y):
        self.x-=self.xvelocity
      self.frame+=1
      if self.frame>16:
        self.frame=0
    elif self.alive:
      if self.facing == Facing.Left:
        self.frame=0
      if self.facing == Facing.Right:
        self.frame=16
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
    tmpsurface=self.sprite.subsurface(self.clips[(self.frame//self.framesPacer)])
    window.blit(tmpsurface,(self.x,self.y))

  def muzzleFlash(self,window):
    clips = [pygame.Rect(0, 0, 15, 10), pygame.Rect(15, 0, 15, 10)]
    muzzleFlashSprite = pygame.image.load("assets/muzzleflash.png")
    if self.facing == Facing.Right:
      muzzleFlashSprite = pygame.transform.flip(muzzleFlashSprite, True, False)
    window.blit(muzzleFlashSprite.subsurface(clips[random.randint(0,1)]), (self.x - 10 + (self.facing * 60), self.y + 33 + random.randint(-1,1)))

  def shoot(self,background,window,shootee):
    if self.ammos==0 or not shootee.alive or not self.can_affect(shootee):
      self.stop_shooting()
      return False
    if (shootee.x>self.x and self.facing==Facing.Right) or (shootee.x<self.x and self.facing==Facing.Left):
      if self.shooting==False:
        self.shooting=True
        self.channel=sound.machineGunSound.play()
      damage = random.randint(0,4)
      if damage > 2:
        self.muzzleFlash(window)
      self.ammos-=1
      shootee.hp-=damage
      background.tinysplatter(shootee.x,shootee.y)
      if shootee.hp<1:
        shootee.die()
        if self.channel!=None:
          self.channel.queue(sound.failSplatSound)
    return True

  def stop_shooting(self):
    self.shooting=False
    if self.channel!=None:
      self.channel.fadeout(300)

  def notice (self,player):
    if self.tier==player.tier and abs(self.x-player.x)<75:
      self.aware=True

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
    sound.bodyThumpSound.play()
    if self.facing == Facing.Right:
      self.sprite = pygame.transform.flip(self.sprite, True, False)
      self.frame = 30


class gang:
  def __init__(self, numberOfGangsters, cfg):
    self.characters = []
    for g in range(numberOfGangsters):
      xy = cfg.readline().split()
      self.characters.append(gangster(gangsterSprite, int(xy[0]), int(xy[1])))
    self.characters[0].pc = True
    self.player = list(filter(lambda g: g.pc, self.characters))[0] #python2 and python3 compatibility
    self.badguys = list(filter(lambda g: g.alive and not g.pc, self.characters))
    self.heartFrame = 0
    self.heartAirborne = False
    self.heartX = self.player.x + 28 - (15 * self.player.facing)
    self.heartY = self.player.y + 23
    self.heartTarget = None
    self.heartStep = 0

  def changePlayerCharacter(self,target):
    xvel=self.player.xvelocity
    yvel=self.player.yvelocity
    if (self.player.alive):
        self.player.die()
    self.player.pc = False
    self.player = target
    self.player.pc = True
    self.player.stop_shooting()
    self.heartTarget = self.player
    self.heartStepX = (self.heartTarget.x - self.heartX)/10
    self.heartStepY = (self.heartTarget.y - self.heartY)/10
    self.heartAirborne = True
    self.player.xvelocity = xvel
    self.player.yvelocity = yvel
    self.badguys.remove(target)

  def drawHeart(self, window):
    clips = [pygame.Rect(0,0,10,20), pygame.Rect(10,0,10,20), pygame.Rect(20,0,10,20), pygame.Rect(30,0,10,20)]
    self.heartFrame += 1
    if self.heartFrame > 30:
      self.heartFrame = 0
    if not self.heartAirborne:
      self.heartX = self.player.x + 28 - (15 * self.player.facing)
      if self.player.alive:
          self.heartY = self.player.y + 23
      else:
          self.heartY = self.player.y + 50
      tmpsurface = heartSprite.subsurface(clips[self.heartFrame//15])
      window.blit(tmpsurface, (self.heartX, self.heartY))
    else:
      #If we're almost there
      closeX = False
      closeY = False 
      if abs(self.heartX-self.heartTarget.x)<abs(self.heartX+self.heartStepX-self.heartTarget.x):
          self.heartX=self.heartTarget.x
      else:
          self.heartX += self.heartStepX
      if abs(self.heartY-self.heartTarget.y)<abs(self.heartY+self.heartStepY-self.heartTarget.y):
          self.heartY=self.heartTarget.y
      else:
          self.heartY += self.heartStepY

      #If we're there
      if self.heartX==self.heartTarget.x and self.heartY==self.heartTarget.y:
          self.heartAirborne = False
          sound.wetSplatSound.play()
          self.heartTarget.xvelocity = 0
          self.heartTarget.yvelocity = 0
      tmpsurface = heartSprite.subsurface(clips[(self.heartFrame//15)+1])
      window.blit(tmpsurface, (self.heartX, self.heartY))

