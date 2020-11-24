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

class HorizontalSelectorSwitchButton(object):
  def __init__(self, text):
    self.position = (0, 0)
    #================#
    self._foreground_color = pygame.Color('#ffffff')
    self._background_color = pygame.Color('#b82e0a')
    self._light_color = pygame.Color('#f15815')
    #================#
    self._font = pygame.font.Font('data/FSEX300.ttf', 32)
    self._text = text
    self._rendered_text = self._font.render(self._text, False, self._foreground_color)
    #================#


  @property
  def button_rect(self):
    return pygame.Rect(self.position, tuple_math(self._rendered_text.get_size(), '-', (0, 1)))
  
  @property
  def button_size(self):
    return self.button_rect.size

  @property
  def button_height(self):
    return self.button_rect.height

  @property
  def button_width(self):
    return self.button_rect.width

  def process(self, events):
    pass

  def render(self, surface):
    self._draw_background(surface)
    self._draw_light(surface)
    self._draw_text(surface)

  def _draw_background(self, surface):
    surface.fill(self._background_color, self.button_rect)

  def _draw_light(self, surface):
    light_position = tuple_math(self.position, '+', (0, self.button_height * 3 / 4))
    light_size = (self.button_width, self.button_height  / 4)
    surface.fill(self._light_color, pygame.Rect(light_position, light_size))

  def _draw_text(self, surface):
    surface.blit(self._rendered_text, tuple_math(self.position, '-', (0, 5)))
    

VerticalSelectorSwitchButton = HorizontalSelectorSwitchButton

#================================================================#



#================================================================#
if __name__ == '__main__':
  #================#
  keyboard = Keyboard()
  keyboard.on_esc += [lambda: done(True)]
  #================#
  a_btn = HorizontalSelectorSwitchButton('A')
  a_btn.position = screen.get_rect().center

  select_btn = VerticalSelectorSwitchButton("SELECT")
  select_btn.position = tuple_math(screen.get_rect().center, '+', (50, 50))
  
  while not done():
    clock.tick()
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    a_btn.process(events)
    select_btn.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    a_btn.render(screen)
    select_btn.render(screen)
    pygame.display.update()

