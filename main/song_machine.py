import pygame
from pygame.locals import *

from constants import *
from utils import *

from song_holder import *
from song_selector import *

EIGHTY_PERCENT = 0.8
FIFTEEN_PERCENT = 0.15

class SongMachine(Shape):
  def __init__(self, song_entries, size=SCREEN_SIZE, background_color=BLACK, parent=None):
    super().__init__(parent)
    #================#
    self.background_color = background_color
    #================#
    self._song_entries = song_entries
    #================#
    self._song_selector = SongSelector(
      size=tuple_math(size, '*', (1, FIFTEEN_PERCENT)),
      background_color=background_color,
      parent=self)
    self._song_selector.on_toggle.append(self._song_selector_on_toggle_handler)
    #================#
    self._song_holder = SongHolder(
      song_entries,
      size=tuple_math(size, '*', (1, EIGHTY_PERCENT)),
      background_color=background_color,
      parent=self
    )
    self._song_holder.scroll_area_size = 4
    #================#
    self._surface = pygame.surface.Surface(size).convert()
    #================#
    self._layout_elements()

  def _song_selector_on_toggle_handler(self, switch):
    if switch.is_on:
      self._song_holder_filter_entries(switch.text)
    else:
      self._song_holder_filter_entries('')

  def _song_holder_filter_entries(self, filter):
    filtered_entries = [song_entry for song_entry in self._song_entries if song_entry.name.casefold().startswith(filter.casefold())]
    self._song_holder.set_song_entries(filtered_entries)

  def _layout_elements(self):
    self._song_selector.pivot = (0.5, 0)
    self._song_selector.position = self._surface.get_rect().midtop
    #================#
    self._song_holder.pivot = (0.5, 1)
    self._song_holder.position = self._surface.get_rect().midbottom


  def process(self, events):
    self._song_selector.process(events)
    self._song_holder.process(events)

  def draw(self):
    self._surface.blit(self._song_selector.draw(), self._song_selector.parent_space_rect.topleft)
    self._surface.blit(self._song_holder.draw(), self._song_holder.parent_space_rect.topleft)
    return self._surface


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
    song_machine.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(song_machine.draw(), song_machine.world_space_rect.topleft)
    pygame.display.update()
