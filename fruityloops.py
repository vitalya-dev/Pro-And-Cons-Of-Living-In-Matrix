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

  def plot(self, messages):
    surface = pygame.surface.Surface(dim_in_pixels(self.cols, self.rows)).convert()
    surface.fill(self.background)
    self._draw(messages, surface)
    return surface

  def _draw(self, messages, surface):
    note_ons =  [message for message in messages_to_abstime(messages) if message.type == 'note_on']
    note_offs = [message for message in messages_to_abstime(messages) if message.type == 'note_off']
    #================================================================#
    scale_x = SCREEN_SIZE[0] / note_offs[-1].time
    average_note = average([note_on.note for note_on in note_ons])
    note_height = 50
    #================================================================#
    for note_on in note_ons:
      i, note_off = find(note_offs, lambda x: x.note == note_on.note)
      if note_off:
        left   = note_on.time * scale_x
        top    = (average_note - note_on.note) * note_height + SCREEN_SIZE[1] / 2
        width  = (note_off.time - note_on.time) * scale_x - 1
        height = note_height
        pygame.draw.rect(surface, self.foreground, (left, top, width, height), 0)
        #=======================#
        del(note_offs[i])

        
    
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

