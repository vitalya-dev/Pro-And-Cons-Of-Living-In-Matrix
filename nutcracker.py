import random
import itertools
import operator

import pygame
from pygame.locals import *

#================================================================#
SCREEN_SIZE = (640, 480)
FONT_SIZE = 32
#================================================================#


#================================================================#
pygame.init()
random.seed()
#================================================================#

#================================================================#
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.Font('data/FSEX300.ttf', FONT_SIZE - 1)
#================================================================#


#================================================================#
def done(val=None):
  if not hasattr(done, 'val'): done.val = False
  if val == None: return done.val
  done.val = val;

def random_couple(a, b):
  return (random.randint(a, b), random.randint(a, b))

def random_triple(a, b):
  return (random.randint(a, b), random.randint(a, b), random.randint(a, b))

def tuple_math(a, op, b):
  if not hasattr(b, "__getitem__"):
    b = (b,) * len(a)
  if op == '+':
    return tuple(map(operator.add, a, b))
  if op == '-':
    return tuple(map(operator.sub, a, b))
  if op == '*':
    return tuple(map(operator.mul, a, b))

def load_frame(frame_name):
  return pygame.image.load(frame_name).convert_alpha()

def rotate_frame(frame, angle):
  return pygame.transform.rotate(frame, angle)
#================================================================#

#================================================================#
class Keyboard(object):
  def __init__(self):
    self.on_esc   = []
    self.on_space = []

  def process(self, events):
    for e in events:
      if e.type == KEYDOWN and e.key == K_ESCAPE:
        for c in self.on_esc: c()
      if e.type == KEYDOWN and e.key == K_SPACE:
        for c in self.on_space: c()

class FrameRenderer(object):
  def render(self, surface):
    pass

#================================================================#

mr_pleasant_frame_1 = load_frame('graphics/mr_pleasant_1.png')
mr_pleasant_frame_2 = load_frame('graphics/mr_pleasant_2.png')  

nutcracker_frame_1 = rotate_frame(load_frame('graphics/nutcracker.png'), 180)
nutcracker_frame_2 = load_frame('graphics/nutcracker.png')
nutcracker_frame_3 = rotate_frame(load_frame('graphics/nutcracker.png'), 180)


if __name__ == '__main__':
  #================#
  keyboard = Keyboard()
  keyboard.on_esc += [lambda: done(True)]
  #================#
  mr_pleasant = FrameRenderer()
  mr_pleasant.pivot = (0.5, 0.5)
  mr_pleasant.position = tuple_math(screen.get_rect().center, '-', (0, 75))
  mr_pleasant.set_frame(mr_pleasant_frame_1)
  #================#
  nutcracker = FrameRenderer()
  nutcracker.pivot = (0.5, 0.5)
  nutcracker.position = tuple_math(screen.get_rect().center, '-', (0, 75))
  #================#

  #================#
  while not done():
    clock.tick()
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    mr_pleasant.render(screen)
    pygame.display.update()
  #================#
