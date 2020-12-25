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
      self._create_beatbar_from_beat((note_on, note_off))

  def _input_contains_note(self, note):
    return find_index(self._inputs, lambda x: x.note == note) != -1

  def _pop_note_from_input(self, note):
    i = find_index(self._inputs, lambda x: x.note == note)
    return self._inputs.pop(i)

  def _add_beat_to_melody(self, beat):
    self._make_beat_start_time_equal_to_melody_end_time(beat)
    self._melody.append(beat)

  def _make_beat_start_time_equal_to_melody_end_time(self, beat):
    beat[0].time = self._melody_duration()
    beat[1].time += self._melody_duration()

  def _melody_duration(self):
    if len(self._melody) > 0:
      last_beat_in_melody = self._melody[-1]
      return last_beat_in_melody[1].time
    else:
      return 0

  def _create_beatbar_from_beat(self, beat):
    beatbar_height = 50
    beatbar_left = beat[0].time * self._scale_x
    beatbar_width = (beat[1].time - beat[0].time) * self._scale_x - 1
    beatbar_top = (self._pianokeys['F'] - beat[0].note) * beatbar_height + self._surface.get_height() / 2 - beatbar_height
    beatbar_text = self._pianokeys[beat[0].note]
    #================#
    beatbar = Label(
      beatbar_text, background=self._foreground_color, foreground=self._background_color, size=(beatbar_width, beatbar_height), parent=self
    )
    beatbar.position = (beatbar_left, beatbar_top)
    self._melody_beatbars.append(beatbar)

  def draw(self):
    self._draw_background()
    self._draw_melody()
    self._draw_input()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self._background_color)

  def _draw_melody(self):
    for beatbar in self._melody_beatbars:
      self._surface.blit(beatbar.draw(), beatbar.parent_space_rect.topleft)

  def _draw_input(self):
    for input in self._inputs:
      inputbar_left = self._melody_duration() * self._scale_x
      inputbar_height = 50
      inputbar_width = (time.time - input.time) * self._scale_x
      inputbar_top = (self._pianokeys['F'] - input.note) * inputbar_height + self._surface.get_height() / 2 - inputbar_height
      inputbar_text = self._pianokeys[beat[0].note]
      pygame.draw.rect(self.screen, self.color, self.rect)

    

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
    screen.blit(melody_editor.draw(), melody_editor.world_space_rect.topleft)
    pygame.display.update()
