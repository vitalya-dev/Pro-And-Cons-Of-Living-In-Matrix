import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class SongHolder(Shape):
  def __init__(self):
    super().__init__()
    #================#
    self._song_entries = []

  def add_song_entry(self, song_entry):
    song_entry.position = self._calculate_position_for_new_entry()
    self._song_entries.append(song_entry)
    #================#
    self._rebuild_surface()

  def _rebuild_surface(self):
    self._surface = pygame.surface.Surface((self._song_entries_max_width(), self._song_entries_total_height())).convert()
    self._surface.set_colorkey((0, 0, 0))

    
  def _song_entries_total_height(self):
    if len(self._song_entries) > 0:
      song_entries_total_height = sum([song_entry.word_space_rect.height for song_entry in self._song_entries])
      song_entries_total_height_with_spaces = song_entries_total_height + self.song_entries_margin * (len(self._song_entries) - 1)
      return song_entries_total_height_with_margin
    else:
      return 0

  def _song_entries_max_width(self):
    if len(self._song_entries) > 0:
      return max([song_entry.world_space_rect.width for song_entry in self._song_entries])
    else:
      return 0


