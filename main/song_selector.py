import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from horizontal_box import *
from horizontal_switch import *
from vertical_switch import *

class SongSelector(Shape):
  def __init__(self, background_color=BLACK, parent=None):
    super().__init__()
    #================#
    self.on_toggle = []
    #================#
    self.background_color = background_color
    #================#
    self._letters_first_row = self._create_letters_first_row()
    self._letters_second_row = self._create_letters_second_row()
    #================#
    self._space_between_rows = 15
    #================#
    self._build_surface()
    #================#
    self._layout_elements()

  def _build_surface(self):
    self._surface = pygame.surface.Surface((self._calculate_surface_width(), self._calculate_surface_height())).convert()

  def _calculate_surface_width(self):
    return max(self._letters_first_row.width, self._letters_second_row.width)

  def _calculate_surface_height(self):
    return self._letters_first_row.height + self._space_between_rows + self._letters_second_row.height
    
  def _create_letters_first_row(self):
    letters_first_row = HorizontalBox(background_color=self.background_color, parent=self)
    for i in 'ABCDEFGHIJKLM':
      letters_first_row.add_child(HorizontalSwitch(i))
      #================#
    return letters_first_row

  def _create_letters_second_row(self):
    letters_second_row = HorizontalBox(background_color=self.background_color, parent=self)
    for i in 'NOPQRSTUVWXYZ':
      letters_second_row.add_child(HorizontalSwitch(i))
      #================#
    return letters_second_row

  def _layout_elements(self):
    self._letters_first_row.pivot = (0, 0)
    self._letters_first_row.position = self.self_space_rect.topleft
    #================#
    self._letters_second_row.pivot = (0, 1)
    self._letters_second_row.position = self.self_space_rect.bottomleft

  def process(self, events):
    self._letters_first_row.process(events)
    self._letters_second_row.process(events)
    #================#
    for e in events:
      if e.type == KEYDOWN: self._process_keydown_event(e)

  def _process_keydown_event(self, e):
    keydown = chr(e.key)
    if keydown in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.casefold():
      self._toggle_letter_switch(keydown)

  def _toggle_letter_switch(self, key_pressed):
    for switch in self._letters_first_row.childs + self._letters_second_row.childs:
      if switch.text.casefold() == key_pressed.casefold():
        switch.toggle()
        for f in self.on_toggle: f(switch)

  def draw(self):
    self._surface.fill(self.background_color)
    #================#
    self._surface.blit(self._letters_first_row.draw(), self._letters_first_row.parent_space_rect.topleft)
    self._surface.blit(self._letters_second_row.draw(), self._letters_second_row.parent_space_rect.topleft)
    #================#
    return self._surface


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  
  #================#
  song_selector = SongSelector()
  song_selector.position = screen.get_rect().center
  song_selector.pivot = (0.5, 0.5)
  #================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    song_selector.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(song_selector.draw(), song_selector.world_space_rect.topleft)

    pygame.display.update()


