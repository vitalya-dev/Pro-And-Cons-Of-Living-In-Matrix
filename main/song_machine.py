import pygame
from pygame.locals import *

from constants import *
from utils import *

from song_holder import *
from song_selector import *


class SongMachine(Shape):
  def __init__(self, song_entries, size=SCREEN_SIZE, background_color=BLACK, parent=None):
    super().__init__(parent)
    #================#
    self.background_color = background_color
    #================#
    self._song_entries = song_entries
    #================#
    self._song_selector = SongSelector(background_color=background_color, parent=self)
    self._song_selector.on_toggle.append(self._song_selector_on_toggle_handler)
    #================#
    self._song_holder = SongHolder(
      song_entries,
      size=tuple_math(size, '-', (0, self._song_selector.height)),
      background_color=background_color,
      parent=self
    )
    self._song_holder.scroll_area_size = 4
    #================#
    self._surface = pygame.surface.Surface(size).convert()
    #================#
    self._layout_elements()

  def _song_selector_on_toggle_handler(self, switch):
    print(switch)

  def _song_holder_filter_entries(self, filter):
    filtered_entries = [song_entry for song_entry in self._song_entries if song_entry.name.casefold().startswidth(filter.casefold())]
    self._song_holder.set_song_entries(filtered_entries)

  def _layout_elements(self):
    self._song_selector.pivot = (0.5, 0)
    self._song_selector.position = self._surface.get_rect().midtop
    #================#
    self._song_holder.pivot = (0.5, 1)
    self._song_holder.position = self._surface.get_rect().midbottom

if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  song_entries = [
    SongEntry('Gimme Shelter'),
    SongEntry('Sympathy For Devil'),
    SongEntry('Bohemian Rhapsody'),
    SongEntry('Respect'),
    SongEntry('Feeling Good'),
    SongEntry('Unchained Melody'),
    SongEntry('Wish You Were Here'),
    SongEntry('Another Break In The Wall'),
    SongEntry('You Cant Always Get What You Want'),
    SongEntry('California Dreaming'),
    SongEntry('No Woman No Cry'),
    SongEntry('Voodoo Child'),
    SongEntry('voodoo People')
  ]
  song_machine = SongMachine(song_entries)

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    pygame.display.update()
