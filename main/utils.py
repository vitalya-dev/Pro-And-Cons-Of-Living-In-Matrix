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


def same_seq_except_n_elements(seq, n):
  if n == 0:
    return seq
  else:
    middle = math.floor(len(seq) / 2)
    left_seq = same_seq_except_n_elements(seq[:middle], math.floor(n/2))
    right_seq = same_seq_except_n_elements(seq[middle+1:], math.floor((n-1)/2))
    return left_seq + right_seq
    
