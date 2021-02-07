import math

import pygame
from pygame.locals import *

from constants import *
from utils import *

from piano import *
from midi import *
from shape import *
from label import *

class BeatsViewer(Shape):
  def __init__(self, beats, piano, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self.beats = beats
    self.piano = piano
    #================#
    self.sec2pixel = SEC2PIXEL
    self.pitch2pixel = PITCH2PIXEL
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
    self._surface.set_colorkey(BLACK)

  def process(self, events):
    pass

  def draw(self):
    self._draw_background()
    self._draw_beats()
    return self._surface

  def _draw_background(self):
    self._surface.fill(BLACK)

  def _draw_beats(self):
    for beat in self.beats:
      self._draw_beatbar(beat)

  def _draw_beatbar(self, beat):
    if is_null_beat(beat):
      return
    #================#
    beatbar_width = beat_duration(beat) * self.sec2pixel - self.padding
    beatbar_height = self.pitch2pixel
    beatbar_x = self.time_to_x(beat[0].time)
    beatbar_y = self.pitch_to_y(beat[0].note)
    beatbar_text = self.piano.keys[beat[0].note]
    #================#
    beatbar = Label(beatbar_text, size=(beatbar_width, beatbar_height), parent=self)
    beatbar.primary_color = self.primary_color
    beatbar.secondary_color = self.secondary_color
    beatbar.position = (beatbar_x, beatbar_y)
    #================#
    self._surface.blit(beatbar.draw(), beatbar.parent_space_rect)
  
  def time_to_x(self, time):
    return time * self.sec2pixel

  def pitch_to_y(self, pitch):
    return (self.piano.keys['F'] - pitch) * self.pitch2pixel + self._surface.get_height() / 2 - self.pitch2pixel

      
if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  #================#
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  beats = Midi('Breath.mid').beats()
  #================#
  beats_viewer = BeatsViewer(null_beats(beats, [5, 11]), Piano(mido.open_output(None), Piano.generate_pianokeys_from_beats(beats)))
  beats_viewer.primary_color=DIM
  beats_viewer.secondary_color=CHARLESTON
  beats_viewer.sec2pixel = SCREEN_SIZE[0] / beats_duration(beats)
  #================================================================================================#
  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    beats_viewer.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(beats_viewer.draw(), beats_viewer.world_space_rect)
    pygame.display.update()
