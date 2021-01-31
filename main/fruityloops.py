import pygame
from pygame.locals import *

from constants import *
from utils import *
 
from shape import *

class Fruityloops(Shape):
  pass
      
if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    pygame.display.update()
