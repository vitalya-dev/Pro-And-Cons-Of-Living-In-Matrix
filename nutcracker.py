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

def multiply(l1, l2):
  from operator import mul
  return tuple(map(mul, l1, l2))

def subtract(l1, l2):
  from operator import sub
  return tuple(map(sub, l1, l2))
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
      pygame.draw.circle(self.surface, (255, 255, 255), self.surface.get_rect().center, int(10 * random.random()))

  def process(self, events):
    pass

  def render(self):
    return self.surface

class Framesheet(object):
  def __init__(self, *frames):
    self.frames = [self._load(frame) if type(frame) == type(str()) else frame.copy() for frame in frames]
    self.position = (0, 0)
    self.pivot    = (0, 0)
    self._current_frame_index = 0 

  def _load(self, frame):
    frame = frame.split(':')
    if len(frame) == 1:
      return pygame.image.load(frame[0]).convert_alpha()
    elif len(frame) == 3:
      return self._load_and_translate(frame[0], frame[1], frame[2])
    else:
      return pygame.image.load(frame[-1]).convert_alpha()

  def _load_and_translate(self, translate_function, translate_param, frame):
    if translate_function == 'r':
      return pygame.transform.rotate(pygame.image.load(frame).convert_alpha(), int(translate_param))
    else:
      return pygame.image.load(frame)

  @property
  def current_frame(self):
    return self.frames[self._current_frame_index]

  @current_frame.setter
  def current_frame(self, current):
    self._current_frame_index = self.frames.index(current)

  @property
  def current_index(self):
    return self._current_frame_index

  @property
  def last_frame(self):
    return self.frames[-1]

  def next_frame(self):
    self._current_frame_index = (self._current_frame_index + 1) % len(self.frames)

  def render(self, surface):
    pivot_position = multiply(self.current_frame.get_size(), self.pivot)
    surface.blit(self.current_frame, subtract(self.position, pivot_position))

  def scale(self, scale_factor):
    return Framesheet(*[pygame.transform.scale(frame, multiply(frame.get_size(), (scale_factor, scale_factor))) for frame in self.frames])

  def __getitem__(self, index):
    return self.frames[index]

  def __str__(self):
    return str(self.frames)

#================================================================#

if __name__ == '__main__':
  #================#
  mr_pleasant = Framesheet("graphics/mr_pleasant_1.png", "graphics/mr_pleasant_2.png", "graphics/mr_pleasant_2.png").scale(14)
  mr_pleasant.pivot = (0.5, 0.5)
  mr_pleasant.position = subtract(screen.get_rect().center, (0, 75))
  #================#
  nutcracker = Framesheet("r:180:graphics/nutcracker.png", "graphics/nutcracker.png", "r:180:graphics/nutcracker.png").scale(14)
  nutcracker.position = subtract(screen.get_rect().center, (0, -125))
  nutcracker.pivot = (0.5, 0.5)
  #================#
  keyboard = Keyboard()
  keyboard.on_space += [lambda: mr_pleasant.next_frame()]
  keyboard.on_space += [lambda: nutcracker.next_frame()]
  keyboard.on_esc   += [lambda: done(True)]
  #================#

  while not done():
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    mr_pleasant.render(screen)
    nutcracker.render(screen)
    pygame.display.update()
