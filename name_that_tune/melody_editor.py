import pygame
from pygame.locals import *

from constants import *
from utils import *

from piano import *
from midi import *
from shape import *
from label import *

class Melody(Shape):
  def __init__(self, pianokeys, scale_x, width, height, background=BLACK, foreground=WHITE, parent=None):
    super().__init__(parent)
    #================#
    self._background_color = background
    self._foreground_color = foreground
    #================#
    self._pianokeys = pianokeys
    self._scale_x = scale_x
    #================#
    self._inputs = []
    #================#
    self._surface = pygame.surface.Surface((width, height)).convert()

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and chr(e.key).upper() in self.keys:
       self.on_key_down(chr(e.key).upper())
      if e.type == KEYUP and chr(e.key).upper() in self.keys:
        self.on_key_up(chr(e.key).upper())

  def on_key_down(self, key):
    if key.upper() in self._keys and len(self._inputs) == 0:
      note_on = mido.Message('note_on',  note=self._keys[key], time=time.time())
      self._inputs.append(note_on)

  def on_key_up(self, key):
    if key.upper() in self.keys and self._inputs_contain_note(self._pianokeys[key])
      note_on = self._inputs[0]
      note_off = mido.Message('note_off',  note=note_on.note, time=time.time()-note_on.time)
      self._add_beat_to_melody((note_on, note_off))
      

  def _inputs_contain_note(self, note):
    pass

  def _add_beat_to_melody(self, beat):09:34
    pass
      


