import pygame
from pygame.locals import *


#================================================================#
SCREEN_SIZE = (640, 480)
FONT_SIZE   = 32
#================================================================#


#================================================================#
pygame.init()
#================================================================#

#================================================================#
screen     = pygame.display.set_mode(SCREEN_SIZE)
clock      = pygame.time.Clock()
font       = pygame.font.Font('data/FSEX300.ttf', FONT_SIZE - 1)
#================================================================#

#================================================================#
def done(val=None):
  if not hasattr(done, 'val'): done.val = False
  if val == None: return done.val
  done.val = val;

def scale(l, x):
  return tuple(map(lambda e: e * x, l)) if type(l) == type(tuple()) else list(map(lambda e: e * x, l))
#================================================================#


mr_pleasant_image = pygame.image.load("graphics/mr_pleasant_1.png").convert_alpha()
mr_pleasant_image = pygame.transform.scale(mr_pleasant_image, scale(mr_pleasant_image.get_size(), 15))

screen.fill(pygame.Color('#000000'))
screen.blit(mr_pleasant_image, (0, 0))

if __name__ == '__main__':
  while not done():
    #PROCESS INPUT
    events = pygame.event.get()
    #RENDER

    pygame.display.update()
