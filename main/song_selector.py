import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from horizontal_button import *
from vertical_button import *

class SongSelector(Shape):
  def __init__(self, background_color=BLACK, parent=None):
    super().__init__()
    #================#
    self.background_color = background_color
    #================#
    self._selectors = []
    self._space_between_selectors = 15

  def add_selector(self, selector):
    selector.position = self._calculate_position_for_new_selector()
    selector.parent = self
    self._selectors.append(selector)
    #================#
    self._rebuild_surface()

  def _calculate_position_for_new_selector(self):
    if len(self._selectors) > 0:
      selector_position = tuple_math(self._selectors[-1].parent_space_rect.topright, '+', (self._space_between_selectors, 0))
      return selector_position
    else:
      return (0, 0)

  def _rebuild_surface(self):
    self._surface = pygame.surface.Surface((self._selectors_total_width(), self._selectors_max_height())).convert()

  def _selectors_total_width(self):
    if len(self._selectors) > 0:
      selectors_total_width  = sum([selector.parent_space_rect.width for selector in self._selectors])
      selectors_total_width_with_spaces = selectors_total_width + (len(self._selectors) - 1) * self._space_between_selectors
      return selectors_total_width_with_spaces
    else:
      return 0

  def _selectors_max_height(self):
    if len(self._selectors) > 0:
      return max([selector.parent_space_rect.height for selector in self._selectors])
    else:
      return 0

  def draw(self):
    self._surface.fill(self.background_color)
    for selector in self._selectors:
      self._surface.blit(selector.draw(), selector.parent_space_rect.topleft)
    return self._surface

  def process(self, events):
    for selector in self._selectors:
      selector.process(events)



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  
  #================#
  song_selector = SongSelector()
  song_selector.position = screen.get_rect().center
  song_selector.pivot = (0.5, 0.5)

  for i in 'ABCDEF':
    song_selector.add_selector(HorizontalButton(i))
  song_selector.add_selector(VerticalButton('SELECT'))
  for i in '123456':
    song_selector.add_selector(HorizontalButton(i)) 
  #================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    song_selector.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(song_selector.draw(), song_selector.world_space_rect.topleft)

    pygame.display.update()


