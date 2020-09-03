import pygame
from pygame.locals import *

SCREEN_SIZE = (640, 480)

pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

def button(text):
  btn = pygame.Surface((96, 32))
  btn.fill(pygame.Color('#57ffff'))
  return btn


main_window = pygame.surface.Surface(SCREEN_SIZE).convert()
main_window.fill(pygame.Color('#0000a8'))

pathbar = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()
pathbar.fill(pygame.Color('#fefe03'))

#================================================================#
help_button = button(help)
#================================================================#

#================================================================#
buttonbar = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()
buttonbar.fill(pygame.Color('#000000'))
buttonbar.blit(help_button, (32, 0))
#================================================================#

#================================================================#
main_window.blit(pathbar, (0, 0))
main_window.blit(buttonbar, (0, SCREEN_SIZE[1] - 32))
#================================================================#


while True:
  dt = clock.tick(60)
  #PROCESS
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      quit()
    if event.type == KEYDOWN:
      pygame.quit()
      quit()
  #RENDER
  screen.fill((0, 0, 0))
  screen.blit(main_window, (0, 0))
  #UPDATE
  pygame.display.update()






