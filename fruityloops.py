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

def playback():
  if not hasattr(playback, 'start'): playback.start = time.time()
  return time.time() - playback.start

def timing(note=None):
  if not hasattr(timing, 'time'): timing.time = 0.0
  if not hasattr(timing, 'last_note'): timing.last_note = None
  #===============#
  timing.time += note.time if note else 0.0
  #===============#
  return timing.time - playback()

if __name__ == '__main__':
  filename = sys.argv[1]
  if len(sys.argv) == 3:
      portname = sys.argv[2]
  else:
      portname = None

  with mido.open_output(portname) as output:
    for note in notes(filename) * 10:
      if timing(note) > 0.0: time.sleep(timing())
      output.send(note)

