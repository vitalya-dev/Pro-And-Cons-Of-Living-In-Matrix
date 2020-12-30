import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from label import *

class HUD(Shape):
  def __init__(self, screen_size):
    super().__init__(parent=None)
    #================#
    self._jukebox_label = Label('Jukebox', parent=self)
    #================#
    self._colorkey = BLACK
    self._surface = pygame.surface.Surface(screen_size).convert()
    self._surface.set_colorkey(self._colorkey)

  def draw(self):
    self._draw_background()
    self._draw_labels()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self._colorkey)

  def _draw_labels(self):
    return self._surface


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  #================================================================================================#
  hud = HUD(SCREEN_SIZE)
  #================================================================================================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(hud.draw(), hud.world_space_rect.topleft)
    pygame.display.update()



