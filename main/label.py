import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class Label(Shape):
  def __init__(self, text , size=None, parent=None):
    super().__init__(parent)
    #================#
    self.primary_color = BLACK
    self.secondary_color = BLACK
    self.tertiary_color = BLACK
    self.quaternary_color = BLACK
    self.quinary_color = BLACK
    self.senary_color = BLACK
    self.septenary_color = BLACK
    self.octonary_color = BLACK
    #================#
    self._font = pygame.font.Font('fonts/FSEX300.ttf', 32)
    self._text = text
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
    self._surface.fill(self.primary_color)

  def _draw_text(self):
    rendered_text = self._font.render(self._text, False, self.secondary_color)
    blit_center(self._surface, rendered_text)
    


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  a_label = Label('A', size=(80, 32))
  a_label.secondary_color = GRAY
  a_label.pivot = (0.5, 0.5)
  a_label.position = screen.get_rect().center

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    a_label.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(a_label.draw(), a_label.world_space_rect)
    pygame.display.update()


    
