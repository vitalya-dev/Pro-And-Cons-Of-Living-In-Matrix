import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from song_entry import *

class SongHolder(Shape):
  def __init__(self, song_entries, background_color=BLACK, parent=None):
    super().__init__(parent)
    #================#
    self.background_color = background_color
    #================#
    self._song_entries = song_entries
    self._space_between_song_entries = 15
    #================#
    self._parent_song_entries()
    self._layout_song_entries()
    #================#
    self._surface = pygame.surface.Surface((self._song_entries_max_width(), self._song_entries_total_height())).convert()

  def _parent_song_entries(self):
    for song_entry in self._song_entries:
      song_entry.parent = self

  def _layout_song_entries(self):
    for i, song_entry in enumerate(self._song_entries):
      if i > 0:
        song_entry_position = tuple_math(self._song_entries[i-1].parent_space_rect.bottomleft, '+', (0, self._space_between_song_entries))
      else:
        song_entry_position = (0, 0)
      song_entry.position = song_entry_position

  def _song_entries_total_height(self):
    if len(self._song_entries) > 0:
      song_entries_total_height = sum([song_entry.parent_space_rect.height for song_entry in self._song_entries])
      song_entries_total_height_with_spaces = song_entries_total_height + self._space_between_song_entries * (len(self._song_entries) - 1)
      return song_entries_total_height_with_spaces
    else:
      return 0

  def _song_entries_max_width(self):
    if len(self._song_entries) > 0:
      return max([song_entry.parent_space_rect.width for song_entry in self._song_entries])
    else:
      return 0

  def draw(self):
    self._surface.fill(self.background_color)
    for song_entry in self._song_entries:
      self._surface.blit(song_entry.draw(), song_entry.parent_space_rect.topleft)
    return self._surface

  def process(self, events):
    for song_entry in self._song_entries:
      song_entry.process(events)

if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  
  #================#
  song_entries =  [
    SongEntry('You Cant Always Get What You Want'),
    SongEntry('Sympathy For Devil'),
    SongEntry('Another Break In The Wall'),
    SongEntry('California Dreaming'),
    SongEntry('No Woman No Cry'),
    SongEntry('Voodoo Child')
  ]
  song_holder = SongHolder(song_entries, background_color=WHITE)
  song_holder.position = screen.get_rect().center
  song_holder.pivot = (0.5, 0.5)


  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(song_holder.draw(), song_holder.world_space_rect.topleft)

    pygame.display.update()

      
