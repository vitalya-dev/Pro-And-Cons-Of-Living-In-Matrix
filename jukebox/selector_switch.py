import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from horizontal_selector_switch_button import *
from vertical_selector_switch_button import *

class SelectorSwitch(Shape):
  def __init__(self):
    super().__init__()
    #================#
    self._switches = []
    self._space_between_switches = 15

  def add_switch_button(self, button):
    button.position = self._calculate_position_for_new_button()
    self._switches.append(button)
    #================#
    self._rebuild_surface()

  def _calculate_position_for_new_button(self):
    if len(self._switches) > 0:
      button_position = tuple_math(self._switches[-1].world_space_rect.topright, '+', (self._space_between_switches, 0))
      return button_position
    else:
      return (0, 0)

  def _rebuild_surface(self):
    self._surface = pygame.surface.Surface((self._buttons_total_width(), self._buttons_max_height())).convert()
    self._surface.set_colorkey((0, 0, 0))

  def _buttons_total_width(self):
    if len(self._switches) > 0:
      buttons_total_width  = sum([button.world_space_rect.width for button in self._switches])
      buttons_total_width_with_spaces = buttons_total_width + (len(self._switches) - 1) * self._space_between_switches
      return buttons_total_width_with_spaces
    else:
      return 0

  def _buttons_max_height(self):
    if len(self._switches) > 0:
      return max([button.world_space_rect.height for button in self._switches])
    else:
      return 0

  def draw(self):
    self._surface.fill((0, 0, 0))
    for button in self._switches:
      self._surface.blit(button.draw(), button.world_space_rect.topleft)
    return self._surface

  def process(self, events):
    for button in self._switches:
      button.process(events)



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  
  #================#
  selector_switch = SelectorSwitch()
  selector_switch.position = screen.get_rect().center
  selector_switch.pivot = (0.5, 0.5)

  for i in 'ABCDEF':
    selector_switch.add_switch_button(HorizontalSelectorSwitchButton(i))
  selector_switch.add_switch_button(VerticalSelectorSwitchButton('SELECT'))
  for i in '123456':
    selector_switch.add_switch_button(HorizontalSelectorSwitchButton(i)) 
  #================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    screen.blit(selector_switch.draw(), selector_switch.world_space_rect.topleft)

    pygame.display.update()


