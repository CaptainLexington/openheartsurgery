import pygame, sys, gangster

class reticule:
  def __init__(self, sprite, gang):
    self.setTarget(gang.badguys[0])
    self.canHeartJump = False
    self.sprite = sprite

  def setTarget(self, newTarget):
    self.target = newTarget
    self.x = newTarget.x

  def draw(self, window):
    window.blit(self.sprite, (self.target.x, 100))

 # def heartJumpCheck(self):
 #   closeX = (self.target.x - gangster.player.x) < 100
 #   closeY = (gangster.player.tier == self.target.tier) or (gangster.player.tier != gangster.Tier.Sewer and self.target.tier != gangster.Tier.Sewer)
 #   if closeX and closeY
        

  def moveLeft(self, gang):
    targets = filter(lambda g: ((g.tier == gang.player.tier) and (g.x < self.target.x)), gang.badguys)
    if len(targets) == 0:
        minGuy = self.target
    elif len(targets) == 1:
        minGuy = targets[0]
    else:
      minGuy = targets[0]
      minVal = targets[0].x - self.target.x
      for g in targets:
        temp = g.x - self.target.x
        if temp < minVal:
          minVal = temp
          minGuy = g
      self.setTarget(minGuy)
 
  def moveRight(self, gang):
    targets = filter(lambda g: ((g.tier == gang.player.tier) and (g.x > self.target.x)), gang.badguys)
    if len(targets) == 0:
        minGuy = self.target
    elif len(targets) == 1:
        minGuy = targets[0]
    else:
      minGuy = targets[0]
      minVal = targets[0].x - self.target.x
      for g in targets:
        temp = g.x - self.target.x
        if temp < minVal:
          minVal = temp
          minGuy = g
      self.setTarget(minGuy)

  def moveUp(self, gang):
    if gang.player.tier == gangster.Tier.Street:
      targets = filter(lambda g: ((g.tier == gangster.Tier.Rooftops)), gang.badguys)
      if len(targets) == 0:
        minGuy = self.target
      elif len(targets) == 1:
        minGuy = targets[0]
      else:
        minGuy = targets[0]
        minVal = targets[0].x - self.target.x
        for g in targets:
          temp = g.x - self.target.x
          if temp < minVal:
            minVal = temp
            minGuy = g
      self.setTarget(minGuy)

  def moveDown(self, gang):
    if gang.player.tier == gangster.Tier.Rooftops:
      targets = filter(lambda g: ((g.tier == gangster.Tier.Street)), gang.badguys)
      if len(targets) == 0:
        minGuy = self.target
      elif len(targets) == 1:
        minGuy = targets[0]
      else:
        minGuy = targets[0]
        minVal = targets[0].x - self.target.x
        for g in targets:
          temp = g.x - self.target.x
          if temp < minVal:
            minVal = temp
            minGuy = g
      self.setTarget(minGuy)
 
 

