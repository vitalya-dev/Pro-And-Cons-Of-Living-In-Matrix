import pygame
from pygame.locals import *

SCREEN_SIZE = (640, 480)


pygame.init()
screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()

background = pygame.surface.Surface(SCREEN_SIZE).convert()
background.fill(pygame.Color('#0000a8'))



while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      quit()
    if event.type == KEYDOWN:
      pygame.quit()
      quit()
  screen.blit(background, (0, 0))
  pygame.display.update()

  dt = clock.tick(60)

