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
    self._rendered_text = self._font.render(self._text, False, self._foreground_color)
    self._rendered_text_position = (0, -5)
    #================#
    self._surface = pygame.surface.Surface(self._rendered_text.get_size()).convert()

  def process(self, events):
    pass

  def draw(self):
    self._draw_background()
    self._draw_text()
    self._draw_light()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self._background_color, self._surface.get_rect())

  def _draw_light(self):
    light_position = (0, self._surface.get_height() * 3 / 4)
    light_size = (self._surface.get_width(), self._surface.get_height() / 4)
    self._surface.fill(self._light_color, pygame.Rect(light_position, light_size))

  def _draw_text(self):
    self._surface.blit(self._rendered_text, self._rendered_text_position)
    

if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  a_btn = HorizontalSelectorSwitchButton('A')
  a_btn.pivot = (0, 0)
  a_btn.position = screen.get_rect().center

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    a_btn.process(events)
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    screen.blit(a_btn.draw(), a_btn.rect.topleft)

    pygame.display.update()
