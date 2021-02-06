import copy

import pygame
from pygame.locals import *

from constants import *
from utils import *
from midi import * 

from shape import *
from piano import *
from beats_viewer import *
from beats_roll import *

class Fruityloops(Shape):
  def __init__(self, beats, piano, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self._puzzle = self._split_beats_by_null_beat(beats)
    self._piano = piano
    #================#
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
    self._beats_viewer = BeatsViewer(beats, piano, parent=self)
    self._beats_viewer.sec2pixel = size[0] / beats_duration(beats)
    #================#
    self._beat_editor = BeatEditor(piano, parent=self)
    self._beat_editor.sec2pixel = self._beats_viewer.sec2pixel
    #================#
    self._beats_roll = BeatsRoll(self._piano.midioutput)
    #================#
    self._surface = pygame.surface.Surface(size).convert()

  def _split_beats_by_null_beat(self, beats):
    null_beat_indexes = [i for i, beat in enumerate(beats, start=1) if is_null_beat(beat)]
    beats_intervals = convert_to_intervals([0] + null_beat_indexes)
    return [beats[i[0]:i[1]] for i in beats_intervals]

  def process(self, events):
    if self.state == 'IDLE':
      self._process_idle_state(events)
    if self.state == 'PLAY':
      self._process_play_state(events)
    if self.state == 'EDIT':
      self._process_edit_state(events)

  def _process_idle_state(self, events):
    if is_key_down(' ', events):
      self._beats_roll.play(self._puzzle[0])
      self.state = 'PLAY'

  def _process_play_state(self, events):
    if self._beats_roll.state == 'IDLE':
      self._beat_editor.edit(self._beats_roll.played_beats_stack[-1])
      self.state = 'EDIT'

  def _process_edit_state(self, events):
    if is_key_down(' ', events):
      self._beats_roll.play(self._puzzle[0])
      self.state = 'PLAY'
    #================#
    self._beat_editor.process(events)

  def draw(self):
    self._draw_background()
    #================#
    if self.state == 'IDLE':
      self._draw_progressbar_in_idle_state()
      self._draw_beats_viewer()
    if self.state == 'PLAY':
      self._draw_progressbar_in_play_state()
      self._draw_beats_viewer()
    if self.state == 'EDIT':
      self._draw_progressbar_in_edit_state()
      self._draw_beats_viewer()
      self._draw_beats_editor()
    #================#
    return self._surface

  def _draw_background(self):
    self._surface.fill(self.primary_color)

  def _draw_beats_viewer(self):
    self._beats_viewer.primary_color = self.secondary_color
    self._beats_viewer.secondary_color = self.tertiary_color
    #================#
    self._surface.blit(self._beats_viewer.draw(), self._beats_viewer.parent_space_rect)

  def _draw_beats_editor(self):
    pass

  def _draw_progressbar_in_idle_state(self):
    self._draw_progressbar_using_beat(self._puzzle[0][0])
    
  def _draw_progressbar_in_play_state(self):
    self._draw_progressbar_using_beat(self._beats_roll.currently_played_beat)

  def _draw_progressbar_in_edit_state(self):
    self._draw_progressbar_using_beat(self._beats_roll.played_beats_stack[-1])

  def _draw_progressbar_using_beat(self, beat):
    progressbar_width = (beat[1].time - beat[0].time) * self._beats_viewer.sec2pixel - 1
    progressbar_height = self._surface.get_height()
    progressbar_x = beat[0].time * self._beats_viewer.sec2pixel
    progressbar_y = 0
    progressbar_color = lerp_color(self.secondary_color, self.primary_color, 0.8)
    #================#
    self._surface.fill(progressbar_color, (progressbar_x, progressbar_y, progressbar_width, progressbar_height))
    
      
if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  #================#
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  beats = Midi('Breath.mid').beats()
  #================#
  fruityloops = Fruityloops(null_beats(beats, [5, 11, -1]), Piano(mido.open_output(None), Piano.generate_pianokeys_from_beats(beats)))
  fruityloops.primary_color=CHARLESTON
  fruityloops.secondary_color=EBONY
  fruityloops.tertiary_color=JET
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
