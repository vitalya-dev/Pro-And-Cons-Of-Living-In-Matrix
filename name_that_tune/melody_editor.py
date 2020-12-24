import time

import pygame
from pygame.locals import *

from constants import *
from utils import *

from piano import *
from midi import *
from shape import *
from label import *

class MelodyEditor(Shape):
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
    self._melody = []
    self._melody_beatbars = []
    #================#
    self._surface = pygame.surface.Surface((width, height)).convert()

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and chr(e.key).upper() in self._pianokeys:
       self.on_key_down(chr(e.key).upper())
      if e.type == KEYUP and chr(e.key).upper() in self._pianokeys:
        self.on_key_up(chr(e.key).upper())

  def on_key_down(self, key):
    if key.upper() in self._pianokeys and len(self._inputs) == 0:
      note_on = mido.Message('note_on',  note=self._pianokeys[key], time=time.time())
      self._inputs.append(note_on)

  def on_key_up(self, key):
    if key.upper() in self._pianokeys and self._input_contains_note(self._pianokeys[key]):
      note_on = self._pop_note_from_input(self._pianokeys[key])
      note_off = mido.Message('note_off',  note=note_on.note, time=time.time()-note_on.time)
      self._add_beat_to_melody((note_on, note_off))


  def _input_contains_note(self, note):
    return find_index(self._inputs, lambda x: x.note == note) != -1

  def _pop_note_from_input(self, note):
    i = find_index(self._inputs, lambda x: x.note == note)
    return self._inputs.pop(i)

  def _add_beat_to_melody(self, beat):
    self._make_beat_start_time_equal_to_melody_end_time(beat)
    self._melody.append(beat)

  def _make_beat_start_time_equal_to_melody_end_time(self, beat):
    if len(self._melody) > 0:
      last_beat_in_melody = self._melody[-1]
      beat[0].time = last_beat_in_melody[1].time
      beat[1].time += last_beat_in_melody[1].time
    else:
      beat[0].time = 0

  def _create_beatbar_from_beat(self, beat):
    beatbar_height = 50
    beatbar_left = beat[0].time * self_scale_x
    beatbar_width = (beat[1].time - beat[0].time) * self._scale_x - 1
    beatbar_top = (melody_middle_note - beat[0].note) * beatbar_height + self._surface.get_height() / 2 - beatbar_height
    beatbar_text = self._get_pianokey_with_corresponded_note(beat[0].note)[0]


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  midioutput = mido.open_output(None)
  piano = Piano(midioutput, Piano.generate_pianokeys_from_midi(Midi('Breath.mid')))
  
  melody_editor = MelodyEditor(Piano.generate_pianokeys_from_midi(Midi('Breath.mid')), 150, 640, 480)


  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    piano.process(events)
    melody_editor.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    pygame.display.update()
