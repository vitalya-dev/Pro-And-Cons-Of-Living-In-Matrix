import time

import pygame
from pygame.locals import *

from constants import *
from utils import *

from piano import *
from midi import *
from shape import *
from label import *

class BeatEditor(Shape):
  def __init__(self, piano, parent=None):
    super().__init__(parent)
    #================#
    self.beat_to_edit = None
    #================#
    self.piano = piano
    #================#
    self.sec2pixel = SEC2PIXEL
    self.pitch2pixel = PITCH2PIXEL
    #================#
    self.input = {'key': 0, 'note': 0, 'time': 0, 'dtime': 0}
    self.state = 'IDLE'
    #================#
    self.primary_color = BLACK
    self.secondary_color = BLACK
    self.tertiary_color = BLACK
    self.quaternary_color = BLACK
    self.quinary_color = BLACK
    self.senary_color = BLACK
    self.septenary_color = BLACK
    self.octonary_color = BLACK
    #================#

  def edit(self, beat):
    self.beat_to_edit = beat
    #================#
    self.input = {'key': 0, 'note': 0, 'time': 0, 'dtime': 0}
    self.state = 'IDLE'
    #================#
    self._surface = pygame.surface.Surface((beat_duration(self.beat_to_edit) * self.sec2pixel, self.pitch2pixel))
    self._surface.set_colorkey(BLACK)
    

  def process(self, events):
    if self.state == 'IDLE':
      self._idle_state(events)
    elif self.state == 'EDIT':
      self._edit_state(events)
  
  def _idle_state(self, events):
    if self._piano_key_down(events):
      key = self._piano_key_down(events)
      #================#
      self.input = {'key': key, 'note': self.piano.keys[key], 'time': time.time(), 'dtime': 0}
      self.piano.on_key_down(key)
      self.state = 'EDIT'

  def _edit_state(self, events):
    self._update_input()
    #================#
    if self._input_is_long_enough():
       self.beat_to_edit[0].note = self.input['note']
       self.beat_to_edit[1].note = self.input['note']
       #================#
       self.state = 'IDLE'              
    elif self._piano_key_up(events):
      self.piano.on_key_up(self.input['key'])
      self.state = 'IDLE'


  def _piano_key_down(self, events):
    keydown_event = get_event(events, KEYDOWN)
    if keydown_event:
      key = chr(keydown_event.key).upper()
      if key in self.piano.keys:
        return key
    return None

  def _piano_key_up(self, events):
    return is_key_up(self.input['key'], events)

  def _update_input(self):
    self.input['dtime'] = time.time() - self.input['time']    

  def _input_is_long_enough(self):
    return self.input['dtime'] > beat_duration(self.beat_to_edit)

  def draw(self):
    if self.state == 'IDLE':
      self._draw_beat()
    if self.state == 'EDIT':
      self._draw_input()
    return self._surface

  def _draw_beat(self):
    beatbar_width = beat_duration(self.beat_to_edit) * self.sec2pixel
    beatbar_height = self.pitch2pixel
    beatbar_text = self.piano.keys[self.beat_to_edit[0].note] if self.beat_to_edit[0].note != 0 else 'Nah'
    #================#
    self._draw_beatbar(beatbar_text, beatbar_width, beatbar_height)
      
  def _draw_input(self):
    inputbar_width = (time.time() - self.input['time']) * self.sec2pixel
    inputbar_height = self.pitch2pixel
    inputbar_text = self.input['key']
    #================#
    self._draw_beatbar(inputbar_text, inputbar_width, inputbar_height)


  def _draw_beatbar(self, beatbar_text, beatbar_width, beatbar_height):
    beatbar = Label(beatbar_text, size=(beatbar_width, beatbar_height), parent=self)
    beatbar.primary_color = self.primary_color
    beatbar.secondary_color = self.secondary_color
    #================#
    self._surface.blit(beatbar.draw(), beatbar.parent_space_rect)


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  #================#
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  beats = Midi('Breath.mid').beats()
  #================#
  beat_editor = BeatEditor(Piano(mido.open_output(None), Piano.generate_pianokeys_from_beats(beats)))
  beat_editor.edit(beats[5])
  beat_editor.primary_color=CHARLESTON
  beat_editor.secondary_color=EBONY
  #================================================================================================#
  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    beat_editor.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(beat_editor.draw(), beat_editor.world_space_rect)
    pygame.display.update()
