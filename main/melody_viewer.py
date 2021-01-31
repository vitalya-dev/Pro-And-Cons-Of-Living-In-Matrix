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
  def __init__(self, melody, piano, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self.melody = melody
    self.piano = piano
    #================#
    self.sec2pixel = SEC2PIXEL
    #================#
    self.padding = 2
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
    pass

  def draw(self):
    self._draw_background()
    self._draw_melody()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self.primary_color, self._surface.get_rect())

  def _draw_melody(self):
    for beat in self.melody:
      self._draw_beatbar(beat)

  def _draw_beatbar(self, beat):
    if beat[0].note == 0:
      return
    #================#
    beatbar_width = (beat[1].time - beat[0].time) * self.sec2pixel - self.padding
    beatbar_height = self._surface.get_height() / 10
    beatbar_x = beat[0].time * self.sec2pixel
    beatbar_y = (self.piano.keys['F'] - beat[0].note) * beatbar_height + self._surface.get_height() / 2 - beatbar_height
    beatbar_text = self.piano.keys[beat[0].note]
    #================#
    beatbar = Label(beatbar_text, size=(beatbar_width, beatbar_height), parent=self)
    beatbar.primary_color = self.secondary_color
    beatbar.secondary_color = lerp_color(self.primary_color, BLACK, 0.2)
    beatbar.position = (beatbar_x, beatbar_y)
    #================#
    self._surface.blit(beatbar.draw(), beatbar.parent_space_rect)

  def set_colorkey(self, colorkey):
    self._surface.set_colorkey(colorkey)

  
      
if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  #================#
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  melody = Midi('Breath.mid').beats()
  #================#
  melody_viewer = MelodyViewer(melody_null_n_beats(melody, 5), Piano(mido.open_output(None), Piano.generate_pianokeys_from_beats(melody)))
  melody_viewer.primary_color=CHARLESTON
  melody_viewer.secondary_color=DIM
  melody_viewer.sec2pixel = SCREEN_SIZE[0] / melody_duration(melody)
  #================================================================================================#
  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    melody_viewer.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(melody_viewer.draw(), melody_viewer.world_space_rect)
    pygame.display.update()
