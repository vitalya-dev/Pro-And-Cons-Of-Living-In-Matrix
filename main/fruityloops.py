import copy

import pygame
from pygame.locals import *

from constants import *
from utils import *
from midi import * 

from shape import *
from piano import *
from beats_roll import *
from melody_viewer import *
from beat_editor import *

class Fruityloops(Shape):
  def __init__(self, melody, piano, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self._melody = melody
    self._piano = piano
    #================#
    self._melody_viewer = MelodyViewer(copy.deepcopy(melody), piano, parent=self)
    self._melody_viewer.sec2pixel = size[0] / melody_duration(melody)
    #================#
    self._beat_editor = None
    #================#
    self._beats_roll = BeatsRoll(piano.midioutput)
    #================#
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
    elif self.state == 'PLAY':
      self._play_state(events)
    elif self.state == 'EDIT':
      self._edit_state(events)

  def _wait_state(self, events):
    keydown_event = get_event(events, KEYDOWN)
    if keydown_event and keydown_event.key == K_SPACE:
      self._beats_roll.play(self._melody_viewer.melody)
      self.state = 'PLAY'

  def _play_state(self, events):
    if self._beats_roll.state == 'COMPLETE':
      self.state = 'WAIT'
    elif self._beats_roll.state == 'INTERRUPT':
      self._handle_beats_roll_interruption()
      
  def _handle_beats_roll_interruption(self):
    if self._beats_roll.zero_beat_interrupt:
      self._beat_editor = BeatEditor(beat_to_edit=self._beats_roll.zero_beat, piano=self._melody_viewer.piano, parent=self)
      self._beat_editor.sec2pixel = self._melody_viewer.sec2pixel
      self.state = 'EDIT'
    else:
      self.state = 'WAIT'


  def _edit_state(self, events):
    self._beat_editor.process(events)
    if self._beat_editor.state == 'DONE':
      self.state = 'WAIT'
      return
    #================#
    keydown_event = get_event(events, KEYDOWN)
    if keydown_event and keydown_event.key == K_SPACE:
      self._beats_roll.play(self._melody_viewer.melody)
      self.state = 'PLAY'

  def draw(self):
    if self.state == 'WAIT':
      self._draw_melody_viewer()
      self._draw_progressbar()
    elif self.state == 'PLAY':
      self._draw_melody_viewer()
      self._draw_progressbar()
    elif self.state == 'EDIT':
      self._draw_melody_viewer()
      self._draw_beat_editor()
    return self._surface

  def _draw_melody_viewer(self):
    self._melody_viewer.primary_color = self.primary_color
    self._melody_viewer.secondary_color = self.secondary_color
    #================#
    self._surface.blit(self._melody_viewer.draw(), self._melody_viewer.parent_space_rect)

  def _draw_progressbar(self):
    current_playing_beat = self._get_current_playing_beat()
    #================#
    progressbar_width = (current_playing_beat[1].time - current_playing_beat[0].time) * self._melody_viewer.sec2pixel - 1
    progressbar_height = self._surface.get_height()
    progressbar_x = current_playing_beat[0].time * self._melody_viewer.sec2pixel
    progressbar_y = 0
    #================#
    self._surface.fill(self.tertiary_color, (progressbar_x, progressbar_y, progressbar_width, progressbar_height))
  
  def _get_current_playing_beat(self):
    if self._beats_roll.current_playing_beat:
      return self._beats_roll.current_playing_beat
    else:
      return self._melody[0]

  def _draw_beat_editor(self):
    self._beat_editor.primary_color = self.tertiary_color
    self._beat_editor.secondary_color = self.secondary_color
    #================#
    self._surface.blit(self._beat_editor.draw(), self._beat_editor.parent_space_rect)

      
if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  #================#
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  melody = Midi('Breath.mid').beats()
  #================#
  fruityloops = Fruityloops(melody_null_n_beats(melody, 5), Piano(mido.open_output(None), Piano.generate_pianokeys_from_beats(melody)))
  fruityloops.primary_color=CHARLESTON
  fruityloops.secondary_color=DIM
  fruityloops.tertiary_color=EBONY
  #================================================================================================#
  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    fruityloops.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(fruityloops.draw(), fruityloops.world_space_rect)
    pygame.display.update()
