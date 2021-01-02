import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from label import *
from fruityloops import *
from jukebox import *

class HUD(Shape):
  def __init__(self, size):
    super().__init__(parent=None)
    #================#
    self._colorkey = BLACK
    self._surface = pygame.surface.Surface(size).convert()
    self._surface.set_colorkey(self._colorkey)
    #================#
    self._topright_label = Label('', parent=self)

  def set_topright_label_text(self, label_text):
    self._topright_label = Label(label_text, parent=self)
    self._topright_label.pivot = (1, 0)
    self._topright_label.position = self.self_space_rect.topright


  def process(self, events):
    pass

  def draw(self):
    self._draw_background()
    self._draw_labels()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self._colorkey)

  def _draw_labels(self):
    self._surface.blit(self._topright_label.draw(), self._topright_label.parent_space_rect.topleft)
    return self._surface


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  #================================================================================================#
  hud = HUD(SCREEN_SIZE)
  hud.set_topright_label_text('[TAB]Jukebox')

  fruityloops = Fruityloops(mido.open_output(None), Midi('Breath.mid').beats(), SCREEN_SIZE)
  #================================================================================================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()

    hud.process(events)
    fruityloops.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(fruityloops.draw(), fruityloops.world_space_rect.topleft)
    screen.blit(hud.draw(), hud.world_space_rect.topleft)
    pygame.display.update()



