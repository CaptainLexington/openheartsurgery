import pygame

class gangster:
  def __init__(self,sprite):
    self.pc=False
    self.alive=True
    self.tier=0
    self.x=0
    self.hp=7
    self.aware=False
    self.frame=0
    self.facing=0
    self.ammos=100
    self.clips=[pygame.Rect(0,0,50,75),pygame.Rect(50,0,50,75),pygame.Rect(100,0,50,75),pygame.Rect(150,0,50,75)]
    self.velocity=0
    self.sprite=sprite
  
  def setVelocity(self, velocity):
    self.velocity = velocity

  def move(self):
    if (self.velocity != 0):
      self.x=self.x+self.velocity
      self.frame+=1
      if self.frame>6:
        self.frame=0
    return self.x

  def draw(self,window):
    tmpsurface=self.sprite.subsurface(self.clips[self.frame/2])
    window.blit(tmpsurface,(self.move(),(500-self.tier*100)))
