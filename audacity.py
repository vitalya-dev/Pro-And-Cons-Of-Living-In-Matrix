import struct
import wave
import sys
import numpy as np
import matplotlib.pyplot as plt

def linspace(start, stop, num=50):
  delta = stop - start
  div = num - 1
  step = delta / div
  return [start + i * step for i in range(num)]

def read_whole(filename):
    SIZES = {1: 'B', 2: 'h', 4: 'i'}
    CHUNK_SIZE_4096 = 4096
    CHUNK_SIZE_1 = 1
    #======================#
    wav_r = wave.open(filename, 'r')
    #======================#
    channels  = wav_r.getnchannels()
    sampwidth = wav_r.getsampwidth()
    #======================#
    fmt_1 = "<" + SIZES[wav_r.getsampwidth()] * channels * CHUNK_SIZE_4096
    fmt_2 = "<" + SIZES[wav_r.getsampwidth()] * channels * CHUNK_SIZE_1
    #======================#
    ret = []
    while wav_r.tell() < wav_r.getnframes():
      if wav_r.getnframes() - wav_r.tell() >= CHUNK_SIZE_4096:
        decoded = struct.unpack(fmt_1, wav_r.readframes(CHUNK_SIZE_4096))
      else:
        decoded = struct.unpack(fmt_2, wav_r.readframes(CHUNK_SIZE_1))
      for i in decoded: ret.append(i)
    return ret


# def __init__(self, filename, read=True, debug=False):
#     mode = 'r' if read else 'w'
#     sizes = {1: 'B', 2: 'h', 4: 'i'}
#     self.wav = wave.open(filename, mode)
#     ...
#     self.channels = self.wav.getnchannels()
#     self.fmt_size = sizes[self.wav.getsampwidth()]
#     self.fmt = "<" + self.fmt_size * self.channels

  
assert len(linspace(0, 2, 6)) == 6
assert linspace(0, 2, 6)[5] == 2
assert linspace(0, 2, 6)[0] == 0

print(linspace(0, 2, 6))

print(len(read_whole("Live Ouside Instrumental 2.wav")))
#print(len(np.frombuffer(wave.open("Live Ouside Instrumental 2.wav", "r").readframes(-1), "Int16")))


#print(read_whole("Live Ouside Instrumental 2.wav"))
# #w = wave.open("Live Ouside Instrumental 2.wav", "r")
# data = w.readframes(1)

# print(int.from_bytes(data, "little", signed=True))
# print(struct.unpack("<h", data))
# print(numpy.frombuffer(data, "Int16")[0])

# w = wave.open("Live Ouside Instrumental 2.wav", "r")

# rate = w.getframerate()
# data = numpy.frombuffer(w.readframes(-1), "Int16")

# print(len(data) / rate)

# Time = numpy.linspace(0, len(data) / rate, num=len(data))

# plt.figure(1)
# plt.title("Signal Wave...")
# plt.plot(Time, data)
# plt.show()

# # import matplotlib.pyplot as plt
# # import numpy as np
# # import wave
# # import sys


# # spf = wave.open("Animal_cut.wav", "r")

# # # Extract Raw Audio from Wav File
# # signal = spf.readframes(-1)
# # signal = np.fromstring(signal, "Int16")
# # fs = spf.getframerate()

# # # If Stereo
# # if spf.getnchannels() == 2:
# #     print("Just mono files")
# #     sys.exit(0)


# # Time = np.linspace(0, len(signal) / fs, num=len(signal))

# # plt.figure(1)
# # plt.title("Signal Wave...")
# # plt.plot(Time, signal)
# # plt.show()


# def read_whole(filename):
#     wav_r = wave.open(filename, 'r')
#     ret = []
#     while wav_r.tell() < wav_r.getnframes():
#         decoded = struct.unpack("<h", wav_r.readframes(1))
#         ret.append(decoded)
#     return ret

# def read_whole(filename):
#   wav_r = wave.open(filename, 'r')
#   ret = []
#   while wav_r.tell() < wav_r.getnframes():
#     decoded = int.from_bytes(wav_r.readframes(1), "little", signed=True)
#     ret.append(decoded)
#   return ret


#print(int.from_bytes(data, "little", signed=True))

# def read_whole(filename):
#   sizes = {1: 'B', 2: 'h', 4: 'i'}
#   wav_r = wave.open(filename, 'r')
#   ret = []
#   while wav_r.tell() < wav_r.getnframes():
#     decoded = int.from_bytes(wav_r.readframes(1), "little", signed=True)
#     ret.append(decoded)
#   return ret
