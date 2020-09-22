import wave
import sys


spf = wave.open("Live Ouside Instrumental.wav", "r")
print(spf.readframes(-1))

