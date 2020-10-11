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
    if l(j): return i
  return -1
      
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

def subtract(a, b):
  from operator import sub
  if type(a) == type(b) == type(tuple()):
    return tuple(map(sub, a, b))
#================================================================#


#================================================================#
def button(text, background, foreground):
  background = pygame.Color(background) if type(background) == type('') else background
  foreground = pygame.Color(foreground) if type(foreground) == type('') else foreground
  return font.render(text, False, foreground, background)

def label(text, background, foreground, size=None):
  background = pygame.Color(background) if type(background) == type('') else background
  foreground = pygame.Color(foreground) if type(foreground) == type('') else foreground
  #==============#
  font_surface = font.render(text, False, foreground)
  if size == None: rect = font_surface.get_size()
  label_surface = pygame.surface.Surface(size).convert()
  #==============#
  label_surface.fill(background)
  label_surface.blit(font_surface, subtract(label_surface.get_rect().center, font_surface.get_rect().center))
  return label_surface
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


class MidiKeys(object):
  def __init__(self, messages):
    self.beats  = Beats(messages)
    self.output = mido.open_output(None)

  def process(self, events):
    keys_down = pygame.key.get_pressed()
    for e in events:
      if e.type == KEYDOWN:
        self.output.send(mido.Message('note_on', note=self.beats.note(e.key)))
      if e.type == KEYUP:
        self.output.send(mido.Message('note_off', note=self.beats.note(e.key)))

class Beats(object):
  def __init__(self, messages):
    self.beat_ons  =  [message for message in messages_to_abstime(messages) if message.type == 'note_on']
    self.beat_offs  = [message for message in messages_to_abstime(messages) if message.type == 'note_off']
    self.average_note = int(average([beat_on.note for beat_on in self.beat_ons]))
    self.note_to_key = {
      self.average_note:   'F',
      self.average_note-1: 'D',
      self.average_note-2: 'S',
      self.average_note-3: 'A',
      self.average_note+1: 'J',
      self.average_note+2: 'K',
      self.average_note+3: 'L'
    }

  def __iter__(self):
    beat_offs = self.beat_offs[:]
    for beat_on in self.beat_ons:
      i = find(beat_offs, lambda x: x.note == beat_on.note)
      if i >= 0:
        yield (beat_on, beat_offs.pop(i))
        
  def time(self):
    return self.beat_offs[-1].time

  def key(self, beat):
    return self.note_to_key[beat.note]

  def note(self, key):
    key = chr(key) if type(key) == type(int()) else key
    key = key.upper()
    #=================#
    key_to_note = {key:note for note, key in self.note_to_key.items()}
    return key_to_note[key] if key in key_to_note else None

  
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
    beats = Beats(messages)
    #=================#
    scale_x = dim_in_pixels(cols=self.cols) / beats.time()
    for beat in beats:
      beat_height = 50
      beat_width  = (beat[1].time - beat[0].time) * scale_x - 1
      beat_left   = beat[0].time * scale_x
      beat_top    = (beats.average_note - beat[0].note) * beat_height + dim_in_pixels(rows=self.rows) / 2 - beat_height
      beat_key    = beats.key(beat[0])
      #=========#
      surface.blit(label(beat_key, self.foreground, self.background, (beat_width, beat_height)), (beat_left, beat_top))
#================================================================#


def play(messages):
  with mido.open_output(None) as output:
    for message in messages * 1:
      if timing(message) > 0.0: time.sleep(timing())
      output.send(message)

if __name__ == '__main__':
  window    = Window(MAX_COLS, MAX_ROWS, '#000080')
  midi_keys = MidiKeys(notes('Breath.mid'))

  window.on_esc = lambda: done(True)
  window.draw(Plot(MAX_COLS, MAX_ROWS, '#000080', '#55FF55').plot(notes('Breath.mid')), (0, 0))

  while not done():
    dt = clock.tick(60)
    #PROCESS
    events = pygame.event.get()
    window.process(events)
    midi_keys.process(events)
    #RENDER
    screen.blit(window.render(), dim_in_pixels(0, 0))
    #UPDATE
    pygame.display.update()


