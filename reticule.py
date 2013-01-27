import pygame, sys, gangster, random, bg

#global muzzleFlashSprite

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
    closeX = abs(self.target.x - gang.player.x) < 100
    closeY = (gang.player.tier == self.target.tier) or (gang.player.tier != gangster.Tier.Sewer and self.target.tier != gangster.Tier.Sewer)
    self.canHeartJump=closeX and closeY
    return self.canHeartJump
        

  def heartJump(self,gang):
    if self.heartJumpCheck(gang):
      gang.changePlayerCharacter(self.target)
      return True
    return False

  def moveHelper(self,gang,targets):
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

  def moveLeft(self, gang):
    if self.target == None:
      self.target=gang.player
    targets = filter(lambda g: ((g.tier == gang.player.tier) and (g.x < self.target.x)), gang.badguys)
    self.moveHelper(gang,targets)
 
  def moveRight(self, gang):
    if self.target==None:
      self.target=gang.player
    targets = filter(lambda g: ((g.tier == gang.player.tier) and (g.x > self.target.x)), gang.badguys)
    self.moveHelper(gang,targets)


  def moveUp(self, gang):
    if gang.player.tier != gangster.Tier.Sewer:
      if self.target==None:
        self.target=gang.player
      targets = filter(lambda g: ((g.tier == gangster.Tier.Rooftops)), gang.badguys)
      self.moveHelper(gang,targets)

  def moveDown(self, gang):
    if gang.player.tier != gangster.Tier.Sewer:
      if self.target==None:
        self.target=gang.player
      targets = filter(lambda g: ((g.tier == gangster.Tier.Street)), gang.badguys)
      self.moveHelper(gang,targets)

  #FINDS BEST TARGET
  #DISREGARDS CURRENT TARGET
  def findTarget(self, gang):
    self.target=gang.player
    targets=filter(lambda g: ((g.tier == gang.player.tier)), gang.badguys)
    self.moveHelper(gang,targets)
    if self.target==None and gang.player.tier != gangster.Tier.Sewer:
      targets=filter(lambda g: ((g.tier != gangster.Tier.Sewer)),gang.badguys)
      self.moveHelper(gang,targets)

  def muzzleFlash(self, gang, window):
    clips = [pygame.Rect(0, 0, 15, 10), pygame.Rect(15, 0, 15, 10)]
    muzzleFlashSprite = pygame.image.load("assets/muzzleflash.png")
    if gang.player.facing == gangster.Facing.Right:
      muzzleFlashSprite = pygame.transform.flip(muzzleFlashSprite, True, False)
    window.blit(muzzleFlashSprite.subsurface(clips[random.randint(0,1)]), (gang.player.x - 10 + (gang.player.facing * 60), gang.player.y + 33 + random.randint(-1,1)))
    
  def shoot(self, gang, background):
    if self.target==None or gang.player.ammos==0:
	return False
    gang.player.shooting=True
    damage = random.randint(0,4)
    gang.player.ammos-=1
    if (self.target.x>gang.player.x and gang.player.facing==gangster.Facing.Right) or (self.target.x<gang.player.x and gang.player.facing==gangster.Facing.Left):
      self.target.hp-=damage
      background.tinysplatter(self.target.x,self.target.y)
      if self.target.hp<1:
        self.target.die()
        gang.badguys.remove(self.target)
        self.findTarget(gang)

  def stop_shooting(self,gang):
    gang.player.shooting=False
    
