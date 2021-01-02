import pygame
from pygame.locals import *

from constants import *
from utils import *

from keyboard import *
from shape import *
from fruityloops import *
from jukebox import *

class Stacke(Shape):
  def __init__(self, parent=None):
    super().__init__(parent)
    #================#
    self._shapes = []
    self._active_shape = None

  def add_shape(self, shape):
    shape.parent = self
    self._shapes.append(shape)
    if len(self._shapes) == 1:
      self._active_shape = shape
      self._surface = self._make_new_surface_with_same_size_as_in_active_shape()

  def _make_new_surface_with_same_size_as_in_active_shape(self):
    return pygame.surface.Surface(self._active_shape._surface.get_size()).convert()

  def process(self, events):
    if self._active_shape:
      self._active_shape.process(events)

  def draw(self):
    if self._active_shape:
      self._surface.blit(self._active_shape.draw(), (0, 0))
    return self._surface

  def cycles_through_shapes(self):
    if self._active_shape:
      current_active_shape_index = self._shapes.index(self._active_shape)
      new_active_shape_index = (current_active_shape_index + 1) % len(self._shapes)
      #================#
      self._active_shape = self._shapes[new_active_shape_index]


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#


  #================================================================================================#
  fruityloops = Fruityloops(mido.open_output(None), Midi('Breath.mid').beats(), SCREEN_SIZE)
  #================#
  song_entries = []
  song_entries.append(SongEntry('You Cant Always Get What You Want', 'A1'))
  song_entries.append(SongEntry('Sympathy For Devil', 'A2'))
  song_entries.append(SongEntry('Another Break In The Wall', 'A3'))
  song_entries.append(SongEntry('California Dreaming', 'B1'))
  song_entries.append(SongEntry('No Woman No Cry', 'B2'))
  song_entries.append(SongEntry('Voodoo Child', 'B3'))
  jukebox = Jukebox(song_entries, SCREEN_SIZE)
  #================#
  stacke = Stacke()
  stacke.add_shape(fruityloops)
  stacke.add_shape(jukebox)
  #================#
  keyboard = Keyboard()
  keyboard.on_tab += [lambda: stacke.cycles_through_shapes()]
  #================================================================================================#


  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    stacke.process(events)
    keyboard.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(stacke.draw(), stacke.world_space_rect.topleft)   
    pygame.display.update()
    
