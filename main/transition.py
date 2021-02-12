import time

import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class Transition(Shape):
  def __init__(self, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self.fade_speed = 0
    #================#
    self.state = 'IDLE'
    #================#
    self._start_time_of_fade_in = 0
    self._start_time_of_fade_out = 0
    #================#
    self.primary_color = BLACK
    self.secondary_color = BLACK
    self.tertiary_color = BLACK
    self.quaternary_color = BLACK
    self.quinary_color = BLACK
    self.senary_color = BLACK
    self.septenary_color = BLACK
    self.octonary_color = BLACK
    #================#
    self._surface = pygame.surface.Surface(size).convert()

  def start(self):
    self._start_time_of_fade_in = time.time()
    self.state = 'FADE IN'

  def process(self, events):
    if self.state == 'FADE IN':
      self._fade_in_state(events)
    elif self.state == 'FADE OUT':
      self._fade_out_state(events)
  
  def _time_since(self, some_point_in_time):
    return time.time() - some_point_in_time

  def _fade_in_state(self, events):
    alpha = self._time_since(self._start_time_of_fade_in) * self.fade_speed
    if alpha < 255:
      self._surface.set_alpha(alpha)
    else:
      self._start_time_of_fade_out = time.time()
      self.state = 'FADE OUT'

  def _fade_out_state(self, events):
    alpha = 255 - self._time_since(self._start_time_of_fade_out) * self.fade_speed
    if alpha > 0:
      self._surface.set_alpha(alpha)
    else:
      self.state = 'IDLE'

  def draw(self):
    self._surface.fill(self.primary_color)
    return self._surface

if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  #================#
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  transition = Transition()
  transition.fade_speed = 80
  transition.primary_color=BLACK
  transition.start()
  #================================================================================================#
  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    transition.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(transition.draw(), transition.world_space_rect)
    pygame.display.update()
    
