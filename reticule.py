import pygame, sys, gangster, random, bg, sound


class reticule:
  def __init__(self, sprite1, sprite2, gang):
    random.seed()
    self.setTarget(gang.badguys[0])
    self.canHeartJump = False
    self.sprite1 = sprite1 #Yes jump
    self.sprite2 = sprite2 #No jump
    self.target=None

  def setTarget(self, newTarget):
    self.target = newTarget

  def draw(self, window, gang):
    if self.target != None:
      if self.heartJumpCheck(gang):
        window.blit(self.sprite1, (self.target.x + 15, self.target.y + 25))
      else:
        window.blit(self.sprite2, (self.target.x + 15, self.target.y + 25))

  def heartJumpCheck(self,gang):
    if self.target==None:
      return False
    facing = (self.target.x>gang.player.x and gang.player.facing==gangster.Facing.Right) or (self.target.x<gang.player.x and gang.player.facing==gangster.Facing.Left)
    closeX = abs(self.target.x - gang.player.x) < 200
    closeY = (gang.player.tier == self.target.tier) or (gang.player.tier != gangster.Tier.Sewer and self.target.tier != gangster.Tier.Sewer)
    self.canHeartJump=closeX and closeY and (facing or not gang.player.alive)
    return self.canHeartJump
        

  def heartJump(self,gang):
    if self.heartJumpCheck(gang):
      sound.nastySquishSound.play()
      sound.boneSquuchSound.play()
      gang.changePlayerCharacter(self.target)
      return True
    return False

  def retargetHelper(self,gang,targets):
    if len(targets) == 0:
        minGuy = self.target
    elif len(targets) == 1:
        minGuy = targets[0]
    else:
      minGuy = targets[0]
      minVal = abs(targets[0].x - self.target.x)
      for g in targets:
        temp = abs(g.x - self.target.x)
        if temp < minVal:
          minVal = temp
          minGuy = g
    self.setTarget(minGuy)
    if self.target==gang.player:
      self.target=None

#in the following functions, filter is cast as a list for compatibility with Pyhton2 and Python3

  #Choose best target left of current
  def moveLeft(self, gang):
    if self.target == None:
      self.target=gang.player
    targets = list(filter(lambda g: ((g.tier == self.target.tier) and (g.x < self.target.x)), gang.badguys))
    self.retargetHelper(gang,targets)
 
  #Choose best target right of current
  def moveRight(self, gang):
    if self.target==None:
      self.target=gang.player
    targets = list(filter(lambda g: ((g.tier == self.target.tier) and (g.x > self.target.x)), gang.badguys))
    self.retargetHelper(gang,targets)

  #If on street or rooftops, choose rooftop target
  def moveUp(self, gang):
    if gang.player.tier != gangster.Tier.Sewer:
      if self.target==None:
        self.target=gang.player
      targets = list(filter(lambda g: ((g.tier == gangster.Tier.Rooftops)), gang.badguys))
      self.retargetHelper(gang,targets)

  #If on street or rooftops, choose street target
  def moveDown(self, gang):
    if gang.player.tier != gangster.Tier.Sewer:
      if self.target==None:
        self.target=gang.player
      targets = list(filter(lambda g: ((g.tier == gangster.Tier.Street)), gang.badguys))
      self.retargetHelper(gang,targets)

  #FINDS BEST TARGET
  #DISREGARDS CURRENT TARGET
  def findTarget(self, gang):
    self.target=gang.player
    targets=list(filter(lambda g: ((g.tier == gang.player.tier)), gang.badguys))
    self.retargetHelper(gang,targets)
    if self.target==None and gang.player.tier != gangster.Tier.Sewer:
      self.target=gang.player
      targets=list(filter(lambda g: ((g.tier != gangster.Tier.Sewer)),gang.badguys))
      self.retargetHelper(gang,targets)

  def shoot(self, gang, background, window):
     if self.target==None or not gang.player.shoot(background, window, self.target):
         self.stop_shooting(gang)
         return False
     else:
         self.makePresenceKnown(gang)
         if self.target.hp<1:
             gang.player.stop_shooting()
             gang.badguys.remove(self.target)
             self.findTarget(gang)
         return True

  def makePresenceKnown(self, gang):
    if gang.player.tier==gangster.Tier.Sewer:
      enemies=filter(lambda g:((g.tier==gangster.Tier.Sewer)),gang.badguys)
    elif gang.player.tier==gangster.Tier.Street:
      enemies=filter(lambda g:((g.tier!=gangster.Tier.Sewer)),gang.badguys)
    elif gang.player.tier==gangster.Tier.Rooftops:
      enemies=filter(lambda g:((g.tier==gangster.Tier.Rooftops)),gang.badguys)
    else:
      enemies=[]
      print ("Someone made a mistake implementing tiers.")
    for jerk in enemies:
      jerk.aware=True

  def stop_shooting(self,gang):
    gang.player.shooting=False
    if gang.player.channel!=None:
      gang.player.channel.fadeout(300)
