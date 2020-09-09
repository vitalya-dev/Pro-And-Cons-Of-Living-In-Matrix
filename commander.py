import os
import pygame
from pygame.locals import *

#================================================================#
SCREEN_SIZE = (640, 480)
#================================================================#


#================================================================#
def clamp(val, min, max):
  if val < min: return min
  if val > max: return max
  return val

def listdir(d, sort):
    dlist = [f for f in os.listdir(d) if os.path.isdir(f)]
    flist = [f for f in os.listdir(d) if os.path.isfile(f)]
    if sort == 'DIRS FIRST':    t_list = dlist + flist
    elif sort == 'FILES FIRST': t_list = flist + dlist
    else:                       t_list = []
    return ['..'] + t_list
#================================================================#



#================================================================#
def button(text):
  btn = pygame.Surface((96, 32))
  btn.fill(pygame.Color('#57ffff'))
  btn.blit(font.render(text, False, pygame.Color('#000000')), (0, 0))
  return btn

def label(text, color):
  return font.render(text, False, color)
#================================================================#



#================================================================#
pygame.init()
pygame.key.set_repeat(10, 75)
#================================================================#


#================================================================#
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
font = pygame.font.Font('data/unispace bd.ttf', 32)
done = False
#================================================================#


#================================================================#
class Pathbar(object):
    def __init__(self):
        self.surface = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()
        self.path = ''

    def render(self):
      self.surface.fill(pygame.Color('#fefe03'))
      self.surface.blit(label(self.path, pygame.Color('#000000')), (16, 0))
      #=================#
      return self.surface

    def process(self, e):
      self.path = os.path.abspath(os.curdir)
      if len(self.path) > 30:
        self.path = ".." + self.path[-28:]

pathbar = Pathbar()
#================================================================#


#================================================================#
class Buttonbar(object):
    def __init__(self):
        self.surface = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()

    def render(self):
      self.surface.fill(pygame.Color('#000000'))
      #=================#
      self.surface.blit(label('X', pygame.Color('#fefe03')), (16 + 8, 0))
      self.surface.blit(button('Help'), (16 + 32, 0))

      self.surface.blit(label('Y', pygame.Color('#fefe03')), (176 + 8, 0))
      self.surface.blit(button('Menu'), (176 + 32, 0))

      self.surface.blit(label('B', pygame.Color('#fefe03')), (336 + 8, 0))
      self.surface.blit(button('Edit'), (336 + 32, 0))

      self.surface.blit(label('A', pygame.Color('#fefe03')), (496 + 8, 0))
      self.surface.blit(button('View'), (496 + 32, 0))
      #=================#
      return self.surface

    def process(self, e):
      pass

buttonbar = Buttonbar()
#================================================================#


#================================================================#
class Fpanel(object):
  def __init__(self):
    self.selection_index = 0
    self.flist = listdir(os.curdir, 'DIRS FIRST')

  def render(self):
    pass

  def process(self, e):
    for e in events:
      if e.type == KEYDOWN and e.key == K_DOWN:
        self.selection_index += 1
      elif e.type == KEYDOWN and e.key == K_UP:
        self.selection_index -= 1
      elif e.type == KEYDOWN and e.key == K_RETURN and os.path.isdir(self.flist[self.selection_index]):
        os.chdir(self.flist[self.selection_index])
        self.flist = listdir(os.curdir, 'DIRS FIRST')
        self.selection_index = 0
    self.selection_index %= len(self.flist)


class SFpanel(Fpanel):
  def __init__(self):
    super().__init__()
    self.scroll_area = [0, 12]
    self.scroll_index = 0
  
  def process(self, e):
    super().process(e)
    self.__scroll()

  def __scroll(self):
    if self.selection_index < self.scroll_area[0]:
      self.scroll_area[0] = self.selection_index
      self.scroll_area[1] = self.scroll_area[0] + 12
    if self.selection_index > self.scroll_area[1]:
      self.scroll_area[1] = self.selection_index
      self.scroll_area[0] = self.scroll_area[1] - 12
    self.scroll_index = self.selection_index - self.scroll_area[0]

class RSFpanel(SFpanel):
  def __init__(self):
    super().__init__()
    self.surface = pygame.surface.Surface((SCREEN_SIZE[0], SCREEN_SIZE[1] - 64)).convert()
    self.selection_bar = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()
    self.selection_bar.fill(pygame.Color('#57ffff'))

  def render(self):
    super().render()
    self.surface.fill(pygame.Color('#0000a8'))

    rlist = self.flist[self.scroll_area[0]:self.scroll_area[1]+1]
    rlist = list(map(lambda d : d + '/' if os.path.isdir(d) else d,  rlist))
    for i, f in enumerate(rlist):
      self.surface.blit(label(f, pygame.Color('#57ffff')), (0, i * 32))

    self.surface.blit(self.selection_bar, (0, self.scroll_index * 32))
    self.surface.blit(label(rlist[self.scroll_index], pygame.Color('#000000')), (0, self.scroll_index * 32))

    return self.surface

fpanel = RSFpanel()
#================================================================#
    
 


#================================================================#
while not done:
  dt = clock.tick(60)
  #PROCESS
  events = pygame.event.get()
  #=================#
  for e in events:
    if e.type == QUIT:
      done = True
    if e.type == KEYDOWN and e.key == K_ESCAPE:
      done = True
  #=================#
  pathbar.process(events)
  fpanel.process(events)
  buttonbar.process(events)
  #RENDER
  screen.fill(pygame.Color('#000000'))
  screen.blit(pathbar.render(), (0, 0))
  screen.blit(fpanel.render(), (0, 32))
  screen.blit(buttonbar.render(), (0, SCREEN_SIZE[1] - 32))
  #UPDATE
  pygame.display.update()
pygame.quit()
quit()
#================================================================#


