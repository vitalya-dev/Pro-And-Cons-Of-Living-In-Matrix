import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *


class Button(Shape):
  def __init__(self, text, background_color=BLACK, text_color=GRAY, parent=None):
    super().__init__(parent)
    #================#
    self._padding = (4, 2)
    #================#
    self.state = 'Normal'
    #================#
    self.background_color = background_color
    self.text_color = text_color
    #================#
    self._when_button_in_normal_state_blending = (100, 100, 100)
    self._when_button_in_focus_state_blending = (200, 200, 200)
    self._when_button_in_pressed_state_blending = (250, 250, 250)
    #================#
    self._font = pygame.font.Font('fonts/FSEX300.ttf', 32)
    self._text = text
    self._rendered_text = self._font.render(self._text, False, self.text_color)
    #================#
    self._surface = pygame.surface.Surface(tuple_math(self._rendered_text.get_size(), '+', self.padding)).convert()
    #================#

  @property
  def text(self):
    return self._text

  @property
  def padding(self):
    return self._padding

  @padding.setter
  def padding(self, value):
    self._padding = value
    self._surface = pygame.surface.Surface(tuple_math(self._rendered_text.get_size(), '+', self.padding)).convert()

  def rotate(self, angle):
    self._surface = pygame.transform.rotate(self._surface, angle)
    self._rendered_text = pygame.transform.rotate(self._rendered_text, angle)

  def process(self, events):
    pass

  def draw(self):
    if self.state == 'Normal':
      self._draw_button_in_normal_state()
    elif self.state == 'Pressed':
      self._draw_button_in_pressed_state()
    elif self.state == 'Focus':
      self._draw_button_in_focus_state()
    return self._surface

  def _draw_button_in_normal_state(self):
    self._draw_background()
    self._draw_text()
    self._add_blending(self._when_button_in_normal_state_blending)

  def _draw_button_in_pressed_state(self):
    self._draw_background()
    self._draw_text()
    self._add_blending(self._when_button_in_pressed_state_blending)

  def _draw_button_in_focus_state(self):
    self._draw_background()
    self._draw_border()
    self._draw_text()
    self._add_blending(self._when_button_in_focus_state_blending)

  def _draw_border(self):
    pygame.draw.rect(self._surface, self.text_color, self._surface.get_rect(), 4)

  def _draw_background(self):
    self._surface.fill(self.background_color, self._surface.get_rect())


  def _draw_text(self):
    blit_center(self._surface, self._rendered_text)

  def _add_blending(self, blending):
    self._surface.fill(blending, self._surface.get_rect(), special_flags=pygame.BLEND_RGB_MULT)     


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  new_game_in_normal_state_1_btn = Button('New Game', background_color=RED, text_color=BLUE)
  new_game_in_normal_state_1_btn.state = 'Normal'
  new_game_in_normal_state_1_btn.pivot = (0.5, 0.5)
  new_game_in_normal_state_1_btn.position = tuple_math(screen.get_rect().center, '+', (0, 0 * 60))

  new_game_in_focus_state_btn = Button('New Game', background_color=RED, text_color=BLUE)
  new_game_in_focus_state_btn.state = 'Focus'
  new_game_in_focus_state_btn.pivot = (0.5, 0.5)
  new_game_in_focus_state_btn.position = tuple_math(screen.get_rect().center, '+', (0, 1 * 60))

  new_game_in_normal_state_2_btn = Button('New Game', background_color=RED, text_color=BLUE)
  new_game_in_normal_state_2_btn.state = 'Normal'
  new_game_in_normal_state_2_btn.pivot = (0.5, 0.5)
  new_game_in_normal_state_2_btn.position = tuple_math(screen.get_rect().center, '+', (0, 2 * 60))




  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    new_game_in_normal_state_1_btn.process(events)
    new_game_in_normal_state_2_btn.process(events)
    new_game_in_focus_state_btn.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(new_game_in_normal_state_1_btn.draw(), new_game_in_normal_state_1_btn.world_space_rect)
    screen.blit(new_game_in_focus_state_btn.draw(), new_game_in_focus_state_btn.world_space_rect)
    screen.blit(new_game_in_normal_state_2_btn.draw(), new_game_in_normal_state_2_btn.world_space_rect)

    pygame.display.update()
