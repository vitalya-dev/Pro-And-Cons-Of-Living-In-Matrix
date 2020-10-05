#!/usr/bin/env python
"""
Play MIDI file on output port.
Run with (for example):
    ./play_midi_file.py 'SH-201 MIDI 1' 'test.mid'
"""
import sys
import mido
import time
from mido import MidiFile

def notes(midifile):
  return [message for message in MidiFile(filename) if message.type == 'note_on' or message.type == 'note_off']


if __name__ == '__main__':
  filename = sys.argv[1]
  if len(sys.argv) == 3:
      portname = sys.argv[2]
  else:
      portname = None

  with mido.open_output(portname) as output:
    start_time = time.time()
    input_time = 0.0
    for note in notes(filename) * 10:
      input_time += note.time
      playback_time = time.time() - start_time
      if input_time - playback_time > 0.0: time.sleep(input_time - playback_time)
      output.send(note)
      print(note.dict())

