import os
import pygame
from pygame.locals import *
from pygame import mixer

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
#================================================================#


#================================================================#
def done(v=None):
  if not hasattr(done, 'val'): done.val = False
  if v == None: return done.val
  done.val = v;
  
def dim_in_pixels(cols, rows):
  return (cols * (int)(FONT_SIZE / 2), rows * FONT_SIZE)

def clamp(val, min, max):
  if val < min: return min
  if val > max: return max
  return val
#================================================================#




#================================================================#
class Window(object):
  def __init__(self, cols, rows, background):
    self.surface = pygame.surface.Surface(dim_in_pixels(cols, rows)).convert()
    self.background = pygame.Color(background)
    self.keys_down = pygame.key.get_pressed()
    self.draws = []

  def draw(self, s, c):
    self.draws.append({'surface': s, 'coord': c})

  def render(self):
    self.surface.fill(self.background)
    for d in self.draws:
      self.surface.blit(d['surface'], dim_in_pixels(*d['coord']))
    return self.surface

  def process(self, events):
    self.keys_down = pygame.key.get_pressed()
    for e in events:
      if e.type == KEYDOWN and e.key == K_ESCAPE and hasattr(self,  'on_esc'):    self.on_esc()
      if e.type == KEYDOWN and e.key == K_SPACE  and hasattr(self,  'on_space'):  self.on_space()

#================================================================#
mixer.init()
mixer.music.load('Live Outside Live Outside Of All Of This.mp3')
mixer.music.play()

window = Window(MAX_COLS, MAX_ROWS, '#000080')
window.on_esc   =   lambda: done(True)
window.on_space =   lambda: mixer.music.play()


while not done():
  dt = clock.tick(60)
  #PROCESS
  events = pygame.event.get()
  window.process(events)
  #RENDER
  screen.blit(window.render(),    dim_in_pixels(0, 0))
  #UPDATE
  pygame.display.update()
#================================================================#

pygame.quit()
quit()



