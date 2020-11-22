import random
import itertools
import operator

import pygame
from pygame.locals import *

#================================================================#
SCREEN_SIZE = (640, 480)
MSEC2SEC = 0.001
#================================================================#


#================================================================#
pygame.init()
random.seed()
#================================================================#


#================================================================#
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
#================================================================#


#================================================================#
def done(val=None):
  if not hasattr(done, 'val'): done.val = False
  if val == None: return done.val
  done.val = val;

def tuple_math(a, op, b):
  if not hasattr(b, "__getitem__"):
    b = (b,) * len(a)
  if op == '+':
    return tuple(map(operator.add, a, b))
  if op == '-':
    return tuple(map(operator.sub, a, b))
  if op == '*':
    return tuple(map(operator.mul, a, b))
#================================================================#


#================================================================#
class Keyboard(object):
  def __init__(self):
    self.on_esc   = []
    self.on_space = []

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and e.key == K_ESCAPE:
        for f in self.on_esc: f()
      if e.type == KEYDOWN and e.key == K_SPACE:
        for f in self.on_space: f()

class ControlPanelButton(object):
  def __init__(self, name):
    self._name = name
    self._rect = pygame.Rect(0, 0, 16, 32)
    self._foreground = pygame.Color('#ffffff')
    self._background = pygame.Color('#b82e0a')
    self._light = pygame.Color('#f15815')
    self._font = pygame.font.Font('data/FSEX300.ttf', 32)


  @property
  def position(self):
    return self._rect.topleft

  @position.setter
  def position(self, value):
    self._rect.topleft = value

  def process(self, events):
    pass

  def render(self, surface):
    self._draw_background(surface)
    self._draw_light(surface)
    self._draw_text(surface)

  def _draw_background(self, surface):
    surface.fill(self._background, self._rect)

  def _draw_light(self, surface):
    light_rect = pygame.Rect(tuple_math(self.position, '+', (0, 24)), (16, 8))
    surface.fill(self._light, light_rect)

  def _draw_text(self, surface):
    surface.blit(self._font.render(self._name, False, self._foreground), tuple_math(self.position, '-', (0, 5)))

#================================================================#



#================================================================#
if __name__ == '__main__':
  #================#
  keyboard = Keyboard()
  keyboard.on_esc += [lambda: done(True)]
  #================#
  a = ControlPanelButton('A')
  a.position = screen.get_rect().center

  while not done():
    clock.tick()
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    a.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    a.render(screen)
    pygame.display.update()

