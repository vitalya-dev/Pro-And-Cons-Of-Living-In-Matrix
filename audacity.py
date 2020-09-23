import wave
import sys
import numpy
import matplotlib.pyplot as plt

def linspace(start, stop, num=50):
  delta = stop - start
  div = num - 1
  step = delta / div


w = wave.open("Live Ouside Instrumental 2.wav", "r")

rate = w.getframerate()
data = numpy.frombuffer(w.readframes(-1), "Int16")

print(len(data) / rate)

Time = numpy.linspace(0, len(data) / rate, num=len(data))

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(Time, data)
plt.show()

# import matplotlib.pyplot as plt
# import numpy as np
# import wave
# import sys


# spf = wave.open("Animal_cut.wav", "r")

# # Extract Raw Audio from Wav File
# signal = spf.readframes(-1)
# signal = np.fromstring(signal, "Int16")
# fs = spf.getframerate()

# # If Stereo
# if spf.getnchannels() == 2:
#     print("Just mono files")
#     sys.exit(0)


# Time = np.linspace(0, len(signal) / fs, num=len(signal))

# plt.figure(1)
# plt.title("Signal Wave...")
# plt.plot(Time, signal)
# plt.show()


