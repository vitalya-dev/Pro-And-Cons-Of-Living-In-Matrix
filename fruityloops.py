#git show 8f98340e744d7c967c8faf71cedd320039c6befd:fruityloops.py | clip

import threading
import time
import sys
import mido
import copy

import pygame
from pygame.locals import *

#================================================================#
SCREEN_SIZE = (640, 480)
FONT_SIZE  = 32
MAX_COLS   = (int)(SCREEN_SIZE[0] / (FONT_SIZE / 2))
MAX_ROWS   = (int)(SCREEN_SIZE[1] / FONT_SIZE)
#================================================================#


#================================================================#
pygame.init()
#================================================================#

#================================================================#
screen     = pygame.display.set_mode(SCREEN_SIZE)
clock      = pygame.time.Clock()
font       = pygame.font.Font('data/FSEX300.ttf', FONT_SIZE - 1)
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
  def __init__(self, messages=[]):
    self._beats = self._generate_beats(messages)

  def clear(self):
    self._beats.clear()

  def _generate_beats(self, messages):
    beats       =  []
    beat_ons    =  [message for message in messages_to_abstime(messages) if message.type == 'note_on']
    beat_offs   =  [message for message in messages_to_abstime(messages) if message.type == 'note_off']
    #==============#
    for beat_on in beat_ons:
      i = find(beat_offs, lambda x: x.note == beat_on.note)[0]
      if i >= 0:
        beats.append((beat_on, beat_offs.pop(i)))
    #==============#
    return beats

  def to_stream(self):
    return sorted([beat for fullbeat in self._beats for beat in fullbeat], key=lambda beat: beat.time)


  def middle_note(self):
    return int(average([beat[0].note for beat in self._beats]))

  def duration(self):
    return self._beats[-1][1].time if len(self._beats) > 0 else 0

  def add(self, beat):
    self._beats.append(beat)

  def __getitem__(self, index):
    return self._beats[index]

  def __iter__(self):
    return iter(self._beats)

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


class Window(object):
  def __init__(self, width, height, background):
    self.surface = pygame.surface.Surface((width, height)).convert()
    self.background = pygame.Color(background)
    #=================#
    self.buffer  = self.surface.copy()
    self.buffer.set_colorkey((0, 0, 0))
    #=================#
    self.keys_down = pygame.key.get_pressed()
    self.draws = []

  @property
  def width(self):
    return self.surface.get_width()

  @property
  def height(self):
    return self.surface.get_height()

  def draw(self, surf, pos):
    self.draws.append({'surface': surf, 'pos': pos})

  def render(self):
    self.surface.fill(self.background)
    for d in self.draws:
      self.surface.blit(d['surface'], d['pos'])
    self.surface.blit(self.buffer, (0, 0))
    return self.surface

  def process(self, events):
    self.keys_down = pygame.key.get_pressed()
    for e in events:
      if e.type == KEYUP:
        self.on_key_up(chr(e.key))
      if e.type == KEYDOWN:
       self.on_key_down(chr(e.key))

  def on_key_up(self, key):
    ...

  def on_key_down(self, key):
    ...

class BeatsEditor(Window):
  def __init__(self, width, height, background, foreground, keys):
    super().__init__(width, height, background)
    self.foreground = foreground
    self.keys = keys
    self.beats = Beats()
    self._inputs = []

  def on_key_down(self, key):
    if key.upper() in self.keys and len(self._inputs) == 0:
      self._inputs.append(mido.Message('note_on',  note=self.keys[key.upper()], time=time.time()))

  def on_key_up(self, key):
    if key.upper() in self.keys:
      i = find(self._inputs, lambda x: x.note == self.keys[key.upper()])[0]
      if i >= 0:
        self.beats.add(self._beat_from_input(self._inputs.pop(i), self.beats.duration()))

  def clear(self):
    self.beats.clear()
    self._inputs.clear()
    self.buffer.fill((0, 0, 0))

  def process(self, events):
    super().process(events)
    for input in self._inputs:
      self._draw_beat(self.buffer, self._beat_from_input(copy.copy(input), self.beats.duration()))

  def _beat_from_input(self, beat_on, position):
    beat_off = mido.Message('note_off',  note=beat_on.note, time=time.time()-beat_on.time)
    #============#
    beat_on.time  = position
    beat_off.time += position
    #============#
    return (beat_on, beat_off)

  def _draw_beat(self, surface, beat):
    scale_x = 150
    beat_height = 50
    beat_width  = (beat[1].time - beat[0].time) * scale_x - 1
    beat_left   = beat[0].time * scale_x
    beat_top    = (int(average(self.keys.values())) - beat[0].note) * beat_height + self.height / 2 - beat_height
    beat_key    = find(self.keys.items(), lambda x: x[1] == beat[0].note)[1][0]
    #=========#
    if beat_width > 10:
      surface.blit(label(beat_key, self.foreground, self.background, (beat_width, beat_height)), (beat_left, beat_top))


class Piano(object):
  def __init__(self, keys, midioutput):
    self.keys = keys
    self.midioutput = midioutput

  def process(self, events):
    keys_down = pygame.key.get_pressed()
    for e in events:
      if e.type == KEYDOWN and chr(e.key).upper() in self.keys:
       self.on_key_down(chr(e.key).upper())
      if e.type == KEYUP and chr(e.key).upper() in self.keys:
        self.on_key_up(chr(e.key).upper())
 
  def on_key_down(self, key):
    self.midioutput.send(mido.Message('note_on',  note=self.keys[key]))

  def on_key_up(self, key):
    self.midioutput.send(mido.Message('note_off', note=self.keys[key]))


class PianoRoll(object):
  def __init__(self, midioutput):
    self.midioutput = midioutput
    self._play = False

  def toggle(self, beats):
    self._play = not self._play
    if self._play: self.play(beats)

  def play(self, beats):
    self._play = True
    threading.Thread(target=self._play_thread, args=(beats,)).start()

  def _play_thread(self, beats):
    start_time = time.time()
    for beat in beats.to_stream():
      playback_time = time.time() - start_time
      if beat.time - playback_time > 0:
        time.sleep(beat.time - playback_time)
      self.midioutput.send(beat)
      if not self._play:
        break
    self._play = False

class Keyboard(object):
  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and e.key == K_ESCAPE and hasattr(self,  'on_esc'):    self.on_esc()
      if e.type == KEYDOWN and e.key == K_SPACE  and hasattr(self,  'on_space'):  self.on_space()


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
  midioutput = mido.open_output(None)
  #===================#
  piano      = Piano(generate_keys(Beats(read_midi('Breath.mid'))), midioutput)
  piano_roll = PianoRoll(midioutput)
  #===================#
  beats_editor = BeatsEditor(SCREEN_SIZE[0], SCREEN_SIZE[1], '#000080', '#55FF55', generate_keys(Beats(read_midi('Breath.mid'))))
  beats_editor.draw(BeatsPlot(SCREEN_SIZE[0], SCREEN_SIZE[1], '#000080', '#AA0000').plot(Beats(read_midi('Breath.mid'))), (0, 0))
  #===================#
  keyboard = Keyboard()
  keyboard.on_space = lambda: piano_roll.toggle(beats_editor.beats)
  keyboard.on_esc   = lambda: beats_editor.clear()
  #===================#

  while not done():
    #PROCESS
    events = pygame.event.get()
    piano.process(events)
    beats_editor.process(events)
    keyboard.process(events)
    #RENDER
    screen.blit(beats_editor.render(), (0, 0))
    #UPDATE
    pygame.display.update()
#================================================================#

