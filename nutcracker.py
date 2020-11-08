import random
import itertools
from couple import Couple

import pygame
from pygame.locals import *


#================================================================#
SCREEN_SIZE = (640, 480)
FONT_SIZE   = 32
#================================================================#


#================================================================#
pygame.init()
random.seed()
#================================================================#

#================================================================#
screen     = pygame.display.set_mode(SCREEN_SIZE)
clock      = pygame.time.Clock()
font       = pygame.font.Font('data/FSEX300.ttf', FONT_SIZE - 1)
#================================================================#

#================================================================#
def done(val=None):
  if not hasattr(done, 'val'): done.val = False
  if val == None: return done.val
  done.val = val;

def multiply(l1, l2):
  from operator import mul
  return tuple(map(mul, l1, l2))

def to_int(l):
  return tuple(map(int, l))

def random_pair(a, b):
  return (random.randint(a, b), random.randint(a, b))

def random_triple(a, b):
  return (random.randint(a, b), random.randint(a, b), random.randint(a, b))
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

class Particles:
  def __init__(self):
    self._particles = []

  def generate(self, position, n):
    for i in range(0, n):
      self._particles.append({
        'position' : position.copy(),
        'radius'   : random.randint(0, 10),
        'velocity' : Couple(*random_pair(-150, 150)),
        'color'    : random_triple(0, 255)
      })

  def process(self, events):
    for particle in self._particles:
      particle['position'] += particle['velocity'] * clock.get_time() * 0.001

  def render(self, surface):
    for particle in self._particles:
      pygame.draw.circle(surface, particle['color'], to_int(particle['position'].as_tuple()), particle['radius'])

class Framesheet(object):
  def __init__(self, *frames):
    self.frames = [self._load(frame) if type(frame) == type(str()) else frame.copy() for frame in frames]
    self.frame_offsets = list(itertools.repeat((0, 0), len(self.frames)))
    self.position = Couple(0, 0)
    self.pivot = Couple(0, 0)
    self._current_frame_index = 0 

  def _load(self, frame_name):
    frame_name_parts = frame_name.split(':')
    if len(frame_name_parts) == 1:
      return pygame.image.load(frame_name_parts[0]).convert_alpha()
    elif len(frame_name_parts) == 3:
      return self._load_and_translate(frame_name_parts[0], frame_name_parts[1], frame_name_parts[2])
    else:
      return pygame.image.load(frame_name_parts[-1]).convert_alpha()

  def _load_and_translate(self, translate_function, translate_param, frame_name):
    if translate_function == 'r':
      translate_param = int(translate_param)
      return pygame.transform.rotate(pygame.image.load(frame_name).convert_alpha(), translate_param)
    if translate_function == 's':
      translate_param = int(translate_param)
      frame = pygame.image.load(frame_name).convert_alpha()
      return pygame.transform.scale(frame, multiply(frame.get_size(), (translate_param, translate_param)))
    else:
      return pygame.image.load(frame_name)

  @property
  def current_frame(self):
    return self.frames[self._current_frame_index]

  @current_frame.setter
  def current_frame(self, current):
    self._current_frame_index = self.frames.index(current)

  @property
  def current_index(self):
    return self._current_frame_index

  @property
  def last_frame(self):
    return self.frames[-1]

  @property
  def frame_position(self):
    return self.position - self.pivot * self.current_frame.get_size() + self.frame_offsets[self.current_index]

  def next_frame(self):
    self._current_frame_index = (self._current_frame_index + 1) % len(self.frames)

  def render(self, surface):
    surface.blit(self.current_frame, to_int(self.frame_position))

  def scale(self, scale_factor):
    return Framesheet(*[pygame.transform.scale(frame, multiply(frame.get_size(), (scale_factor, scale_factor))) for frame in self.frames])

  def __getitem__(self, index):
    return self.frames[index]

  def __str__(self):
    return str(self.frames)

#================================================================#

if __name__ == '__main__':
  #================#
  mr_pleasant = Framesheet("graphics/mr_pleasant_1.png", "graphics/mr_pleasant_2.png", "graphics/mr_pleasant_2.png").scale(14)
  mr_pleasant.pivot = Couple(0.5, 0.5)
  mr_pleasant.position = Couple(*screen.get_rect().center) + (0, -75)
  #================#
  nutcracker = Framesheet("r:180:graphics/nutcracker.png", "graphics/nutcracker.png", "r:180:graphics/nutcracker.png").scale(14)
  nutcracker.position  = Couple(*screen.get_rect().center) + (0, 125)
  nutcracker.pivot = Couple(0.5, 0.5)
  nutcracker.frame_offsets = [(0, 0), (0, -80), (0, 0)]
  #================#
  particles = Particles()
  #================#
  keyboard = Keyboard()
  keyboard.on_space += [lambda: mr_pleasant.next_frame()]
  keyboard.on_space += [lambda: nutcracker.next_frame()]
  keyboard.on_space += [lambda: particles.generate(nutcracker.position + (0, -150), 25) if nutcracker.current_index == 1 else ...]
  keyboard.on_esc   += [lambda: done(True)]
  #================#

  while not done():
    clock.tick()
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    particles.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    mr_pleasant.render(screen)
    nutcracker.render(screen)
    particles.render(screen)
    pygame.display.update()
