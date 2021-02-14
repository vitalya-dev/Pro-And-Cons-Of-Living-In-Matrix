import math

import mido
import pygame
from pygame.locals import *

from midi import *
from constants import *
from utils import *

class Piano(object):
  def __init__(self, midioutput, keys):
    self.midioutput = midioutput
    self.keys = keys

  def process(self, events):
    keys_down = pygame.key.get_pressed()
    for e in events:
      if e.type == KEYDOWN and chr(e.key).upper() in self.keys:
       self.on_key_down(chr(e.key).upper())
      if e.type == KEYUP and chr(e.key).upper() in self.keys:
        self.on_key_up(chr(e.key).upper())
 
  def on_key_down(self, key):
    self.midioutput.send(mido.Message('note_on',  note=self.keys[key]))

  def on_key_up(self, key):
    self.midioutput.send(mido.Message('note_off', note=self.keys[key]))

  @staticmethod
  def generate_pianokeys_from_midi(midi):
    return Piano.generate_pianokeys_from_beats(midi.beats())
   
  @staticmethod
  def generate_pianokeys_from_beats(beats):
    middle_note = math.floor(average([beat[0].note for beat in beats]))
    return {
      'F': middle_note,
      'D': middle_note-1,
      'S': middle_note-2,
      'A': middle_note-3,
      'J': middle_note+1,
      'K': middle_note+2,
      'L': middle_note+3,
      middle_note:   'F',
      middle_note-1: 'D',
      middle_note-2: 'S',
      middle_note-3: 'A',
      middle_note+1: 'J',
      middle_note+2: 'K',
      middle_note+3: 'L',
    }

  @staticmethod
  def grand_piano(midioutput):
    grand_piano_keys = {
      'F': 51,
      'D': 50,
      'S': 49,
      'A': 48,
      'J': 52,
      'K': 53,
      'L': 54,
      51: 'F',
      50: 'D',
      49: 'S',
      48: 'A',
      52: 'J',
      53: 'K',
      54: 'L'
     }
    return Piano(midioutput, grand_piano_keys)
    



if __name__ == '__main__':
  midioutput = mido.open_output(None)
  piano = Piano(midioutput, Piano.generate_pianokeys_from_midi(Midi('Breath.mid')))
  print(Piano.generate_pianokeys_from_beats(Midi('Breath.mid').beats()))
  #===========================================INIT=================================================#
  pygame.init()
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    piano.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    pygame.display.update()
