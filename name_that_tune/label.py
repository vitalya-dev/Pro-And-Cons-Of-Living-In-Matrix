import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class Label(Shape):
  def __init__(self, text, size=None, parent=None):
    super().__init__(parent)
    #================#
    self._foreground_color = pygame.Color('#AA0000')
    self._background_color = pygame.Color('#000080')
    #================#
    self._font = pygame.font.Font('fonts/FSEX300.ttf', 32)
    self._text = text
    self._rendered_text = self._font.render(self._text, False, self._foreground_color)
    #================#
    if size == None:
      size = self._rendered_text.get_size()
    self._surface = pygame.surface.Surface(size).convert()

  def process(self, events):
    pass

  def draw(self):
    self._draw_background()
    self._draw_text()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self._background_color)

  def _draw_text(self):
    self._surface.blit(self._rendered_text, self._rendered_text.get_rect(center=self._surface.get_rect().center).topleft)
    


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  a_label = Label('A', size=(80, 32))
  a_label.pivot = (0.5, 0.5)
  a_label.position = screen.get_rect().center

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    a_label.process(events)
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    screen.blit(a_label.draw(), a_label.world_space_rect.topleft)
    pygame.display.update()


    
