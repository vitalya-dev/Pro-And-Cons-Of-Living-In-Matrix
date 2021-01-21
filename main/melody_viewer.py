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
  def __init__(self, melody, size, background_color=BLACK, foreground_color=WHITE, text_color=GRAY, parent=None):
    super().__init__(parent)
    #================#
    self.background_color = background_color
    self.foreground_color = foreground_color
    self.text_color = text_color
    #================#
    self._surface = pygame.surface.Surface(size).convert()
    #================#
    self._melody = melody
    self._pianokeys = Piano.generate_pianokeys_from_beats(self._melody)
    #================#
    self._melody_beatbars = self._create_melody_beatbars()
    #================#
    self._show_only_this_beats = 'ALL'


  def process(self, events):
    pass

  @property
  def time_to_pixel_scale(self):
    melody_length = self._melody[-1][1].time
    return self._surface.get_width() / melody_length

  def _create_melody_beatbars(self):
    melody_beatbars = []
    for beat in self._melody:
      beatbar_height = self._surface.get_height() / 10
      beatbar_left = beat[0].time * self.time_to_pixel_scale
      beatbar_width = (beat[1].time - beat[0].time) * self.time_to_pixel_scale - 1
      beatbar_top = (self._pianokeys['F'] - beat[0].note) * beatbar_height + self._surface.get_height() / 2 - beatbar_height
      beatbar_text = self._pianokeys[beat[0].note]
      #================#
      beatbar = Label(
        beatbar_text, background_color=self.foreground_color, text_color=self.text_color, size=(beatbar_width, beatbar_height), parent=self
      )
      beatbar.position = (beatbar_left, beatbar_top)
      melody_beatbars.append(beatbar)
    return melody_beatbars

  def show_only_this_beats(self, beats_to_show):
    self._show_only_this_beats = beats_to_show

  def draw(self):
    self._draw_background()
    self._draw_melody()
    return self._surface

  def _draw_background(self):
    self._surface.fill(self.background_color)

  def _draw_melody(self):
    if self._show_only_this_beats == 'ALL':
      self._draw_melody_all_beats()
    if self._show_only_this_beats == 'EVERY SECOND':
      self._draw_melody_every_x_beats(2)
    if self._show_only_this_beats == 'EVERY THIRD':
      self._draw_melody_every_x_beats(3)
    if self._show_only_this_beats == 'ALL EXCEPT ONE':
      self._draw_melody_all_except_n_beats(1)
    if self._show_only_this_beats == 'ALL EXCEPT TWO':
      self._draw_melody_all_except_n_beats(2)
    if self._show_only_this_beats == 'ALL EXCEPT THREE':
      self._draw_melody_all_except_n_beats(3)
    if self._show_only_this_beats == 'ALL EXCEPT FOUR':
      self._draw_melody_all_except_n_beats(4)
    if self._show_only_this_beats == 'ALL EXCEPT FIFE':
      self._draw_melody_all_except_n_beats(5)
    if self._show_only_this_beats == 'ALL EXCEPT SIX':
      self._draw_melody_all_except_n_beats(6)

  def _draw_melody_all_beats(self):
    for beatbar in self._melody_beatbars:
      self._surface.blit(beatbar.draw(), beatbar.parent_space_rect)

  def _draw_melody_every_x_beats(self, x):
    for beatbar in self._melody_beatbars[::x]:
      self._surface.blit(beatbar.draw(), beatbar.parent_space_rect)

  def _draw_melody_all_except_n_beats(self, n):
    for beatbar in same_seq_except_n_elements(self._melody_beatbars, n):
      self._surface.blit(beatbar.draw(), beatbar.parent_space_rect)

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

  melody_viewer = MelodyViewer(Midi('Breath.mid').beats(), SCREEN_SIZE)
  melody_viewer.show_only_this_beats('ALL EXCEPT SIX')

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    melody_viewer.process(events)
    piano.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(melody_viewer.draw(), melody_viewer.world_space_rect)
    pygame.display.update()
