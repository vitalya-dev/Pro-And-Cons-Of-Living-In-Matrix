import mido

from constants import *
from utils import *

class Piano(object):
  def __init__(self, midioutput):
    self.midioutput = midioutput

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


if __name__ == '__main__':
  midioutput = mido.open_output(None)
  #===================#
  print(read_midi_notes('Breath.mid'))
  piano = Piano(midioutput)
