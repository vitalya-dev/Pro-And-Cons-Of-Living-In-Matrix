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
    if l(j): return i
  return -1

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

def read_messages(midifile):
  return list(mido.MidiFile(midifile))
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
class Tune(object):
  def __init__(self, messages):
    self.beat_ons    =  [message for message in messages_to_abstime(messages) if message.type == 'note_on']
    self.beat_offs   =  [message for message in messages_to_abstime(messages) if message.type == 'note_off']
  
  def middle_note(self):
    return int(average([beat_on.note for beat_on in self.beat_ons]))

  def duration(self):
    self.beat_offs[-1].time

  def __iter__(self):
    beat_offs = self.beat_offs[:]
    for beat_on in self.beat_ons:
      i = find(beat_offs, lambda x: x.note == beat_on.note)
      if i >= 0:
        yield (beat_on, beat_offs.pop(i))

  def __str__(self):
    return str(list(self))
#================================================================#
  



#================================================================#
if __name__ == '__main__':
  print(Tune(read_messages('Breath.mid')))
#================================================================#
