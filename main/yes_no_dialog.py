import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from button import *
from label import *

class YesNoDialog(Shape):
  def __init__(self, background_color=BLACK, foreground_color=WHITE, text_color=GRAY, parent=None):
    super().__init__(parent)
    #================#
    self._message = Label(
      text='Are you sure?',
      background_color=background_color,
      text_color=text_color,
      size=self._calculate_message_size(),
      parent=self
    )
    self._yes_btn = Button('Yes', background_color=foreground_color, text_color=text_color, parent=self)
    self._no_btn = Button('No', background_color=foreground_color, text_color=text_color, parent=self)
    #================#
    self._yes_btn.state = 'Focus'
    #================#
    self.background_color = background_color
    #================#
    self._surface = pygame.surface.Surface(self._calculate_surface_size())
    #================#
    self._layout_elements()

  def _layout_elements(self):
    self._message.pivot = (0, 0)
    self._message.position = self._surface.get_rect().topleft
    #================#
    self._yes_btn.pivot = (1, 1)
    self._yes_btn.position = self._surface.get_rect().midbottom
    #================#
    self._no_btn.pivot = (0, 1)
    self._no_btn.position = self._surface.get_rect().midbottom
    #================#
    self._yes_btn.move(-10, 0)
    self._no_btn.move(10, 0)


  def _calculate_message_size(self):
    return tuple_math(self._calculate_surface_size(), '*', (1, 0.7))

  def _calculate_surface_size(self):
    return tuple_math(SCREEN_SIZE, '/', (2, 4))

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and e.key == K_LEFT:
        self._proces_key_left_event()
      if e.type == KEYDOWN and e.key == K_RIGHT:
        self._proces_key_right_event()

  def _proces_key_right_event(self):
    self._cycle_focus()

  def _proces_key_left_event(self):
    self._cycle_focus()

  def _cycle_focus(self):
    for button in [self._yes_btn, self._no_btn]:
      if button.state == 'Focus': button.state = 'Normal'
      elif button.state == 'Normal': button.state = 'Focus'

  def draw(self):
    self._surface.blit(self._message.draw(), self._message.parent_space_rect)
    self._surface.blit(self._yes_btn.draw(), self._yes_btn.parent_space_rect)
    self._surface.blit(self._no_btn.draw(), self._no_btn.parent_space_rect)
    return self._surface


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  yes_no_dialog = YesNoDialog()
  yes_no_dialog.pivot = (0.5, 0.5)
  yes_no_dialog.position = screen.get_rect().center
  

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    yes_no_dialog.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(yes_no_dialog.draw(), yes_no_dialog.world_space_rect)
    pygame.display.update()
  
