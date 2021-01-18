import pygame
from pygame.locals import *

from constants import *
from utils import *

from piano import *
from piano_roll import *
from midi import *
from melody_editor import *
from melody_viewer import *

class Fruityloops(Shape):
  def __init__(self, midioutput, melody, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self._piano = Piano(midioutput, Piano.generate_pianokeys_from_beats(melody))
    self._piano_roll = PianoRoll(midioutput)
    #================#
    self._melody_viewer = MelodyViewer(melody, size, parent=self)
    #================#
    self._melody_editor = MelodyEditor(
      pianokeys=Piano.generate_pianokeys_from_beats(melody),
      scale_x=self._melody_viewer.time_to_pixel_scale,
      foreground_color=RED,
      text_color=GREEN,
      size=size,
      parent=self
    )
    self._melody_editor.set_colorkey(BLACK)
    #================#
    self._surface = pygame.surface.Surface(size).convert()

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and e.key == K_SPACE:
        self._piano_roll.start_or_stop_playing_beats(self._melody_editor.melody)
    #================#
    self._melody_viewer.process(events)
    self._melody_editor.process(events)
    self._piano.process(events)

  def draw(self):
    self._surface.blit(self._melody_viewer.draw(), self._melody_viewer.parent_space_rect)
    self._surface.blit(self._melody_editor.draw(), self._melody_editor.parent_space_rect)
    return self._surface

      
if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  fruityloops = Fruityloops(mido.open_output(None), Midi('Breath.mid').beats())

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    fruityloops.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(fruityloops.draw(), fruityloops.world_space_rect)
    pygame.display.update()
