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

def clamp(val, min, max):
  if val < min: return min
  if val > max: return max
  return val
#================================================================#




#================================================================#
def button(text, background, foreground):
  btn = pygame.Surface((96, 32))
  btn.fill(background)
  btn.blit(font.render(text, False, foreground), (0, 0))
  return btn

def label(text, foreground):
  return font.render(text, False, pygame.Color(foreground))

def cursor(foreground):
  if not hasattr(cursor, 'blink'): cursor.blink = True
  if not hasattr(cursor, 'tick'): cursor.tick = pygame.time.get_ticks()
  #==========#
  if (pygame.time.get_ticks() - cursor.tick) > 100:
    cursor.blink = not cursor.blink
    cursor.tick = pygame.time.get_ticks()
  #==========#
  if cursor.blink:
    return font.render("_", False, foreground)
  else:
    return font.render("",  False, foreground)
#================================================================#



#================================================================#
class Window(object):
  def __init__(self, cols, rows, background):
    self.surface = pygame.surface.Surface(dim_in_pixels(cols, rows)).convert()
    self.background = pygame.Color(background)
    self.draws = []


  def draw(self, s, c):
    self.draws.append({'surface': s, 'coord': c})

  def render(self):
    self.surface.fill(self.background)
    for d in self.draws:
      self.surface.blit(d['surface'], dim_in_pixels(*d['coord']))
    return self.surface

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN: self.on_key_down(e)

  def on_key_down(self, e): pass

class Editor(Window):
  def __init__(self, cols, rows, background, foreground):
    super().__init__(cols, rows, background)
    self.foreground = pygame.Color(foreground)
    self.text = [[]]
    self.x = 0
    self.y = 0

  def render(self):
    super().render()
    for i, line in enumerate(self.text):
      self.surface.blit(font.render("".join(line), False, self.foreground), dim_in_pixels(0, i))
    self.surface.blit(cursor(self.foreground), dim_in_pixels(self.x, self.y))
    return self.surface

  def on_key_down(self, e):
    if e.key == K_ESCAPE:
      done(True)
    elif e.key == K_BACKSPACE and self.x > 0:
      del(self.text[self.y][self.x-1])
      self.cursor_left()
    elif e.key == K_BACKSPACE and self.x == 0 and self.y > 0:
      self.cursor_up()
      self.cursor_end_of_line()
      #=======#
      self.merge_lines(self.y, self.y+1)
    elif e.key == K_RETURN:
      text_0 = self.text[self.y][0:self.x]
      text_1 = self.text[self.y][self.x:]
      #=======#
      self.text[self.y] = text_0
      self.text.insert(self.y+1, text_1)
      #=======#
      self.cursor_down()
      self.cursor_beg_of_line()
    elif e.key == K_UP:
      self.cursor_up()
      self.x = clamp(self.x, 0, len(self.text[self.y]))
    elif e.key == K_DOWN:
      self.cursor_down()
      self.x = clamp(self.x, 0, len(self.text[self.y]))
    elif e.key == K_LEFT and self.x > 0:
      self.cursor_left()
    elif e.key == K_LEFT and self.x == 0 and self.y > 0:
      self.cursor_up()
      self.cursor_end_of_line()
    elif e.key == K_RIGHT:
      self.cursor_right()
    elif e.unicode != '' and e.unicode.isprintable():
      self.text[self.y].insert(self.x, e.unicode)
      self.cursor_right()

  def cursor_up(self):
    if self.y > 0:
      self.y -= 1

  def cursor_down(self):
    if self.y < len(self.text)-1:
      self.y += 1

  def cursor_right(self):
    if self.x in range(len(self.text[self.y])):
      self.x += 1

  def cursor_left(self):
    if self.x > 0:
      self.x -= 1

  def cursor_beg_of_line(self):
    self.x = 0
  
  def cursor_end_of_line(self):
    self.x = len(self.text[self.y])

  def merge_lines(self, y1, y2):
    if y1 in range(len(self.text)) and y2 in range(len(self.text)):
      self.text[y1] += self.text[y2]
      del(self.text[y2])

#================================================================#
editor = Editor(MAX_COLS, MAX_ROWS, '#000080', '#c0c0c0')

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

print(pygame.time.get_ticks())

pygame.quit()
quit()



