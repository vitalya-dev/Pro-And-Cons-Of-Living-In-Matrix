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
  if op == '/':
    return tuple(map(operator.truediv, a, b))
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
  def rect(self):
    return pygame.Rect(self.position, tuple_math(self._rendered_text.get_size(), '-', (0, 1)))
  
  @property
  def size(self):
    return self.rect.size

  @property
  def height(self):
    return self.rect.height

  @property
  def width(self):
    return self.rect.width

  @property
  def x(self):
    return self.rect.x

  @property
  def y(self):
    return self.rect.y

  def process(self, events):
    pass

  def render(self, surface):
    self._draw_background(surface)
    self._draw_light(surface)
    self._draw_text(surface)

  def _draw_background(self, surface):
    surface.fill(self._background_color, self.rect)

  def _draw_light(self, surface):
    light_position = tuple_math(self.position, '+', (0, self.height * 3 / 4))
    light_size = (self.width, self.height  / 4)
    surface.fill(self._light_color, pygame.Rect(light_position, light_size))

  def _draw_text(self, surface):
    surface.blit(self._rendered_text, tuple_math(self.position, '-', (0, 5)))
    

class VerticalSelectorSwitchButton(HorizontalSelectorSwitchButton):
  def __init__(self, text):
    super().__init__(text)
    self._rendered_text = pygame.transform.rotate(self._rendered_text, -90)

  def render(self, surface):
    self._draw_background(surface)
    self._draw_text(surface)

  def _draw_text(self, surface):
    surface.blit(self._rendered_text, self.position)

class SelectorSwitch(object):
  def __init__(self):
    self.position = (0, 0)
    self.pivot = (0, 0)
    self.button_margin = 25
    self._switches = []
    self._surface = pygame.surface.Surface((0, 0)).convert()

  def add_horizontal_switch_button(self, button_name):
    button = HorizontalSelectorSwitchButton(button_name)
    button.position = self._calculate_position_for_new_button()
    self._switches.append(button)
    #================#
    self._resize_surface()


  def add_vertical_switch_button(self, button_name):
    button = VerticalSelectorSwitchButton(button_name)
    button.position = self._calculate_position_for_new_button()
    self._switches.append(button)
    #================#
    self._resize_surface()

  def _resize_surface(self):
    self._surface = pygame.surface.Surface((self._buttons_total_width(), self._buttons_max_height())).convert()
    self._surface.set_colorkey((0, 0, 0))

  def _calculate_position_for_new_button(self):
    if len(self._switches) == 0:
      return (0, 0)
    else:
      new_button_position = tuple_math(self._switches[-1].position, '+', (self._switches[-1].width, 0))
      new_button_position = tuple_math(new_button_position, '+', (self.button_margin, 0))
      return new_button_position

  def _buttons_total_width(self):
    if len(self._switches) > 0:
      buttons_total_width = sum([button.width for button in self._switches])
      buttons_total_width_with_margin = buttons_total_width + self.button_margin * (len(self._switches) - 1)
      return buttons_total_width_with_margin
    else:
      return 0

  def _buttons_max_height(self):
    if len(self._switches) > 0:
      return max([button.height for button in self._switches])
    else:
      return 0

  def _top_left_position(self):
    pivot_position = tuple_math(self.pivot, '*', self._surface.get_size())
    pivot_position_as_int = tuple(map(int, pivot_position))
    return tuple_math(self.position, '-', pivot_position_as_int)

  def render(self, surface):
    self._surface.fill((0, 0, 0))
    for button in self._switches:
      button.render(self._surface)
    surface.blit(self._surface, self._top_left_position())

  def process(self, events):
    for button in self._switches:
      button.process(events)


class SongEntry(object):
  def __init__(self, name, id):
    self.name = name
    self.id = id
    self.position = (0, 0)
    self.pivot = (0, 0)
    #================#
    self._song_name_foreground_color = pygame.Color('#b99559')
    self._song_id_foreground_color = pygame.Color('#b82e0a')
    self._background_color = pygame.Color('#efe8b4')
    self._border_color = pygame.Color('#767877')
    #================#
    self._song_name_font = pygame.font.Font('data/FSEX300.ttf', 24)
    self._song_id_font = pygame.font.Font('data/FSEX300.ttf', 64)
    self._rendered_song_name = self._song_name_font.render(self.name, False, self._song_name_foreground_color)
    self._rendered_song_id = self._song_id_font.render(self.id, False, self._song_id_foreground_color)
    #================#
    self._surface = pygame.surface.Surface(self._calculate_surface_size())
    self._surface.fill(self._background_color)
    pygame.draw.rect(self._surface, self._border_color, self._surface.get_rect(), 5)
  
  def _calculate_surface_size(self):
    size_for_name = self._rendered_song_name.get_size()
    size_for_name_and_id = tuple_math(size_for_name, '+', (0, 48))
    size_for_name_and_id_with_margin = tuple_math(size_for_name_and_id, '+', (12, 0))
    return size_for_name_and_id_with_margin

  def _top_left_position(self):
    pivot_position = tuple_math(self.pivot, '*', self._surface.get_size())
    pivot_position_as_int = tuple(map(int, pivot_position))
    return tuple_math(self.position, '-', pivot_position_as_int)

  def process(self, events):
    pass

  def render(self, surface):
    self._surface.blit(self._rendered_song_name, self._rendered_song_name_position())
    self._surface.blit(self._rendered_song_id, self._rendered_song_id_position())
    surface.blit(self._surface, self._top_left_position())

  def _rendered_song_name_position(self):
    return (6, 6)

  def _rendered_song_id_position(self):
    return (6, 16)

#================================================================#



#================================================================#
if __name__ == '__main__':
  #================#
  keyboard = Keyboard()
  keyboard.on_esc += [lambda: done(True)]
  #================#
  selector_switch = SelectorSwitch()
  selector_switch.position = screen.get_rect().center
  selector_switch.pivot = (0.5, 0.5)
  for i in 'ABCDEF':
    selector_switch.add_horizontal_switch_button(i) 
  selector_switch.add_vertical_switch_button('SELECT')
  for i in '123456':
    selector_switch.add_horizontal_switch_button(i) 
  #================#
  song = SongEntry('You Cant Always Get What You Want', 'A1')

  while not done():
    clock.tick()
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    selector_switch.process(events)
    song.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    selector_switch.render(screen)
    song.render(screen)
    pygame.display.update()

