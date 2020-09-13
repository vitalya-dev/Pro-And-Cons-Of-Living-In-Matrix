import os
import pygame
from pygame.locals import *

#================================================================#
SCREEN_SIZE = (640, 480)
FONT_SIZE = 32
MAX_COLS = (int)(SCREEN_SIZE[0] / (FONT_SIZE / 2))
MAX_ROWS = (int)(SCREEN_SIZE[1] / FONT_SIZE)
#================================================================#


#================================================================#
pygame.init()
pygame.key.set_repeat(10, 75)
#================================================================#


#================================================================#
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.Font('data/FSEX300.ttf', FONT_SIZE - 1)
done = False
#================================================================#


#================================================================#
def dim_in_pixels(cols, rows):
  return (cols * (int)(FONT_SIZE / 2), rows * FONT_SIZE)

def esc_is_exit():
  global done
  for e in events:
    if e.type == QUIT:
      done = True
    if e.type == KEYDOWN and e.key == K_ESCAPE:
      done = True
#================================================================#




#================================================================#
def button(text):
  btn = pygame.Surface((96, 32))
  btn.fill(pygame.Color('#57ffff'))
  btn.blit(font.render(text, False, pygame.Color('#000000')), (0, 0))
  return btn

def label(text, color):
  return font.render(text, False, pygame.Color(color))
#================================================================#



#================================================================#
class Window(object):
  def __init__(self, cols, rows, color):
    self.surface = pygame.surface.Surface(dim_in_pixels(cols, rows)).convert()
    self.color = pygame.Color(color)
    self.draws = []


  def draw(self, s, c):
    self.draws.append({'surface': s, 'coord': c})

  def render(self):
    self.surface.fill(self.color)
    for d in self.draws:
      self.surface.blit(d['surface'], dim_in_pixels(*d['coord']))
    return self.surface

  def process(self, e):
    esc_is_exit()
#================================================================#

window = Window(MAX_COLS, MAX_ROWS, '#000080')
for i in range(MAX_ROWS):
  window.draw(label('*' * MAX_COLS, '#c0c0c0'), (0, i))


while not done:
  dt = clock.tick(60)
  #PROCESS
  events = pygame.event.get()
  window.process(events)
  #RENDER
  screen.blit(window.render(), (0, 0))
  #UPDATE
  pygame.display.update()
#================================================================#


pygame.quit()
quit()



