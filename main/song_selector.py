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
    self.background_color = background_color
    #================#
    self._space_between_child = 15
    #================#
    self._numbers_box = self._create_numbers_box()
    self._select_switch = self._create_select_switch()
    self._letters_box = self._create_letters_box()
    #================#
    self._build_surface()
    #================#
    self._layout_elements()


  def _build_surface(self):
    self._surface = pygame.surface.Surface((self._calculate_surface_width(), self._calculate_surface_height())).convert()

  def _calculate_surface_width(self):
    surface_width = self._numbers_box.parent_space_rect.width
    surface_width += self._space_between_child
    surface_width += self._select_switch.parent_space_rect.width
    surface_width += self._space_between_child
    surface_width += self._letters_box.parent_space_rect.width
    return surface_width

  def _calculate_surface_height(self):
    return max(
      [self._numbers_box.parent_space_rect.height, self._letters_box.parent_space_rect.height, self._select_switch.parent_space_rect.height]
    )
    
  def _create_numbers_box(self):
    numbers_box = HorizontalBox(background_color=self.background_color, parent=self)
    for i in '123456':
      numbers_box.add_child(HorizontalSwitch(i))
    return numbers_box

  def _create_select_switch(self):
    select_switch = VerticalSwitch('SELECT', parent=self)
    return select_switch

  def _create_letters_box(self):
    letters_box = HorizontalBox(background_color=self.background_color, parent=self)
    for i in 'ABCDEF':
      letters_box.add_child(HorizontalSwitch(i))
      #================#
    return letters_box

  def _layout_elements(self):
    self._numbers_box.pivot  = (0, 0)
    self._numbers_box.position = self.self_space_rect.topleft
    #================#
    self._select_switch.pivot = (0.5, 0)
    self._select_switch.position = self.self_space_rect.midtop
    #================#
    self._letters_box.pivot = (1, 0)
    self._letters_box.position = self.self_space_rect.topright
    

  def process(self, events):
    self._numbers_box.process(events)
    self._letters_box.process(events)
    self._select_switch.process(events)

  def draw(self):
    self._surface.fill(self.background_color)
    #================#
    self._surface.blit(self._numbers_box.draw(), self._numbers_box.parent_space_rect.topleft)
    self._surface.blit(self._select_switch.draw(), self._select_switch.parent_space_rect.topleft)
    self._surface.blit(self._letters_box.draw(), self._letters_box.parent_space_rect.topleft)
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


