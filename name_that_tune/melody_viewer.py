import math

import pygame
from pygame.locals import *

from constants import *
from utils import *

from piano import *
from midi import *
from shape import *
from label import *

class MelodyViewer(Shape):
  def __init__(self, melody, width, height, background_color=BLACK, foreground_color=WHITE, text_color=GRAY, parent=None):
    super().__init__(parent)
    #================#
    self.background_color = background_color
    self.foreground_color = foreground_color
    self.text_color = text_color
    #================#
    self._surface = pygame.surface.Surface((width, height)).convert()
    #================#
    self._melody = melody
    self._melody_beatbars = self._create_melody_beatbars()

  def process(self, events):
    pass

  @property
  def time_to_pixel_scale(self):
    melody_length = self._melody[-1][1].time
    return self._surface.get_width() / melody_length

  def _create_melody_beatbars(self):
    melody_middle_note = math.floor(average([beat[0].note for beat in self._melody]))
    #================#
    melody_beatbars = []
    for beat in self._melody:
      beatbar_height = 50
      beatbar_left = beat[0].time * self.time_to_pixel_scale
      beatbar_width = (beat[1].time - beat[0].time) * self.time_to_pixel_scale - 1
      beatbar_top = (melody_middle_note - beat[0].note) * beatbar_height + self._surface.get_height() / 2 - beatbar_height
      beatbar_text = self._get_pianokey_with_corresponded_note(beat[0].note)[0]
      #================#
      beatbar = Label(
        beatbar_text, background=self.foreground_color, foreground=self.text_color, size=(beatbar_width, beatbar_height), parent=self
      )
      beatbar.position = (beatbar_left, beatbar_top)
      melody_beatbars.append(beatbar)
    return melody_beatbars

  def _get_pianokey_with_corresponded_note(self, note):
    pianokeys = Piano.generate_pianokeys_from_beats(self._melody)
    pianokey_with_corresponded_note = find_value(pianokeys.items(), lambda x: x[1] == note)
    return pianokey_with_corresponded_note

  def draw(self):
    self._draw_background()
    self._draw_melody()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self.background_color)

  def _draw_melody(self):
    for beatbar in self._melody_beatbars:
      self._surface.blit(beatbar.draw(), beatbar.parent_space_rect.topleft)
    
  def set_colorkey(self, colorkey):
    self._surface.set_colorkey(colorkey)

  
      
if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  midioutput = mido.open_output(None)
  piano = Piano(midioutput, Piano.generate_pianokeys_from_midi(Midi('Breath.mid')))

  melody_viewer = MelodyViewer(Midi('Breath.mid').beats(), 640, 480)

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    melody_viewer.process(events)
    piano.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(melody_viewer.draw(), melody_viewer.world_space_rect.topleft)
    pygame.display.update()
