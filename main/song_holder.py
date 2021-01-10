import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from song_entry import *

class SongHolder(Shape):
  def __init__(self, song_entries, size=SCREEN_SIZE, background_color=BLACK, parent=None):
    super().__init__(parent)
    #================#
    self.background_color = background_color
    self.highlight_blend_color = (125, 125, 125)
    #================#
    self._song_entries = song_entries
    self._space_between_song_entries = 15
    #================#
    self._scroll_area = [0, 5]
    #================#
    self._current_selection = 0
    #================#
    self._parent_song_entries()
    self._layout_song_entries_in_scroll_area()
    #================#
    self._surface = pygame.surface.Surface(size).convert()

  def _parent_song_entries(self):
    for song_entry in self._song_entries:
      song_entry.parent = self

  def _layout_song_entries_in_scroll_area(self):
    song_entries_in_scroll_area = self._song_entries[self._scroll_area[0]:self._scroll_area[1]]
    for i, song_entry in enumerate(song_entries_in_scroll_area):
      if i > 0:
        previous_song_entry = song_entries_in_scroll_area[i-1]
        song_entry_position = tuple_math(previous_song_entry.parent_space_rect.bottomleft, '+', (0, self._space_between_song_entries))
      else:
        song_entry_position = (0, 0)
      song_entry.position = song_entry_position

  def draw(self):
    self._draw_background()
    self._draw_song_entries_in_scroll_area()
    self._highlight_current_selection_in_scroll_area()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self.background_color)

  def _draw_song_entries_in_scroll_area(self):
    song_entries_in_scroll_area = self._song_entries[self._scroll_area[0]:self._scroll_area[1]]
    for song_entry in song_entries_in_scroll_area:
      self._surface.blit(song_entry.draw(), song_entry.parent_space_rect.topleft)

  def _highlight_current_selection_in_scroll_area(self):
    song_entries_in_scroll_area = self._song_entries[self._scroll_area[0]:self._scroll_area[1]]
    if len(song_entries_in_scroll_area) > 0:
      selected_song_entry = song_entries_in_scroll_area[self._current_selection]
      self._surface.fill(self.highlight_blend_color, selected_song_entry.parent_space_rect, special_flags=pygame.BLEND_RGB_ADD)     

  def process(self, events):
    self._propogate_to_song_entries(events)
    for e in events:
      if e.type == KEYDOWN and e.key == K_DOWN and len(self._song_entries) > 0:
        self._scroll_down()
      if e.type == KEYDOWN and e.key == K_UP and len(self._song_entries) > 0:
        self._scroll_up()

  @property
  def scroll_area_size(self):
    return self._scroll_area[1] - self._scroll_area[0]

  @scroll_area_size.setter
  def scroll_area_size(self, value):
    self._scroll_area = [0, value]
    

  def _scroll_down(self):
    if self._current_selection < self.scroll_area_size - 1:
      self._current_selection += 1
    else:
      self._scroll_down_area()
    #================#
    self._layout_song_entries_in_scroll_area()

  def _scroll_down_area(self):
    if self._scroll_area[1] < len(self._song_entries):
      self._scroll_area[0] += 1
      self._scroll_area[1] += 1

  def _scroll_up(self):
    if self._current_selection > 0:
      self._current_selection -= 1
    else:
      self._scroll_up_area()
    #================#
    self._layout_song_entries_in_scroll_area()

  def _scroll_up_area(self):
    if self._scroll_area[0] > 0:
      self._scroll_area[0] -= 1
      self._scroll_area[1] -= 1


  def _propogate_to_song_entries(self, events):
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
    SongEntry('Voodoo People')
  ]
  song_holder = SongHolder(song_entries, background_color=WHITE)
  song_holder.position = screen.get_rect().midtop
  song_holder.pivot = (0.5, 0)


  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    song_holder.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(song_holder.draw(), song_holder.world_space_rect.topleft)

    pygame.display.update()

      
