import random

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
  return tuple(map(sub, a, b))


#================================================================#


#================================================================#
class Keyboard(object):
  def __init__(self):
    self.on_esc   = []
    self.on_space = []

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and e.key == K_ESCAPE:
        for c in self.on_esc: c()
      if e.type == KEYDOWN and e.key == K_SPACE:
        for c in self.on_space: c()

class Particles:
  def __init__(self, timer):
    self.surface = pygame.surface.Surface(SCREEN_SIZE).convert()
    self.surface.set_colorkey((0, 0, 0))

  def generate(self, n):
    for i in range(0, n):
      pygame.draw.circle(self.surface, (255, 255, 255), self.sruface.get_rect().center, 10 * random.random())

  def process(self, events):
    pass

  def render(self):
    return self.surface

class Framesheet(object):
  def __init__(self, *frames):
    self.frames = [self._load(frame) if type(frame) == type(str()) else frame.copy() for frame in frames]
    self._i = 0 

  def _load(self, frame):
    frame = frame.split(':')
    if len(frame) == 1:
      return pygame.image.load(frame[0]).convert_alpha()
    elif len(frame) == 3:
      return self._load_and_translate(frame[0], frame[1], frame[2])
    else:
      return pygame.image.load(frame[-1]).convert_alpha()

  def _load_and_translate(self, tr, x, frame):
    if tr == 'r':
      return pygame.transform.rotate(pygame.image.load(frame).convert_alpha(), int(x))
    else:
      return pygame.image.load(frame)

  @property
  def current(self):
    return self.frames[self._i]

  @property
  def index(self):
    return self._i

  @current.setter
  def current(self, current):
    self._i = self.frames.index(current)

  @property
  def last(self):
    return self.frames[-1]


  def next_frame(self):
    self._i = (self._i + 1) % len(self.frames)


  def scale(self, s):
    return Framesheet(*[pygame.transform.scale(frame, scale(frame.get_size(), s)) for frame in self.frames])

  def __getitem__(self, index):
    return self.frames[index]

  def __str__(self):
    return str(self.frames)

#================================================================#
#framesheet.scale(15)



if __name__ == '__main__':
  #================#
  mr_pleasant_frames = Framesheet("graphics/mr_pleasant_1.png", "graphics/mr_pleasant_2.png", "graphics/mr_pleasant_2.png").scale(14)
  mr_pleasant_positions = [
    subtract(screen.get_rect().center, (0, 75)),
    subtract(screen.get_rect().center, (0, 75)),
    subtract(screen.get_rect().center, (0, 75))
  ]
  #================#
  nutcracker_frames  = Framesheet("r:180:graphics/nutcracker.png", "graphics/nutcracker.png", "r:180:graphics/nutcracker.png").scale(14)
  nutcracker_positions = [
    subtract(screen.get_rect().center, (0, -125)),
    subtract(screen.get_rect().center, (0, -45)),
    subtract(screen.get_rect().center, (0, -125))
  ]
  #================#
  particles = Particles(3)
  particles_positions = [nutcracker_positions[0], nutcracker_positions[1], nutcracker_positions[2]]
  #================#
  keyboard = Keyboard()
  keyboard.on_space += [lambda: mr_pleasant_frames.next_frame()]
  keyboard.on_space += [lambda: nutcracker_frames.next_frame()]
  keyboard.on_space += [lambda: particles.generate(250 * 1 if nutcracker_frames.index == 1 else 0)]
  keyboard.on_esc   += [lambda: done(True)]
  #================#

  while not done():
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    particles.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    screen.blit(mr_pleasant_frames.current, mr_pleasant_positions[mr_pleasant_frames.index])
    screen.blit(nutcracker_frames.current,  nutcracker_positions[nutcracker_frames.index])
    screen.blit(particles.render(), particles_positions)
    pygame.display.update()
