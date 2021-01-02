import pygame
from pygame.locals import *

from constants import *
from utils import *

from keyboard import *
from shape import *
from label import *
from fruityloops import *
from jukebox import *
from stacke import *

class HUD(Shape):
  def __init__(self, size):
    super().__init__(parent=None)
    #================#
    self._colorkey = BLACK
    self._surface = pygame.surface.Surface(size).convert()
    self._surface.set_colorkey(self._colorkey)
    #================#
    self._topright_label = Label('', parent=self)
    self._topleft_label = Label('', parent=self)

  def set_topright_label_text(self, label_text):
    self._topright_label = Label(label_text, parent=self)
    self._topright_label.pivot = (1, 0)
    self._topright_label.position = self.self_space_rect.topright

  def set_topleft_label_text(self, label_text):
    self._topleft_label = Label(label_text, parent=self)
    self._topleft_label.pivot = (0, 0)
    self._topleft_label.position = self.self_space_rect.topleft

  def process(self, events):
    pass

  def draw(self):
    self._draw_background()
    self._draw_labels()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self._colorkey)

  def _draw_labels(self):
    self._surface.blit(self._topleft_label.draw(), self._topleft_label.parent_space_rect.topleft)
    self._surface.blit(self._topright_label.draw(), self._topright_label.parent_space_rect.topleft)


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  #================================================================================================#
  fruityloops = Fruityloops(mido.open_output(None), Midi('Breath.mid').beats(), SCREEN_SIZE)
  fruityloops.name = 'Fruityloops'
  #================#
  song_entries = []
  song_entries.append(SongEntry('You Cant Always Get What You Want', 'A1'))
  song_entries.append(SongEntry('Sympathy For Devil', 'A2'))
  song_entries.append(SongEntry('Another Break In The Wall', 'A3'))
  song_entries.append(SongEntry('California Dreaming', 'B1'))
  song_entries.append(SongEntry('No Woman No Cry', 'B2'))
  song_entries.append(SongEntry('Voodoo Child', 'B3'))
  jukebox = Jukebox(song_entries, SCREEN_SIZE)
  jukebox.name = 'Jukebox'
  #================#
  stacke = Stacke()
  stacke.add_shape(fruityloops)
  stacke.add_shape(jukebox)
  #================#
  hud = HUD(SCREEN_SIZE)
  hud.set_topleft_label_text('MODE')
  hud.set_topright_label_text(stacke.active_shape.name)
  #================#
  keyboard = Keyboard()
  keyboard.on_tab += [lambda: stacke.cycles_through_shapes()]
  keyboard.on_tab += [lambda: hud.set_topright_label_text(stacke.active_shape.name)]
  #================================================================================================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    hud.process(events)
    stacke.process(events)
    keyboard.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(stacke.draw(), stacke.world_space_rect.topleft)   
    screen.blit(hud.draw(), hud.world_space_rect.topleft)
    pygame.display.update()



