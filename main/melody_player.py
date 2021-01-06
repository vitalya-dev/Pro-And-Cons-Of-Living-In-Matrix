import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *
from piano_roll import *
from midi import *


class MelodyPlayer(Shape):
  def __init__(self, midioutput, melody=[], size=SCREEN_SIZE, background_color=WHITE, parent=None):
    super().__init__(parent)
    #================#
    self._melody = melody
    #================#
    self._piano_roll = PianoRoll(midioutput)
    #================#
    self.background_color = background_color
    self._backgrond_image = pygame.image.load('images/music_note.png').convert_alpha()
    self._backgrond_image = pygame.transform.scale(self._backgrond_image, size)
    #================#
    self._surface = pygame.surface.Surface(size).convert()


  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and e.key == K_SPACE:
        self._piano_roll.start_or_stop_playing_beats(self._melody)

  def draw(self):
    self._surface.fill(self.background_color)
    blit_center(target=self._surface, source=self._backgrond_image)
    return self._surface



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  melody_player = MelodyPlayer(midioutput=mido.open_output(None), background_color=PINK, melody=Midi('Breath.mid').beats())

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    melody_player.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(melody_player.draw(), melody_player.world_space_rect.topleft)
    pygame.display.update()
