import os
import pygame
from pygame.locals import *

#================================================================#
SCREEN_SIZE = (640, 480)
#================================================================#


#================================================================#
def button(text):
  btn = pygame.Surface((96, 32))
  btn.fill(pygame.Color('#57ffff'))
  btn.blit(font.render(text, False, pygame.Color('#000000')), (0, 0))
  return btn

def label(text, color):
  return font.render(text, False, color)
#================================================================#



#================================================================#
pygame.init()
pygame.key.set_repeat(10, 75)



#================================================================#
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
font = pygame.font.Font('data/unispace bd.ttf', 32)
done = False
#================================================================#




#================================================================#
while not done:
  dt = clock.tick(60)
  #PROCESS
  events = pygame.event.get()
  for e in events:
    if e.type == QUIT:
      done = True
    if e.type == KEYDOWN and e.key == K_ESCAPE:
      done = True
  #RENDER
  #
  #
  #
  #UPDATE
  pygame.display.update()
#================================================================#
pygame.quit()
quit()



