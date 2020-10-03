import threading
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

def read_wav(filename):
    wav_r = wave.open(filename, 'r')
    #======================#
    sampwidth =  wav_r.getsampwidth()
    nframes   =  wav_r.getnframes()
    nchannels =  wav_r.getnchannels()
    #======================#
    while wav_r.getnframes() - wav_r.tell():
      chunk_size = int(nframes / 10) if wav_r.getnframes() - wav_r.tell() >= int(nframes / 10) else wav_r.getnframes() - wav_r.tell()
      data = struct.unpack(
        '<{0}{1}'.format(chunk_size * nchannels, {1: 'B', 2: 'h', 4: 'i'}[sampwidth]), wav_r.readframes(chunk_size)
      )
      yield data if nchannels == 1 else [j for i, j in enumerate(data) if i % 2 == 0]
    

def dim_in_pixels(cols=None, rows=None):
  if cols == None:
    return rows * FONT_SIZE
  elif rows == None:
    return cols * (int)(FONT_SIZE / 2)
  else:
    return (cols * (int)(FONT_SIZE / 2), rows * FONT_SIZE)

def done(v=None):
  if not hasattr(done, 'val'): done.val = False
  if v == None: return done.val
  done.val = v;

def clamp(val, min, max):
  if val < min: return min
  if val > max: return max
  return val

def average(l):
  return sum(l) / len(l)

def maxabs(l):
  return max(l) if max(l) > abs(min(l)) else min(l)
#================================================================#


#================================================================#
def button(text, background, foreground):
  background = pygame.Color(background) if type(background) == type('') else background
  foreground = pygame.Color(foreground) if type(foreground) == type('') else foreground
  return font.render(text, False, foreground, background)

def label(text, foreground):
  foreground = pygame.Color(foreground) if type(foreground) == type('') else foreground
  return font.render(text, False, foreground)

def loading(foreground):
  if not hasattr(loading, 'tick'): loading.tick = 0
  loading.tick +=1
  return label('Loading' + '.' * loading.tick, foreground)
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

class Plot(object):
  def __init__(self, cols, rows, background, foreground):
    self.cols = cols
    self.rows = rows
    self.background = pygame.Color(background)
    self.foreground = pygame.Color(foreground)

  def plot(self, data):
    surface = pygame.surface.Surface(dim_in_pixels(self.cols, self.rows)).convert()
    surface.fill(self.background)
    threading.Thread(target=self._plot_thread, args=(surface, data,)).start()
    return surface

  def _plot_thread(self, surface, data_loader):
    data = self._loading(data_loader, lambda:surface.blit(loading(self.foreground), dim_in_pixels(0, self.rows / 2)))
    data = self._scale_x(data)
    data = self._scale_y(data)

    surface.fill(self.background)
    for x, y in zip(linspace(0, self.cols, len(data)), data):
      pygame.draw.line(surface, self.foreground, dim_in_pixels(x, self.rows / 2), dim_in_pixels(x, (self.rows - y) / 2), 1)
    
  def _loading(self, data_loader, notify=None):
    data = []
    for chunk in data_loader:
      data += chunk
      if notify: notify()
    return data

  def _scale_x(self, data):
    scale = int(len(data) / (self.cols * 500))
    return [average(data[x:x+scale]) for x in range(0, len(data), scale)] if scale > 1 else data

  def _scale_y(self, data):
    scale = self.rows / max(abs(max(data)), abs(min(data)))
    return [y * scale for y in data]
#================================================================#

if __name__ == '__main__':
  window = Window(MAX_COLS, MAX_ROWS, '#000080')
  window.on_esc = lambda: done(True)
  window.draw(Plot(MAX_COLS, MAX_ROWS, '#000080', 'green').plot(read_wav("Live Ouside Instrumental.wav")), (0, 0))

  while not done():
    dt = clock.tick(60)
    #PROCESS
    events = pygame.event.get()
    window.process(events)
    #RENDER
    screen.blit(window.render(), dim_in_pixels(0, 0))
    #UPDATE
    pygame.display.update()


