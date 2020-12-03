import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class SongEntry(Shape):
  def __init__(self, text, **kwargs):
    super().__init__()
    #================#
    self.name = name
    self.id = id
    #================#
    self._padding = (12, 2)
    #================#
    self._song_name_foreground_color = pygame.Color('#b99559')
    self._song_id_foreground_color = pygame.Color('#b82e0a')
    self._background_color = pygame.Color('#efe8b4')
    self._border_color = pygame.Color('#767877')
    #================#
    self._song_name_font = pygame.font.Font('data/FSEX300.ttf', 24)
    self._song_id_font = pygame.font.Font('data/FSEX300.ttf', 64)
    self._rendered_song_name = self._song_name_font.render(self.name, False, self._song_name_foreground_color)
    self._rendered_song_name_position = (6, 6)
    self._rendered_song_id = self._song_id_font.render(self.id, False, self._song_id_foreground_color)
    self._rendered_song_id_position = (6, 16)
    #================#
    self._surface = pygame.surface.Surface(self._calculate_surface_size())


  def _calculate_surface_size(self):
    size_for_name = self._rendered_song_name.get_size()
    size_for_name_and_id = tuple_math(size_for_name, '+', (0, 48))
    size_for_name_and_id_with_padding = tuple_math(size_for_name_and_id, '+', self._padding)
    return size_for_name_and_id_with_padding


  def draw(self):
    self._surface.blit(self._rendered_song_name, self._rendered_song_name_position)
    self._surface.blit(self._rendered_song_id, self._rendered_song_id_position)
    return self._surface
