import time
import threading
import mido
import pygame
from pygame.locals import *

from midi import *
from constants import *
from utils import *
from keyboard import *

class PianoRoll(object):
  def __init__(self, midioutput):
    self.midioutput = midioutput
    self.state = 'WAIT'
    #================#
    self._start_time = 0
    self._interrupted = False

  def play(self, beats=None):
    if self.state == 'PLAY':
      self._interrupted = True
    if self.state in ('WAIT', 'COMPLETE', 'UNCOMPLETE'): 
      self.state = 'PLAY'
      threading.Thread(target=self._play_thread, args=(beats,)).start()
    

  def _play_thread(self, beats):
    self._start_time = time.time()
    self._interrupted = False
    #================#
    beats_stream = sorted(flatten(beats), key=lambda beat: beat.time)
    for beat in beats_stream:
      self._play_beat_in_right_tempo(beat)
      if self._interrupted:
        break;
    #================#
    if self._interrupted:
      self.state = 'UNCOMPLETE' if self._interrupted else 'COMPLETE'

  def _play_beat_in_right_tempo(self, beat):
    if beat.note == 0:
      self._interrupted = True
      return
    #================#
    playback_time = time.time() - self._start_time
    if beat.time > playback_time:
      time.sleep(beat.time - playback_time)
    self.midioutput.send(beat)


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  midioutput = mido.open_output(None)
  piano_roll = PianoRoll(midioutput)

  keyboard = Keyboard()
  keyboard.on_space += [lambda: piano_roll.play(Midi('Breath.mid').beats())]

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    keyboard.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    pygame.display.update()
