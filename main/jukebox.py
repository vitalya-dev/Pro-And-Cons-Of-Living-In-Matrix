import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from song_selector import *
from song_holder import *
from scroll import *


class Jukebox(Shape):
  def __init__(self, song_entries, size, parent=None):
    super().__init__(parent)
    #================#
    self._surface = pygame.surface.Surface(size).convert()
    #================#
    self._song_selector = self._create_song_selector()
    self._song_holder_scroller = self._create_song_holder_scroller(song_entries)
    self._song_holder_scroller.move(0, 120)
    

  def draw(self):
    self._surface.blit(self._song_selector.draw(), self._song_selector.parent_space_rect.topleft)
    self._surface.blit(self._song_holder_scroller.draw(), self._song_holder_scroller.parent_space_rect.topleft)
    return self._surface

  def process(self, events):
    self._song_selector.process(events)
    self._song_holder_scroller.process(events)

  def _create_song_selector(self):
    song_selector = SongSelector()
    for i in 'ABCDEF':
      song_selector.add_selector(HorizontalButton(i))
    song_selector.add_selector(VerticalButton('SELECT'))
    for i in '123456':
      song_selector.add_selector(HorizontalButton(i)) 
    return song_selector

  def _create_song_holder_scroller(self, song_entries):
    song_holder_scroller = Scroll(SongHolder())
    song_holder_scroller.limit = self._surface.get_size()
    for song_entry in song_entries:
      song_holder_scroller.child.add_song_entry(song_entry)
    return song_holder_scroller


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

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

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    jukebox.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(jukebox.draw(), jukebox.world_space_rect.topleft)
    pygame.display.update()

