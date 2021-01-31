import time
import threading
import mido
import pygame
from pygame.locals import *

from midi import *
from constants import *
from utils import *
from keyboard import *

class BeatsRoll(object):
  def __init__(self, midioutput):
    self.midioutput = midioutput
    #================#
    self.state = 'WAIT'
    #================#
    self.play_when_already_playing_interrupt = False
    self.zero_beat_interrupt = False
    self.zero_beat = None
    #================#
    self._start_time = 0


  def play(self, beats=None):
    if self.state == 'PLAYING':
      self.play_when_already_playing_interrupt = True
      self.state = 'INTERRUPT'
    elif self.state in ('WAIT', 'COMPLETE', 'INTERRUPT'): 
      self.state = 'PLAYING'
      threading.Thread(target=self._play_thread, args=(beats,)).start()
    

  def _play_thread(self, beats):
    self._start_time = time.time()
    self.play_when_already_playing_interrupt = False
    self.zero_beat_interrupt = False
    self.zero_beat = None
    #================#
    for beat in beats:
      self._try_to_play_beat_pieces_in_right_tempo(beat[0])
      self._try_to_play_beat_pieces_in_right_tempo(beat[1])
      if self.zero_beat_interrupt:
        self.state = 'INTERRUPT'
        self.zero_beat = beat
        return
      if self.play_when_already_playing_interrupt:
        self.state = 'INTERRUPT'
        return
    #================#
    self.state = 'COMPLETE'

  def _try_to_play_beat_pieces_in_right_tempo(self, beat_pieces):
    if beat_pieces.note == 0:
      self.zero_beat_interrupt = True
      return
    #================#
    playback_time = time.time() - self._start_time
    if beat_pieces.time > playback_time:
      time.sleep(beat_pieces.time - playback_time)
    self.midioutput.send(beat_pieces)


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  midioutput = mido.open_output(None)
  beats_roll = BeatsRoll(midioutput)

  keyboard = Keyboard()
  keyboard.on_space += [lambda: beats_roll.play(Midi('Breath.mid').beats())]

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    keyboard.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    pygame.display.update()
