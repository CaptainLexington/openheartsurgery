import pygame

class Facing:
  Left, Right, Back = range(3)

class Tier:
  Sewer, Street, Rooftops = range(3)


class gangster:
  def __init__(self,sprite, x = 200):
    self.pc=False
    self.alive=True
    self.tier=Tier.Street
    self.x=x
    self.hp=7
    self.aware=False
    self.frame=0
    self.facing=Facing.Left
    self.ammos=100
    self.clips=[pygame.Rect(0,0,50,75),pygame.Rect(50,0,50,75),pygame.Rect(100,0,50,75),pygame.Rect(150,0,50,75)]
    self.velocity=0
    self.sprite=sprite
  
  def setVelocity(self, velocity):
    self.velocity+=velocity
    if (velocity != 0):
      if (self.velocity < 0) and (self.facing != Facing.Left):
        self.facing = Facing.Left
        self.sprite = pygame.transform.flip(self.sprite, True, False)
      elif (self.velocity > 0) and (self.facing != Facing.Right):
        self.facing = Facing.Right
        self.sprite = pygame.transform.flip(self.sprite, True, False)

  def move(self):
    if (self.velocity != 0):
      self.x=self.x+self.velocity
      self.frame+=1
      if self.frame>6:
        self.frame=0
    else:
      self.frame=0
    return self.x

  def draw(self,window):
    tmpsurface=self.sprite.subsurface(self.clips[self.frame/2])
    window.blit(tmpsurface,(self.move(),(500-self.tier*100)))
