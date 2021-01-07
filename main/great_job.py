import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *


class GreatJob(Shape):
  def __init__(self, size=SCREEN_SIZE, background_color=WHITE, parent=None):
    super().__init__(parent)
    #================#
    self.background_color = background_color
    self.backgrond_image = pygame.image.load('images/great_job.png').convert_alpha()
    self.backgrond_image = pygame.transform.scale(self.backgrond_image, size)
    #================#
    self._surface = pygame.surface.Surface(size).convert()

  def process(self, events):
    pass

  def draw(self):
    self._surface.fill(self.background_color)
    blit_center(target=self._surface, source=self.backgrond_image)
    return self._surface


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  great_job = GreatJob(background_color=PINK)

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    great_job.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(great_job.draw(), great_job.world_space_rect.topleft)
    pygame.display.update()

