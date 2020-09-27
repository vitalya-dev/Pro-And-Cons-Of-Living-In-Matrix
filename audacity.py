import struct
import wave
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
def linspace(start, stop, num=50):
  delta = stop - start
  div = num - 1
  step = delta / div
  return [start + i * step for i in range(num)]

def read_whole(filename):
    SIZES = {1: 'B', 2: 'h', 4: 'i'}
    CHUNK_SIZE_4096 = 4096
    CHUNK_SIZE_1 = 1
    #======================#
    wav_r = wave.open(filename, 'r')
    #======================#
    channels  = wav_r.getnchannels()
    sampwidth = wav_r.getsampwidth()
    #======================#
    fmt_1 = "<" + SIZES[wav_r.getsampwidth()] * channels * CHUNK_SIZE_4096
    fmt_2 = "<" + SIZES[wav_r.getsampwidth()] * channels * CHUNK_SIZE_1
    #======================#
    ret = []
    while wav_r.tell() < wav_r.getnframes():
      if wav_r.getnframes() - wav_r.tell() >= CHUNK_SIZE_4096:
        decoded = struct.unpack(fmt_1, wav_r.readframes(CHUNK_SIZE_4096))
      else:
        decoded = struct.unpack(fmt_2, wav_r.readframes(CHUNK_SIZE_1))
      for i in decoded: ret.append(i)
    return ret


def dim_in_pixels(cols, rows):
  return (cols * (int)(FONT_SIZE / 2), rows * FONT_SIZE)


def done(v=None):
  if not hasattr(done, 'val'): done.val = False
  if v == None: return done.val
  done.val = v;
  
def clamp(val, min, max):
  if val < min: return min
  if val > max: return max
  return val
#================================================================#


#================================================================#
def button(text, background, foreground):
  return font.render(text, False, pygame.Color(foreground), pygame.Color(background))

def label(text, foreground):
  return font.render(text, False, pygame.Color(foreground))

def plot(xs, ys):
  surface = pygame.surface.Surface(dim_in_pixels(MAX_COLS, MAX_ROWS)).convert()
  #=============#
  scale_factor = (1/2 * MAX_ROWS) / max(abs(max(ys)), abs(min(ys)))
  normalize = lambda x, y: dim_in_pixels(x, MAX_ROWS / 2 - y * scale_factor)
  for i in range(0, len(xs)):
    pygame.draw.line(surface, pygame.Color('green'), normalize(xs[i], 0), normalize(xs[i], ys[i]), 1)
  #=============#
  return surface
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

window = Window(MAX_COLS, MAX_ROWS, '#000080')

data = read_whole("Live Ouside Instrumental 2.wav")

window.draw(plot(linspace(0, MAX_COLS, len(data)), data), (0, 0))

window.on_esc = lambda: done(True)


if __name__ == '__main__':
  while not done():
    dt = clock.tick(60)
    #PROCESS
    events = pygame.event.get()
    window.process(events)    
    #RENDER
    screen.blit(window.render(), dim_in_pixels(0, 0))
    #UPDATE
    pygame.display.update()
