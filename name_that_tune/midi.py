import mido

from constants import *
from utils import *

class Midi(object):
  def __init__(self, midifile):
    self.all_messages_with_deltatime = self._read_all_messages(midifile)
    self.all_messages_with_abstime = self._generate_abstime_messages_from_deltatime_messages(self.all_messages_with_delta_time)

  def _read_all_messages(self, midifile):
    return list(mido.MidiFile(midifile))

  def _generate_abstime_messages_from_deltatime_messages(self, deltatime_messages):
    abstime_messages = []
    #==============#
    now = 0
    for message in deltatime_messages:
      now += message.time
      abstime.messages.append(message.copy(time=now))
    #==============#
    return abstime_messages

  @property
  def notes(self):
    note_ons = [message for message in self.all_messages_with_abstime if message.type == 'note_on']
    note_offs = [message for message in self.all_messages_with_abstime if message.type == 'note_off']
    #==============#
    all_notes =  []
    for note_on in note_ons:
      i = find_note_in_notes(note_offs, lambda x: x.note == note_on.note)[0]
      if i >= 0:
        all_notes.append((note_on, note_offs.pop(i)))
    #==============#
    return all_notes



