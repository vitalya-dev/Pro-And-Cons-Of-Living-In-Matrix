import pygame
from pygame.locals import *

from constants import *
from utils import *
from midi import * 

from shape import *
from piano import *
from piano_roll import *
from melody_viewer import *
from beat_editor import *

class Fruityloops(Shape):
  def __init__(self, melody, piano, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self._melody_viewer = MelodyViewer(melody, piano, parent=self)
    self._melody_viewer.sec2pixel = size[0] / melody_duration(melody)
    #================#
    self._beat_editor = None
    #================#
    self._piano_roll = PianoRoll(piano.midioutput)
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
    if self.state == 'PLAY':
      self._play_state(events)
    elif self.state == 'EDIT':
      self._edit_state(events)

  def _wait_state(self, events):
    keydown_event = get_event(events, KEYDOWN)
    if keydown_event and keydown_event.key == K_SPACE:
      self._piano_roll.play(self._melody_viewer.melody)
      self.state = 'PLAY'

  def _play_state(self, events):
    if self._piano_roll.state == 'COMPLETE':
      self.state = 'WAIT'
    elif self._piano_roll.state == 'UNCOMPLETE':
      self._beat_editor = BeatEditor(beat_to_edit=self.piano_roll[5], self.melody_viewer.piano)
      self.state = 'EDIT'

  def _edit_state(self, events):
    print('EDIT STATE')


  def draw(self):
    self._draw_melody_viewer()
    return self._surface

  def _draw_melody_viewer(self):
    self._melody_viewer.primary_color = self.primary_color
    self._melody_viewer.secondary_color = self.secondary_color
    #================#
    self._surface.blit(self._melody_viewer.draw(), self._melody_viewer.parent_space_rect)

      
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
