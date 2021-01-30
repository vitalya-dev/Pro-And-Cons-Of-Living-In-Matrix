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
  def __init__(self, beat_to_edit, piano, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self._beat_to_edit = beat_to_edit
    self._beat_to_edit[0].note = 0
    self._beat_to_edit[1].note = 0
    #================#
    self.piano = piano
    #================#
    self.sec2pixel = SEC2PIXEL
    #================#
    self._input = {'key': 0, 'note': 0, 'time': 0, 'dtime': 0}
    self.state = 'WAIT'
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
    self._surface = pygame.surface.Surface(size).convert()

  def process(self, events):
    if self.state == 'WAIT':
      self._wait_state(events)
    elif self.state == 'EDIT':
      self._edit_state(events)
    elif self.state == 'DONE':
      print(self._beat_to_edit)
  
  def _wait_state(self, events):
    self._handle_keydown(events)

  def _handle_keydown(self, events):
    keydown_event = get_event(events, KEYDOWN)
    if keydown_event:
      key = chr(keydown_event.key).upper()
      #================#
      if key in self.piano.keys:
        self._input = {'key': key, 'note': self.piano.keys[key], 'time': time.time(), 'dtime': 0}
        self.piano.on_key_down(key)
        self.state = 'EDIT'

  def _edit_state(self, events):
    self._update_input()
    self._handle_keyup(events)
    self._handle_input_is_long_enough()

  def _update_input(self):
    self._input['dtime'] = time.time() - self._input['time']    

  def _handle_keyup(self, events):
    keyup_event = get_event(events, KEYUP)
    if keyup_event:
      key = chr(keyup_event.key).upper()
      #================#
      if key == self._input['key']:
        self._input = {'key': 0, 'note': 0, 'time': 0, 'dtime': 0}
        self.piano.on_key_up(key)
        self.state = 'WAIT'

  def _handle_input_is_long_enough(self):
    if self._input_is_long_enough():
      self._beat_to_edit[0].note = self._input['note']
      self._beat_to_edit[1].note = self._input['note']
      #================#
      self.state = 'DONE'
      

  def _input_is_long_enough(self):
    return self._input['dtime'] > self._beat_to_edit_duration()

  def _beat_to_edit_duration(self):
    return self._beat_to_edit[1].time - self._beat_to_edit[0].time

  def draw(self):
    if self.state == 'WAIT':
      self._draw_background()
      self._draw_editbar()
    elif self.state == 'EDIT':
      self._draw_background()
      self._draw_editbar()
      self._draw_beatbar()
    elif self.state == 'DONE':
      self._draw_background()
    return self._surface
  
  def _draw_background(self):
    self._surface.fill(self.primary_color, self._surface.get_rect())

  def _draw_editbar(self):
    editbar_width = (self._beat_to_edit[1].time - self._beat_to_edit[0].time) * self.sec2pixel - 1
    editbar_height = self._surface.get_height()
    editbar_x = self._beat_to_edit[0].time * self.sec2pixel
    editbar_y = 0
    self._surface.fill(self.secondary_color, (editbar_x, editbar_y, editbar_width, editbar_height))

  def _draw_beatbar(self):
    beatbar_width = (time.time() - self._input['time']) * self.sec2pixel
    beatbar_height = self._surface.get_height() / 10
    beatbar_x = self._beat_to_edit[0].time * self.sec2pixel
    beatbar_y = (self.piano.keys['F'] - self._input['note']) * beatbar_height + self._surface.get_height() / 2 - beatbar_height
    beatbar_text = self._input['key']
    #================#
    beatbar = Label(beatbar_text, size=(beatbar_width, beatbar_height), parent=self)
    beatbar.primary_color = self.tertiary_color
    beatbar.secondary_color = lerp_color(self.primary_color, BLACK, 0.2)
    beatbar.position = (beatbar_x, beatbar_y)
    #================#
    self._surface.blit(beatbar.draw(), beatbar.parent_space_rect)




if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  #================#
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  melody = Midi('Breath.mid').beats()
  #================#
  beat_editor = BeatEditor(beat_to_edit=melody[5], piano=Piano(mido.open_output(None), Piano.generate_pianokeys_from_beats(melody)))
  beat_editor.primary_color=CHARLESTON
  beat_editor.secondary_color=OLIVE
  beat_editor.tertiary_color=EBONY
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
