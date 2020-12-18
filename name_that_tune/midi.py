import mido

from constants import *
from utils import *

class Midi(object):
  def __init__(self, midifile):
    self.all_messages_with_deltatime = self._read_all_messages(midifile)
    self.all_messages_with_abstime = self._generate_abstime_messages_from_deltatime_messages(self.all_messages_with_deltatime)

  def _read_all_messages(self, midifile):
    return list(mido.MidiFile(midifile))

  def _generate_abstime_messages_from_deltatime_messages(self, deltatime_messages):
    abstime_messages = []
    #==============#
    now = 0
    for message in deltatime_messages:
      now += message.time
      abstime_messages.append(message.copy(time=now))
    #==============#
    return abstime_messages

  def beats(self):
    beat_ons = [message for message in self.all_messages_with_abstime if message.type == 'note_on']
    beat_offs = [message for message in self.all_messages_with_abstime if message.type == 'note_off']
    #==============#
    all_beats =  []
    for beat_on in beat_ons:
      i = self._find_note_in_beats(beat_offs, beat_on.note)
      if i >= 0:
        all_beats.append((beat_on, beat_offs.pop(i)))
    #==============#
    return all_beats

  def _find_note_in_beats(self, beats, note):
    return find(beats, lambda x: x.note == note)[0]

  def beats_stream(self):
    return sorted(flatten(self.beats()), key=lambda beat: beat.time)

  def duration(self):
    if len(self.beats_stream()) > 0:
      last_beat = self.beats_stream()[-1]
      return last_beat.time
    else:
      return 0


if __name__ == '__main__':
  print(Midi('Breath.mid').beats_stream())
  print(Midi('Breath.mid').duration())
  



