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
    self.state = 'IDLE'
    #================#
    self.currently_played_beat = None
    self.played_beats_stack = []
    #================#
    self._rewind = 0
    self._start_time = 0

  def play(self, beats=None):
    if self.state == 'IDLE':
      self.state = 'PLAY'
      threading.Thread(target=self._play_thread, args=(beats,)).start()
  
  def _play_thread(self, beats):
    self._start_time = time.time()
    self.currently_played_beat = None
    self.played_beats_stack = []
    #================#
    self._rewind_if_beats_delayed(beats)
    for beat in beats:
      self.currently_played_beat = beat
      #================#
      self._try_to_play_beat_pieces_in_right_tempo(beat[0])
      self._try_to_play_beat_pieces_in_right_tempo(beat[1])
      #================#
      self.played_beats_stack.append(beat)
    #================#
    self.state = 'IDLE'

  def _rewind_if_beats_delayed(self, beats):
    self._rewind = beats[0][0].time if len(beats) > 0 else 0

  def _try_to_play_beat_pieces_in_right_tempo(self, beat_pieces):
    if beat_pieces.note == 0:
      return
    #================#
    playback_time = time.time() - self._start_time 
    total_time = playback_time + self._rewind
    #================#
    if beat_pieces.time > total_time:
      time.sleep(beat_pieces.time - total_time)
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
