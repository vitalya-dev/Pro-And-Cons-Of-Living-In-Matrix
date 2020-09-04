import pygame
from pygame.locals import *

SCREEN_SIZE = (640, 480)

pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
font = pygame.font.Font('data/unispace bd.ttf', 32)



def button(text):
  btn = pygame.Surface((96, 32))
  btn.fill(pygame.Color('#57ffff'))
  btn.blit(font.render(text, False, pygame.Color('#000000')), (0, 0))
  return btn

def label(text):
  label = pygame.Surface((32, 32))
  label.blit(font.render(text, False, pygame.Color('#fefe03')), (0, 0))
  return label


main_window = pygame.surface.Surface(SCREEN_SIZE).convert()
main_window.fill(pygame.Color('#0000a8'))

pathbar = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()
pathbar.fill(pygame.Color('#fefe03'))

#================================================================#
buttonbar = pygame.surface.Surface((SCREEN_SIZE[0], 32)).convert()
buttonbar.fill(pygame.Color('#000000'))

buttonbar.blit(label('X'), (16 + 8, 0))
buttonbar.blit(button('Help'), (16 + 32, 0))

buttonbar.blit(label('Y'), (176 + 8, 0))
buttonbar.blit(button('Menu'), (176 + 32, 0))

buttonbar.blit(label('B'), (336 + 8, 0))
buttonbar.blit(button('Edit'), (336 + 32, 0))

buttonbar.blit(label('A'), (496 + 8, 0))
buttonbar.blit(button('View'), (496 + 32, 0))
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






