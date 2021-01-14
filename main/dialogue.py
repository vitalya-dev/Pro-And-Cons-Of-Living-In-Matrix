import pygame
from pygame.locals import *

from globals import *
from constants import *
from utils import *

from keyboard import *

class Dialogue:
  
  @staticmethod
  def _draw_yes_no_dialog():
    print('draw draw draw')

  @staticmethod
  def show_yes_no_dialog():
    while (True):
      Dialogue._draw_yes_no_dialog()
      print(SCREEN)
      print(CLOCK)

if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  SCREEN = pygame.display.set_mode(SCREEN_SIZE)
  CLOCK = pygame.time.Clock()
  #================================================================================================#
  keyboard = Keyboard()
  keyboard.on_space += [lambda: Dialogue.show_yes_no_dialog()]
  #================================================================================================#

  while not done():
    CLOCK.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    keyboard.process(events)
    #===========================================RENDER==================================================#
    SCREEN.fill(WHITE)
    pygame.display.update()



