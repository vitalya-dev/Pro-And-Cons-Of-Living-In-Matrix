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
  def __init__(self, midioutput, beats):
    self.midioutput = midioutput
    self.beats = beats
    self._play = False

  def toggle(self):
    self._play = not self._play
    if self._play:
      threading.Thread(target=self._play_thread).start()

  def play(self, beats):
    if not self._play:
      self._play = True
      threading.Thread(target=self._play_thread, args=(beats,)).start()

  def _play_thread(self, beats):
    start_time = time.time()
    beats_stream = sorted(flatten(self.beats), key=lambda beat: beat.time)
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
  piano_roll = PianoRoll(midioutput, Midi('Breath.mid').beats())

  keyboard = Keyboard()
  keyboard.on_space += [lambda: piano_roll.toggle()]

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    keyboard.process(events)
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    pygame.display.update()
