import time

import pygame
from pygame.locals import *

from constants import *
from utils import *

from piano import *
from midi import *
from shape import *
from label import *

class MelodyEditor(Shape):
  def __init__(self, size=SCREEN_SIZE, parent=None):
    super().__init__(parent)
    #================#
    self.melody_to_edit = []
    #================#
    self.pianokeys = {}
    #================#
    self.primary_color = BLACK
    self.secondary_color = RED
    self.tertiary_color = BLUE
    self.quaternary_color = GREEN
    self.quinary_color = None
    self.senary_color = None
    self.septenary_color = None
    self.octonary_color = None
    #================#
    self.time_to_pixel_scale = 0
    #================#
    self._surface = pygame.surface.Surface(size).convert()

  def process(self, events):
    pass

  def draw(self):
    self._draw_background()
    self._draw_editbars()
    self._highlight_active_editbar()
    self._draw_melody()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self.primary_color, self._surface.get_rect())

  def _draw_editbars(self):
    for beat in self.melody_to_edit:
      self._surface.fill(self.secondary_color, self._beat_to_editbar(beat))

  def _highlight_active_editbar(self):
    if len(self.melody_to_edit) > 0:
      active_beat = self.melody_to_edit[0]
      self._surface.fill(self.tertiary_color, self._beat_to_editbar(active_beat))

  def _draw_melody(self):
    for beat in self.melody_to_edit:
      beatbar = self._beat_to_beatbar(beat)
      self._surface.blit(beatbar.draw(), beatbar.parent_space_rect)
      
  def _beat_to_editbar(self, beat):
    editbar_width = (beat[1].time - beat[0].time) * self.time_to_pixel_scale - 1
    editbar_height = self._surface.get_height()
    editbar_x = beat[0].time * self.time_to_pixel_scale
    editbar_y = 0
    return (editbar_x, editbar_y, editbar_width, editbar_height)
    
  def _beat_to_beatbar(self, beat):
    beatbar_width = (beat[1].time - beat[0].time) * self.time_to_pixel_scale - 1
    beatbar_height = self._surface.get_height() / 10
    beatbar_x = beat[0].time * self.time_to_pixel_scale
    beatbar_y = (self.pianokeys['F'] - beat[0].note) * beatbar_height + self._surface.get_height() / 2 - beatbar_height
    beatbar_text = self.pianokeys[beat[0].note]
    #================#
    beatbar = Label(beatbar_text, size=(beatbar_width, beatbar_height), parent=self)
    beatbar.position = (beatbar_x, beatbar_y)
    return beatbar



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  midioutput = mido.open_output(None)
  piano = Piano(midioutput, Piano.generate_pianokeys_from_midi(Midi('Breath.mid')))
  #================#
  melody = Midi('Breath.mid').beats()
  melody_editor = MelodyEditor()
  melody_editor.melody_to_edit=difference_of_two_seq(melody, same_seq_except_n_elements(melody, 6))
  melody_editor.time_to_pixel_scale = 150
  melody_editor.pianokeys = Piano.generate_pianokeys_from_midi(Midi('Breath.mid'))
  #================================================================================================#
  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    piano.process(events)
    melody_editor.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(melody_editor.draw(), melody_editor.world_space_rect)
    pygame.display.update()
