import copy
import math
import functools
import operator
import pygame


def done(val=None):
  if not hasattr(done, 'val'): done.val = False
  if val == None: return done.val
  done.val = val;

def tuple_math(a, op, b):
  if not hasattr(b, "__getitem__"):
    b = (b,) * len(a)
  if op == '+':
    return tuple(map(operator.add, a, b))
  if op == '-':
    return tuple(map(operator.sub, a, b))
  if op == '*':
    return tuple(map(operator.mul, a, b))
  if op == '/':
    return tuple(map(operator.truediv, a, b))

def average(l):
  return sum(l) / len(l)

def find_index_value(lst, f):
  for i, j in enumerate(lst):
    if f(j): return i, j
  return -1, None

def find_index(lst, f):
  return find_index_value(lst, f)[0]

def find_value(lst, f):
  return find_index_value(lst, f)[1]

def flatten(lst):
  if len(lst) == 0:
    return []
  else:
    return functools.reduce(operator.concat, lst)

def load_frame(frame_name):
  return pygame.image.load(frame_name).convert_alpha()

def rotate_frame(frame, angle):
  return pygame.transform.rotate(frame, angle)

def scale_frame(frame, factor):
  return pygame.transform.scale(frame, tuple_math(frame.get_size(), '*', factor))  


def blit_center(target, source):
  target.blit(source, source.get_rect(center=target.get_rect().center))

def one_eighth_of(val):
  return val / 8.0


def difference_of_two_seq(seq1, seq2):
  return [elem for elem in seq1 if elem not in seq2]


def lerp_color(color_1, color_2, t):
  color_with_float_coeff = tuple_math(color_1, '+', tuple_math(tuple_math(color_2, '-', color_1), '*', t))
  color_with_int_coeff = tuple(map(math.floor, color_with_float_coeff))
  return color_with_int_coeff

def get_event(events, type):
  for e in events:
    if e.type == type: return e
  return None
  
def melody_duration(melody):
  last_beat_in_melody = melody[-1]
  return last_beat_in_melody[1].time


def melody_null_n_beats(melody, n):
  if n == 0:
    return copy.deepcopy(melody)
  else:
    middle = math.floor(len(melody) / 2)
    #================#
    middle_beat = copy.deepcopy(melody[middle])
    middle_beat[0].note = 0
    middle_beat[1].note = 0
    #================#
    left_part_of_melody = melody_null_n_beats(melody[:middle], math.floor(n/2))
    right_part_of_melody = melody_null_n_beats(melody[middle+1:], math.floor((n-1)/2))
    return left_part_of_melody + [middle_beat] + right_part_of_melody

    
