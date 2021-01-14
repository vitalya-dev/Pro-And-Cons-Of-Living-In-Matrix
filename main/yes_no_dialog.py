import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *


class YesNoDialog(Shape):
  def __init__(self, background_color=BLACK, text_color=GRAY, parent=None):
    super().__init__(parent)
    #================#
    self.background_color = background_color
    self.text_color = text_color
    #================#
    self._surface = pygame.surface.Surface(self._calculate_surface_size())

  def _calculate_surface_size(self):
    return (300, 120)

  def process(self, events):
    pass

  def draw(self):
    return self._surface


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  yes_no_dialog = YesNoDialog()
  yes_no_dialog.pivot = (0.5, 0.5)
  yes_no_dialog.position = screen.get_rect().center
  

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    yes_no_dialog.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(yes_no_dialog.draw(), yes_no_dialog.world_space_rect.topleft)
    pygame.display.update()
  
