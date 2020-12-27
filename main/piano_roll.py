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
    self._play = False

  def start_or_stop_playing_beats(self, beats=None):
    if not self._play:
      self._play = True
      threading.Thread(target=self._play_thread, args=(beats,)).start()
    else:
      self._play = False

  def stop(self):
    self._play = False

  def _play_thread(self, beats):
    start_time = time.time()
    beats_stream = sorted(flatten(beats), key=lambda beat: beat.time)
    for beat in beats_stream:
      playback_time = time.time() - start_time
      if beat.time - playback_time > 0:
        time.sleep(beat.time - playback_time)
      self.midioutput.send(beat)
      if not self._play:
        break
    self._play = False


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  midioutput = mido.open_output(None)
  piano_roll = PianoRoll(midioutput)

  keyboard = Keyboard()
  keyboard.on_space += [lambda: piano_roll.start_or_stop_playing_beats(Midi('Breath.mid').beats())]

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    keyboard.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    pygame.display.update()
