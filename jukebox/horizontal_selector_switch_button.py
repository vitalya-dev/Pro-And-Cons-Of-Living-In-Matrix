import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class HorizontalSelectorSwitchButton(Shape):
  def __init__(self, text):
    super().__init__()
    #================#
    self._foreground_color = pygame.Color('#ffffff')
    self._background_color = pygame.Color('#b82e0a')
    self._light_color = pygame.Color('#f15815')
    #================#
    self._font = pygame.font.Font('data/FSEX300.ttf', 32)
    self._text = text
    self._text_offset = (0, -5)
    self._rendered_text = self._font.render(self._text, False, self._foreground_color)
    #================#

  @property
  def size(self):
    return self._rendered_text.get_size()

  @size.setter
  def size(self, value):
    pass

  def process(self, events):
    pass

  def render(self, surface):
    self._draw_background(surface)
    self._draw_light(surface)
    self._draw_text(surface)

  def _draw_background(self, surface):
    surface.fill(self._background_color, self.rect)

  def _draw_light(self, surface):
    light_position = tuple_math(self.rect.topleft, '+', (0, self.rect.height * 3 / 4))
    light_size = (self.rect.width, self.rect.height / 4)
    surface.fill(self._light_color, pygame.Rect(light_position, light_size))

  def _draw_text(self, surface):
    surface.blit(self._rendered_text, tuple_math(self.rect.topleft, '+', self._text_offset))
    

if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  a_btn = HorizontalSelectorSwitchButton('A')
  a_btn.pivot = (0.5, 0.5)
  a_btn.position = screen.get_rect().center

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    a_btn.process(events)
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    a_btn.render(screen)
    pygame.display.update()
