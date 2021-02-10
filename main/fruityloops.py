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
from beat_editor import *


class Fruityloops(Shape):
  def __init__(self, beats, piano, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self._beats_splitted = self._split_beats_by_null_beat(beats)
    self._beats_splitted_current_part_index = 0
    self._beats_solved = []
    #================#
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
    elif self.state == 'PLAY':
      self._process_play_state(events)
    elif self.state == 'EDIT':
      self._process_edit_state(events)

  def _process_idle_state(self, events):
    if is_keycode_down(K_SPACE, events) and self._beats_splitted_all_parts_is_solved():
      self._beats_roll.play(self._beats_solved)
      self.state = 'COMPLETE'
    elif is_keycode_down(K_SPACE, events) and is_keycode_pressed(K_LSHIFT) and len(self._beats_solved) > 0:
      self._beats_roll.play(self._beats_solved)
      self.state = 'PLAY'
    elif is_keycode_down(K_SPACE, events) and not is_keycode_pressed(K_LSHIFT):
      self._beats_roll.play(self._beats_splitted[self._beats_splitted_current_part_index])
      self.state = 'PLAY'

  def _process_play_state(self, events):
    if self._beats_roll.state == 'IDLE' and self._beats_roll.played_beats_stack == self._beats_solved:
      self.state = 'IDLE'
    elif self._beats_roll.state == 'IDLE':
       self._beat_editor.edit(self._beats_roll.played_beats_stack[-1])
       self.state = 'EDIT'
  
  def _process_edit_state(self, events):
    self._beat_editor.process(events)
    #================#
    if self._beat_editor.state == 'EDIT':
      self._update_beat_editor_position()
    #================#
    if is_keycode_down(K_SPACE, events) and is_keycode_pressed(K_LSHIFT):
      self._beats_roll.play(self._beats_solved + self._beats_splitted[self._beats_splitted_current_part_index])
      self.state = 'PLAY'
    elif is_keycode_down(K_SPACE, events) and not is_keycode_pressed(K_LSHIFT):
      self._beats_roll.play(self._beats_splitted[self._beats_splitted_current_part_index])
      self.state = 'PLAY'
    elif is_keycode_down(K_RETURN, events):
      self._beats_solved += self._beats_splitted[self._beats_splitted_current_part_index]
      self._beats_splitted_goto_next_part()
      self.state = 'IDLE'

  def _beats_splitted_goto_next_part(self):
    self._beats_splitted_current_part_index += 1
    self._beats_splitted_current_part_index %= len(self._beats_splitted)

  def _beats_splitted_all_parts_is_solved(self):
    return len(self._beats_solved) == len(self._beats_viewer.beats)
    
  def _update_beat_editor_position(self):
    beat_editor_pos_x = self._beats_viewer.time_to_x(self._beat_editor.beat_to_edit[0].time)
    beat_editor_pos_y = self._beats_viewer.pitch_to_y(self._beat_editor.input['note'])
    self._beat_editor.position = (beat_editor_pos_x, beat_editor_pos_y)

  def draw(self):
    self._draw_background()
    #================#
    if self.state == 'IDLE':
      self._draw_beats_splitted_current_part_background()
      self._draw_progressbar_in_idle_state()
      self._draw_beats_viewer()
    elif self.state == 'PLAY':
      self._draw_beats_splitted_current_part_background()
      self._draw_progressbar_in_play_state()
      self._draw_beats_viewer()
    elif self.state == 'EDIT':
      self._draw_beats_splitted_current_part_background()
      self._draw_progressbar_in_edit_state()
      self._draw_beats_viewer()
      if self._beat_editor.state == 'EDIT':
        self._draw_beat_editor()
    elif self.state == 'COMPLETE':
      self._draw_progressbar_in_play_state()
      self._draw_beats_viewer()
    #================#
    return self._surface

  def _draw_background(self):
    self._surface.fill(self.primary_color)

  def _draw_beats_splitted_current_part_background(self):
    beats_splitted_current_part = self._beats_splitted[self._beats_splitted_current_part_index]
    #================#
    bscp_background_width = beats_duration(beats_splitted_current_part) * self._beats_viewer.sec2pixel
    bscp_background_height = self._surface.get_height()
    bscp_background_x = beats_splitted_current_part[0][0].time * self._beats_viewer.sec2pixel
    bscp_background_y = 0
    bscp_background_color = lerp_color(self.primary_color, BLACK, 0.05)
    #================#
    self._surface.fill(bscp_background_color, (bscp_background_x, bscp_background_y, bscp_background_width, bscp_background_height))

  def _draw_beats_viewer(self):
    self._beats_viewer.primary_color = self.secondary_color
    self._beats_viewer.secondary_color = self.tertiary_color
    self._surface.blit(self._beats_viewer.draw(), self._beats_viewer.parent_space_rect)

  def _draw_beat_editor(self):
    self._beat_editor.primary_color = self.secondary_color
    self._beat_editor.secondary_color = self.tertiary_color
    #================#
    self._surface.blit(self._beat_editor.draw(), self._beat_editor.parent_space_rect)

  def _draw_progressbar_in_idle_state(self):
    self._draw_progressbar_using_beat(self._beats_splitted[self._beats_splitted_current_part_index][0])
    
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
    clock.tick(60)
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    fruityloops.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(fruityloops.draw(), fruityloops.world_space_rect)
    pygame.display.update()
