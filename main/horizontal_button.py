import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class HorizontalButton(Shape):
  def __init__(self, text, background_color=BLACK, text_color=GRAY, parent=None):
    super().__init__(parent)
    #================#
    self._padding = (2, -2)
    #================#
    self._clicked = False
    #================#
    self.background_color = background_color
    self.text_color = text_color
    self.light_color = tuple_math(self.background_color, '*', (1.2, 1.2, 1.2))
    self.highlight_blend_color = (125, 125, 125)
    #================#
    self._font = pygame.font.Font('fonts/FSEX300.ttf', 32)
    self._text = text
    self._rendered_text = self._font.render(self._text, False, self.text_color)
    #================#
    self._surface = pygame.surface.Surface(tuple_math(self._rendered_text.get_size(), '+', self.padding)).convert()

  @property
  def padding(self):
    return self._padding

  @padding.setter
  def padding(self, value):
    self._padding = value
    self._surface = pygame.surface.Surface(tuple_math(self._rendered_text.get_size(), '+', self.padding)).convert()

  def process(self, events):
    for e in events:
      if e.type == MOUSEBUTTONDOWN:
        self._process_mouse_button_down_event(e)
      if e.type == MOUSEBUTTONUP:
        self._process_mouse_button_up_event(e)

  def _process_mouse_button_down_event(self, e):
    if self.world_space_rect.collidepoint(e.pos):
      self._clicked = True

  def _process_mouse_button_up_event(self, e):
    if self.world_space_rect.collidepoint(e.pos):
      self._clicked = False

  def rotate(self, angle):
    self._surface = pygame.transform.rotate(self._surface, angle)
    self._rendered_text = pygame.transform.rotate(self._rendered_text, angle)

  def draw(self):
    self._draw_background()
    self._draw_light()
    self._draw_text()
    if self._clicked:
      self._draw_highlight()
    return self._surface

  
  def _draw_background(self):
    self._surface.fill(self.background_color, self._surface.get_rect())


  def _draw_light(self):
    if not self._clicked:
      light_position = (0, self._surface.get_height() * 7.0 / 8.0)
      light_size = (self._surface.get_width(), self._surface.get_height() / 8.0)
      self._surface.fill(self.light_color, pygame.Rect(light_position, light_size))

  def _draw_text(self):
    self._surface.blit(self._rendered_text, self._rendered_text.get_rect(center=self._surface.get_rect().center).topleft)

  def _draw_highlight(self):
    self._surface.fill(self.highlight_blend_color, self._surface.get_rect(), special_flags=pygame.BLEND_RGB_ADD)     


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  a_btn = HorizontalButton('A')
  a_btn.pivot = (0, 0)
  a_btn.position = screen.get_rect().center

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    a_btn.process(events)
    #===========================================RENDER==================================================#
    screen.fill((0, 0, 0))
    screen.blit(a_btn.draw(), a_btn.world_space_rect.topleft)

    pygame.display.update()
