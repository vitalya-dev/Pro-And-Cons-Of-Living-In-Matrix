#!/usr/bin/env python
"""
Play MIDI file on output port.
Run with (for example):
    ./play_midi_file.py 'SH-201 MIDI 1' 'test.mid'
"""
import threading
import time
import sys
import mido

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
def notes(midifile):
  return [message for message in mido.MidiFile(midifile) if message.type == 'note_on' or message.type == 'note_off']

def messages_to_abstime(messages):
  now = 0
  for msg in messages:
    now += msg.time
    yield msg.copy(time=now)

def find(lst, l):
  for i, j in enumerate(lst):
    if l(j): return (i, j)
  return (None, None)
      
def playback():
  if not hasattr(playback, 'start'): playback.start = time.time()
  return time.time() - playback.start

def timing(note=None):
  if not hasattr(timing, 'time'): timing.time = 0.0
  #===============#
  timing.time += note.time if note else 0.0
  #===============#
  return timing.time - playback()

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

def average(l):
  return sum(l) / len(l)
#================================================================#


#================================================================#
def button(text, background, foreground):
  background = pygame.Color(background) if type(background) == type('') else background
  foreground = pygame.Color(foreground) if type(foreground) == type('') else foreground
  return font.render(text, False, foreground, background)

def label(text, foreground):
  foreground = pygame.Color(foreground) if type(foreground) == type('') else foreground
  return font.render(text, False, foreground)
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


class Beat(object):
  def __init__(self, cols, rows, beat_ons, beat_offs):
    self.cols  = cols
    self.rows  = rows
    self.scale = dim_in_pixels(cols=cols) / beat_offs[-1].time
    self.average_beat = average([beat_on.note for beat_on in beat_ons])
    self.beat_height = 50

  def rect(self, beat_on, beat_off):
    left  = beat_on.time * self.scale
    top   = (self.average_beat  - beat_on.note) * self.beat_height + dim_in_pixels(rows=self.rows) / 2
    width = (beat_off.time - beat_on.time) * self.scale - 1
    #=============#
    return pygame.Rect(left, top, width, self.beat_height)
  
class Plot(object):
  def __init__(self, cols, rows, background, foreground):
    self.cols = cols
    self.rows = rows
    self.background = pygame.Color(background)
    self.foreground = pygame.Color(foreground)

  def plot(self, messages):
    surface = pygame.surface.Surface(dim_in_pixels(self.cols, self.rows)).convert()
    surface.fill(self.background)
    self._draw(messages, surface)
    return surface

  def _draw(self, messages, surface):
    beat_ons  = [message for message in messages_to_abstime(messages) if message.type == 'note_on']
    beat_offs = [message for message in messages_to_abstime(messages) if message.type == 'note_off']
    beat      = Beat(self.cols, self.rows, beat_ons, beat_offs)
    #=============#
    for beat_on in beat_ons:
      i, beat_off = find(beat_offs, lambda x: x.note == beat_on.note)
      if beat_off:
        pygame.draw.rect(surface, self.foreground, beat.rect(beat_on, beat_off), 0)
        del(beat_offs[i])
#================================================================#


def play(messages):
  with mido.open_output(None) as output:
    for message in messages * 10:
      if timing(message) > 0.0: time.sleep(timing())
      output.send(message)

if __name__ == '__main__':
  window = Window(MAX_COLS, MAX_ROWS, '#000080')
  window.on_esc = lambda: done(True)

  window.draw(Plot(MAX_COLS, MAX_ROWS, '#000080', '#55FF55').plot(notes('Breath.mid')), (0, 0))
  threading.Thread(target=play, args=(notes('Breath.mid'),)).start()

  while not done():
    dt = clock.tick(60)
    #PROCESS
    events = pygame.event.get()
    window.process(events)
    #RENDER
    screen.blit(window.render(), dim_in_pixels(0, 0))
    #UPDATE
    pygame.display.update()


