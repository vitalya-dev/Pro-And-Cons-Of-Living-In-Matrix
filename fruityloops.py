#!/usr/bin/env python
"""
Play MIDI file on output port.
Run with (for example):
    ./play_midi_file.py 'SH-201 MIDI 1' 'test.mid'
"""
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
    self._time = 0

  def plot(self, notes):
    surface = pygame.surface.Surface(dim_in_pixels(self.cols, self.rows)).convert()
    surface.fill(self.background)
    for note in notes:
      self._draw(note, surface)
    return surface

  def _draw(self, note, surface):
    self._time += note.time
    print(note)
    if note.type == 'note_off': pygame.draw.rect(surface, self.foreground, ((self._time - note.time) * 150, (note.note - 50) * 15, 25, 12), 0)

#================================================================#


if __name__ == '__main__':
  window = Window(MAX_COLS, MAX_ROWS, '#000080')
  window.on_esc = lambda: done(True)
  
  window.draw(Plot(MAX_COLS, MAX_ROWS, '#000080', 'green').plot(notes('Breath.mid')), (0, 0))

  while not done():
    dt = clock.tick(60)
    #PROCESS
    events = pygame.event.get()
    window.process(events)
    #RENDER
    screen.blit(window.render(), dim_in_pixels(0, 0))
    #UPDATE
    pygame.display.update()

