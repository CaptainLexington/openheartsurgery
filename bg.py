import pygame, random

class bg:
  def __init__(self,a=[1,1,1,1]):
    random.seed()
    self.image_set=a
    base_image=self.load_image()
    clips=[]
    for i in range(4):
      clips.append(pygame.Rect(self.image_set[i]*200,0,200,600))
    self.screen=pygame.Surface((800,600))
    for i in range(4):
      tmpsurface=base_image.subsurface(clips[i])
      self.screen.blit(tmpsurface,(i*200,0))

  def get_bg(self):
    return self.screen

  def load_image(self):
    return pygame.image.load('assets/level1a.png')

  def is_falling(self,x,y):
    if self.is_stairs(x,y):
      return False
    image=self.image_set[x/200]
    x=x%200
    y=y+70 #Hit with your feet, not with your head
    x=x+25
    if image==0:
      if y<80 or (y>81 and y<370):
        return True
    elif image==1:
      if y<370:
        return True
    elif image==2:
      if y<155 or (y>155 and y<370):
        return True
    elif image==3:
      if y<225 or (y>225 and y<370):
        return True
    elif y>410 and y<570:
      return True
    else:
      return False

  def is_stairs(self,x,y):
    image=self.image_set[x/200]
    x=x%200
    y=y+70 #Hit with your feet, not with your head
    x=x+25
    if image==0:
      if x<70 and y<375 and y>68:
        return True
    if image==1:
      pass
    if image==2:
      pass
    if image==3:
      pass
    return False

  def splatter(self,x,y,blood):
    #put the blood near the character's center
    x+=25
    y+=37
    for i in range(random.randint(3,10)):
      x+=random.randint(0,40)-20
      y+=random.randint(0,40)-20
      self.screen.blit(blood[i%len(blood)],(x,y))
