#git show 8f98340e744d7c967c8faf71cedd320039c6befd:fruityloops.py | clip

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
def find(lst, l):
  for i, j in enumerate(lst):
    if l(j): return i, j
  return -1, None

def average(l):
  return sum(l) / len(l)

def subtract(a, b):
  from operator import sub
  if type(a) == type(b) == type(tuple()):
    return tuple(map(sub, a, b))

def done(val=None):
  if not hasattr(done, 'val'): done.val = False
  if val == None: return done.val
  done.val = val;

def messages_to_abstime(messages):
  now = 0
  for message in messages:
    now += message.time
    yield message.copy(time=now)

def read_midi(midifile):
  return list(mido.MidiFile(midifile))

def generate_keys(beats):
  middle_note = beats.middle_note()
  return {
    'F': middle_note,
    'D': middle_note-1,
    'S': middle_note-2,
    'A': middle_note-3,
    'J': middle_note+1,
    'K': middle_note+2,
    'L': middle_note+3,
  }
#================================================================#


#================================================================#
def label(text, background, foreground, size=None):
  background = pygame.Color(background) if type(background) == type('') else background
  foreground = pygame.Color(foreground) if type(foreground) == type('') else foreground
  #==============#
  font_surface  = font.render(text, False, foreground)
  label_surface = pygame.surface.Surface(size if size else font_surface.get_size()).convert()
  #==============#
  label_surface.fill(background)
  label_surface.blit(font_surface, subtract(label_surface.get_rect().center, font_surface.get_rect().center))
  return label_surface
#================================================================#

#================================================================#
class Beats(object):
  def __init__(self, messages):
    self.beat_ons    =  [message for message in messages_to_abstime(messages) if message.type == 'note_on']
    self.beat_offs   =  [message for message in messages_to_abstime(messages) if message.type == 'note_off']
  
  def middle_note(self):
    return int(average([beat_on.note for beat_on in self.beat_ons]))

  def duration(self):
    return self.beat_offs[-1].time

  def __iter__(self):
    beat_offs = self.beat_offs[:]
    for beat_on in self.beat_ons:
      i = find(beat_offs, lambda x: x.note == beat_on.note)[0]
      if i >= 0:
        yield (beat_on, beat_offs.pop(i))

  def __str__(self):
    return str(list(self))

class Progression:
  def __init__(self, prog):
    self.prog = prog
    self._current = 0

  def current(self):
    return self.prog[self._current]

  def next(self):
    self._current = (self._current + 1) % len(self.prog)


class Piano(object):
  def __init__(self, keys):
    self.output = mido.open_output(None)
    self.keys = keys

  def process(self, events):
    keys_down = pygame.key.get_pressed()
    for e in events:
      if e.type == KEYDOWN and chr(e.key).upper() in self.keys:
       self.on_key_down(chr(e.key).upper())
      if e.type == KEYUP and chr(e.key).upper() in self.keys:
        self.on_key_up(chr(e.key).upper())
 
  def on_key_down(self, key):
    self.output.send(mido.Message('note_on',  note=self.keys[key]))

  def on_key_up(self, key):
    self.output.send(mido.Message('note_off', note=self.keys[key]))

class BeatsPlot(object):
  def __init__(self, width, height, background, foreground):
    self.width  = width
    self.height = height
    self.background = pygame.Color(background) if type(background) == type('') else background
    self.foreground = pygame.Color(foreground) if type(foreground) == type('') else foreground

  def plot(self, beats):
    surface = pygame.surface.Surface((self.width, self.height)).convert()
    surface.fill(self.background)
    self._draw(surface, beats)
    return surface

  def _draw(self, surface, beats):
    scale_x = self.width / beats.duration()
    keys = generate_keys(beats)
    for beat in beats:
      beat_height = 50
      beat_width  = (beat[1].time - beat[0].time) * scale_x - 1
      beat_left   = beat[0].time * scale_x
      beat_top    = (beats.middle_note() - beat[0].note) * beat_height + self.height / 2 - beat_height
      beat_key    = find(keys.items(), lambda x: x[1] == beat[0].note)[1][0]
      #=========#
      surface.blit(label(beat_key, self.foreground, self.background, (beat_width, beat_height)), (beat_left, beat_top))


#================================================================#
  



#================================================================#
if __name__ == '__main__':
  print(Beats(read_midi('Breath.mid')))

  piano = Piano(generate_keys(Beats(read_midi('Breath.mid'))))

  screen.blit(BeatsPlot(SCREEN_SIZE[0], SCREEN_SIZE[1], '#000080', '#55FF55').plot(Beats(read_midi('Breath.mid'))), (0, 0))

  while not done():
    #PROCESS
    events = pygame.event.get()
    piano.process(events)
    #RENDER
    ...
    #UPDATE
    pygame.display.update()


