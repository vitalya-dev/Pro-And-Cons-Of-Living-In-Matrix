import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      quit()
    if event.type == KEYDOWN:
      pygame.quit()
      quit()
  dt = clock.tick(60)
  pygame.display.update()
