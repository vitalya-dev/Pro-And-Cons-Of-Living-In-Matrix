

import pygame
from pygame.locals import *

#================================================================#

#================================================================#


#================================================================#

#================================================================#


#================================================================#
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
#================================================================#


#================================================================#

#================================================================#


#================================================================#


class SongHolder(object):
  def __init__(self):
    self.position = (0, 0)
    self.pivot = (0, 0)
    self.song_entries_margin = 25
    self._song_entries = []
    self._surface = pygame.surface.Surface((0, 0)).convert()

  def add(self, song_entry):
    self._surface.set_colorkey((0, 0, 0))
    self._song_entries.append(song_entry)
    song_entry.render(self._surface)

  def _song_entries_total_height(self):
    if len(self._song_entries) > 0:
      song_entries_total_height = sum([song_entry.height for song_entry in self._song_entries])
      song_entries_total_height_with_margin = song_entries_total_height + self.song_entries_margin * (len(self._song_entries) - 1)
      return song_entries_total_height_with_margin
    else:
      return 0

  def _song_entries_max_width(self):
    if len(self._song_entries) > 0:
      return max([song_entry.width for song_entry in self._song_entries])
    else:
      return 0

  def _resize_surface(self):
    self._surface = pygame.surface.Surface((self._song_entries_max_width(), self._song_entries_total_height())).convert()
    self._surface.set_colorkey((0, 0, 0))

  def process(self, events):
    pass

  def render(self, surface):
    surface.blit(self._surface, self._top_left_position())

  def _top_left_position(self):
    pivot_position = tuple_math(self.pivot, '*', self._surface.get_size())
    pivot_position_as_int = tuple(map(int, pivot_position))
    return tuple_math(self.position, '-', pivot_position_as_int)

  


class SongEntry(object):
  def __init__(self, name, id):
    self.name = name
    self.id = id
    self.position = (0, 0)
    self.pivot = (0, 0)
    #================#
    self._song_name_foreground_color = pygame.Color('#b99559')
    self._song_id_foreground_color = pygame.Color('#b82e0a')
    self._background_color = pygame.Color('#efe8b4')
    self._border_color = pygame.Color('#767877')
    #================#
    self._song_name_font = pygame.font.Font('data/FSEX300.ttf', 24)
    self._song_id_font = pygame.font.Font('data/FSEX300.ttf', 64)
    self._rendered_song_name = self._song_name_font.render(self.name, False, self._song_name_foreground_color)
    self._rendered_song_id = self._song_id_font.render(self.id, False, self._song_id_foreground_color)
    #================#
    self._surface = pygame.surface.Surface(self._calculate_surface_size())
    self._surface.fill(self._background_color)
  
  def _calculate_surface_size(self):
    size_for_name = self._rendered_song_name.get_size()
    size_for_name_and_id = tuple_math(size_for_name, '+', (0, 48))
    size_for_name_and_id_with_margin = tuple_math(size_for_name_and_id, '+', (12, 0))
    return size_for_name_and_id_with_margin

  def _top_left_position(self):
    pivot_position = tuple_math(self.pivot, '*', self._surface.get_size())
    pivot_position_as_int = tuple(map(int, pivot_position))
    return tuple_math(self.position, '-', pivot_position_as_int)

  def process(self, events):
    pass

  def render(self, surface):
    self._surface.blit(self._rendered_song_name, self._rendered_song_name_position())
    self._surface.blit(self._rendered_song_id, self._rendered_song_id_position())
    surface.blit(self._surface, self._top_left_position())

  def _rendered_song_name_position(self):
    return (6, 6)

  def _rendered_song_id_position(self):
    return (6, 16)

#================================================================#



#================================================================#
if __name__ == '__main__':
  #================#
  keyboard = Keyboard()
  keyboard.on_esc += [lambda: done(True)]
  #================#
  selector_switch = SelectorSwitch()
  selector_switch.position = screen.get_rect().center
  selector_switch.pivot = (0.5, 0.5)
  for i in 'ABCDEF':
    selector_switch.add_horizontal_switch_button(i) 
  selector_switch.add_vertical_switch_button('SELECT')
  for i in '123456':
    selector_switch.add_horizontal_switch_button(i) 
  #================#
  song_holder = SongHolder()
  song_holder.add(SongEntry('You Cant Always Get What You Want', 'A1'))

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    keyboard.process(events)
    selector_switch.process(events)
    song_holder.process(events)
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    selector_switch.render(screen)
    song_holder.render(screen)
    pygame.display.update()

