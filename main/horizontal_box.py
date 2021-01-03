import pygame
from pygame.locals import *

from constants import *
from utils import *

from horizontal_switch import *
from shape import *

class HorizontalBox(Shape):

  def __init__(self, background_color=BLACK, parent=None):
    super().__init__()
    #================#
    self.background_color = background_color
    self._space_between_child = 15
    #================#
    self._childs = []

  def add_child(self, child):
    child.parent = self
    child.position = self._calculate_position_for_new_child()
    self._childs.append(child)
    #================#
    self._rebuild_surface()

  def _calculate_position_for_new_child(self):
    if len(self._childs) > 0:
      child_position = tuple_math(self._childs[-1].parent_space_rect.topright, '+', (self._space_between_child, 0))
      return child_position
    else:
      return (0, 0)

  def _rebuild_surface(self):
    self._surface = pygame.surface.Surface((self._child_total_width(), self._child_max_height())).convert()

  def _child_total_width(self):
    if len(self._childs) > 0:
      child_total_width  = sum([child.parent_space_rect.width for child in self._childs])
      child_total_width_with_spaces = child_total_width + (len(self._childs) - 1) * self._space_between_child
      return child_total_width_with_spaces
    else:
      return 0

  def _child_max_height(self):
    if len(self._childs) > 0:
      return max([child.parent_space_rect.height for child in self._childs])
    else:
      return 0

  def process(self, events):
    for child in self._childs:
      child.process(events)

  def draw(self):
    self._surface.fill(self.background_color)
    for child in self._childs:
      self._surface.blit(child.draw(), child.parent_space_rect.topleft)
    return self._surface



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  
  #================#
  horizontal_box = HorizontalBox()
  for i in 'ABCDEF':
    horizontal_box.add_child(HorizontalSwitch(i))
  #================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    horizontal_box.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(horizontal_box.draw(), horizontal_box.world_space_rect.topleft)
    pygame.display.update()

