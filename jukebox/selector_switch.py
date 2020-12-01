import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class SelectorSwitch(Shape):
  def __init__(self):
    super().__init__()
    #================#
    self._switches = []
    self._space_between_switches = 25

  def add_switch_button(self, button):
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
      new_button_position = tuple_math(self._switches[-1].position, '+', (self._switches[-1].world_space_rect.width, 0))
      new_button_position = tuple_math(new_button_position, '+', (self._space_between_switches, 0))
      return new_button_position

  def _buttons_total_width(self):
    if len(self._switches) > 0:
      buttons_total_width = sum([button.world_space_rect.width for button in self._switches])
      buttons_total_width_with_margin = buttons_total_width + self._space_between_switches * (len(self._switches) - 1)
      return buttons_total_width_with_margin
    else:
      return 0

  def _buttons_max_height(self):
    if len(self._switches) > 0:
      return max([button.height for button in self._switches])
    else:
      return 0

  def render(self, surface):
    self._surface.fill((0, 0, 0))
    for button in self._switches:
      button.render(self._surface)
    surface.blit(self._surface, self._top_left_position())

  def process(self, events):
    for button in self._switches:
      button.process(events)







