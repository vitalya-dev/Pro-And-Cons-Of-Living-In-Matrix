import copy

import pygame
from pygame.locals import *

from constants import *
from utils import *
from midi import * 

from shape import *
from piano import *
from beats_viewer import *

class Fruityloops(Shape):
  def __init__(self, beats, piano, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self._beats = beats
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
    self._surface = pygame.surface.Surface(size).convert()


  def process(self, events):
    if self.state == 'IDLE':
      self._process_idle_state(events)

  def _process_idle_state(self, events):
    print('IDLE')

  def _is_key_down(self, key, events):
    keydown_event = get_event(events, KEYDOWN)
    return keydown_event and keydown_event.key == key 

  def draw(self):
    if self.state == 'IDLE':
      self._draw_background()
      self._draw_idle_progressbar()
      self._draw_beats_viewer()
    #================#
    return self._surface

  def _draw_background():
    self._surface.fill(self.primary_color)

  def _draw_beats_viewer(self):
    self._beats_viewer.primary_color = self.secondary_color
    self._beats_viewer.secondary_color = self.tertiary_color
    #================#
    self._surface.blit(self._beats_viewer.draw(), self._beats_viewer.parent_space_rect)

  def _draw_idle_progressbar(self):
    start_beat = self._get_start_beat()
    #================#
    progressbar_width = (start_beat[1].time - start_beat[0].time) * self._beats_viewer.sec2pixel - 1
    progressbar_height = self._surface.get_height()
    progressbar_x = start_beat[0].time * self._beats_viewer.sec2pixel
    progressbar_y = 0
    progressbar_color = lerp_color(self.secondary_color, self.primary_color, 0.5)
    self._surface.fill(progressbar_color, (progressbar_x, progressbar_y, progressbar_width, progressbar_height))

  def _get_start_beat(self):
    return self._beats[0]


      
if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  #================#
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  beats = Midi('Breath.mid').beats()
  #================#
  fruityloops = Fruityloops(null_beats(beats, [5, 11]), Piano(mido.open_output(None), Piano.generate_pianokeys_from_beats(beats)))
  fruityloops.primary_color=CHARLESTON
  fruityloops.secondary_color=EBONY
  fruityloops.tertiary_color=DIM
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
