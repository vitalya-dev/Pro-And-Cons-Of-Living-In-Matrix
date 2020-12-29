import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from song_holder import *


class Scroll(Shape):
  
  def __init__(self, child, parent=None):
    super().__init__(parent)
    #================#
    self.child = child
    self.child.parent = self
    #================#
    self._surface = pygame.Surface(self.child._surface.get_size())
    #================#
    self._scroll_offset = (0, 0)
    self._scroll_step = 10
    #================#
    self.limit = (1e300, 1e300)


  @property
  def size(self):
    return self._surface.get_size()

  @size.setter
  def size(self, value):
    self._surface = pygame.surface.Surface(value).convert()

  def draw(self):
    self._sync_surface_size_if_needed()
    self._surface.blit(self.child.draw(), self._scroll_offset)
    return self._surface
    
  def _sync_surface_size_if_needed(self):
    child_surface_clipping_size = self.child._surface.get_rect().clip(pygame.Rect((0, 0), self.limit)).size
    scroll_surface_size = self._surface.get_rect().size
    if child_surface_clipping_size != scroll_surface_size:
      self._surface = pygame.Surface(child_surface_clipping_size)
    
  def process(self, events):
    self.child.process(events)
    for e in events:
      if e.type == KEYDOWN and e.key == K_DOWN:
        self._scroll_offset = tuple_math(self._scroll_offset, '+', (0, -self._scroll_step))
      if e.type == KEYDOWN and e.key == K_UP:
        self._scroll_offset = tuple_math(self._scroll_offset, '+', (0, self._scroll_step))
      if e.type == KEYDOWN and e.key == K_LEFT:
        self._scroll_offset = tuple_math(self._scroll_offset, '+', (-self._scroll_step, 0))
      if e.type == KEYDOWN and e.key == K_RIGHT:
        self._scroll_offset = tuple_math(self._scroll_offset, '+', (self._scroll_step, 0))


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  
  #================#
  song_holder_scroller = Scroll(SongHolder(background_color=WHITE))
  song_holder_scroller.position = screen.get_rect().center
  song_holder_scroller.pivot = (0.5, 0.5)
  song_holder_scroller.limit = tuple_math(SCREEN_SIZE, '/', (4, 4))

  song_holder_scroller.child.add_song_entry(SongEntry('You Cant Always Get What You Want', 'A1'))
  song_holder_scroller.child.add_song_entry(SongEntry('Sympathy For Devil', 'A2'))
  song_holder_scroller.child.add_song_entry(SongEntry('Another Break In The Wall', 'A3'))
  song_holder_scroller.child.add_song_entry(SongEntry('California Dreaming', 'B1'))
  song_holder_scroller.child.add_song_entry(SongEntry('No Woman No Cry', 'B2'))
  song_holder_scroller.child.add_song_entry(SongEntry('Voodoo Child', 'B3'))
  #================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()

    song_holder_scroller.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(song_holder_scroller.draw(), song_holder_scroller.world_space_rect.topleft)

    pygame.display.update()
