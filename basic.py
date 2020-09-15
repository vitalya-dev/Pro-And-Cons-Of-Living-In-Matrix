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
#================================================================#


#================================================================#
def done(v=None):
  if not hasattr(done, 'val'): done.val = False
  if v == None: return done.val
  done.val = v;
  
def dim_in_pixels(cols, rows):
  return (cols * (int)(FONT_SIZE / 2), rows * FONT_SIZE)
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

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN: self.on_key_down(e)

  def on_key_down(self, e): pass

class Editor(Window):
  def __init__(self, cols, rows, color):
    super().__init__(cols, rows, color)
    self.text = [[]]
    self.x = 0
    self.y = 0

  def render(self):
    super().render()
    for i, line in enumerate(self.text):
      self.surface.blit(font.render("".join(line), False, pygame.Color('#c0c0c0')), dim_in_pixels(0, i))
    return self.surface

  def on_key_down(self, e):
    if e.key == K_ESCAPE:
      done(True)
    if e.key == K_SPACE:
      self.text[self.y] += ' '
      cursor_right()
    if e.key == K_BACKSPACE and self.x > 0:
      del(self.text[self.y][self.x-1])
      cursor_left()
    if e.key == K_BACKSPACE and self.x == 0:
      merge_line(self.y-1, self.y)
      del(self.text[self.y])
      #=======#
      cursor_up()
      cursor_beg_of_line()
    if e.key == K_RETURN:
      text_0 = self.text[self.y][0:self.x]
      text_1 = self.text[self.y][self.x:]
      #=======#
      self.text[self.y] = text_0
      self.text.insert(self.y+1, text_1)
      #=======#
      cursor_down()
      cursor_end_of_line()
    if e.unicode.isalpha():
      self.text[self.y] += e.unicode
      cursor_right()
    print(self.text)

#================================================================#

editor = Editor(MAX_COLS, MAX_ROWS, '#000080')

while not done():
  dt = clock.tick(60)
  #PROCESS
  events = pygame.event.get()
  editor.process(events)
  #RENDER
  screen.blit(editor.render(), (0, 0))
  #UPDATE
  pygame.display.update()
#================================================================#


pygame.quit()
quit()



