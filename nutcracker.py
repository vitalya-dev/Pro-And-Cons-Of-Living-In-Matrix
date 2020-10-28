import pygame
from pygame.locals import *


#================================================================#
SCREEN_SIZE = (640, 480)
FONT_SIZE   = 32
#================================================================#


#================================================================#
pygame.init()
#================================================================#

#================================================================#
screen     = pygame.display.set_mode(SCREEN_SIZE)
clock      = pygame.time.Clock()
font       = pygame.font.Font('data/FSEX300.ttf', FONT_SIZE - 1)
#================================================================#

#================================================================#
def done(val=None):
  if not hasattr(done, 'val'): done.val = False
  if val == None: return done.val
  done.val = val;

def scale(l, x):
  if type(l) == type(tuple()):
    return tuple(map(lambda e: e * x, l))
  else:
    return list(map(lambda e: e * x, l))

def subtract(a, b):
  from operator import sub
  if type(a) == type(b) == type(tuple()):
    return tuple(map(sub, a, b))
  if type(a) == type(b) == type(list()):
    return tuple(map(sub, a, b))
#================================================================#


#================================================================#
class Keyboard(object):
  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and e.key == K_ESCAPE and hasattr(self,  'on_esc'):    self.on_esc()
      if e.type == KEYDOWN and e.key == K_SPACE  and hasattr(self,  'on_space'):  self.on_space()

class Framesheet(object):
  def __init__(self, *frames):
    self.frames = [pygame.image.load(frame).convert_alpha() if type(frame) == type(str()) else frame.copy() for frame in frames]
    self._i = 0 

  @property
  def current(self):
    return self.frames[self._i]

  def next_frame(self):
    self._i = (self._i + 1) % len(self.frames)


  def scale(self, s):
    return Framesheet(*[pygame.transform.scale(frame, scale(frame.get_size(), s)) for frame in self.frames])

  def __str__(self):
    return str(self.frames)

#================================================================#
#framesheet.scale(15)


#


if __name__ == '__main__':
  #================#
  mr_pleasant_frames = Framesheet("graphics/mr_pleasant_1.png", "graphics/mr_pleasant_2.png").scale(15)
  nutcracker         = Framesheet("graphics/nutcracker.png").scale(15)
  #================#
  keyboard = Keyboard()
  keyboard.on_space = lambda: mr_pleasant_frames.next_frame()
  keyboard.on_esc   = lambda: done(True)
  #================#

  while not done():
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    screen.blit(mr_pleasant_frames.current, subtract(screen.get_rect().center, mr_pleasant_frames.current.get_rect().center))
    pygame.display.update()
