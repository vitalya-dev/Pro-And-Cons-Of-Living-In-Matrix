import random
import itertools
import operator

import pygame
from pygame.locals import *

#================================================================#
SCREEN_SIZE = (640, 480)
FONT_SIZE = 32
MSEC2SEC = 0.001
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

def scale_frame(frame, factor):
  return pygame.transform.scale(frame, tuple_math(frame.get_size(), '*', factor))
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
  def __init__(self):
    self.frame = None
    self.position = (0, 0)
    self.pivot = (0.5, 0.5)

  def set_frame(self, frame):
    self.frame = frame

  def move(self, dx, dy):
    self.position = tuple_math(self.position, '+', (dx, dy))

  def render(self, surface):
    surface.blit(self.frame, self.frame_top_left_position)
    pass

  @property
  def frame_top_left_position(self):
    pivot_position = tuple_math(self.pivot, '*', self.frame.get_size())
    pivot_position_as_int = tuple(map(int, pivot_position))
    return tuple_math(self.position, '-', pivot_position_as_int)

class Timeline(object):
  def __init__(self):
    self._timeline_events = []
    self._non_played_timeline_events = []
    self._input_time = 0
    self._is_playing = False

  def add_event(self, time, event_func):
    self._timeline_events.append(
      {'time': time, 'func': event_func}
    )
    self._timeline_events.sort(key=lambda e: e['time'])

  def play(self):
    self._input_time = 0
    self._is_playing = True
    self._non_played_timeline_events = self._timeline_events.copy()

  def process(self, events):
    if self._is_playing:
      self._input_time += clock.get_time()
      self._call_events_if_time_comes()
      self._remove_played_events()
      if len(self._non_played_timeline_events) == 0:
        self_is_playing = False
        
  def _call_events_if_time_comes(self):
    for event in self._non_played_timeline_events:
      if self._input_time >= event['time']:
        event['func'].__call__()

  def _remove_played_events(self):
    self._non_played_timeline_events = [e for e in self._non_played_timeline_events if e['time'] > self._input_time]


class ParticleEmitter:
  def __init__(self):
    self._particles = []
    self.position = (0, 0)
    self.count = 0

  def emit(self):
    for i in range(0, self.count):
      self._particles.append({
        'position' : self.position,
        'radius'   : random.randint(0, 10),
        'velocity' : random_couple(-150, 150),
        'color'    : random_triple(0, 255)
      })

  def process(self, events):
    for particle in self._particles:
      movement = tuple_math(particle['velocity'], '*', clock.get_time() * MSEC2SEC)
      particle['position'] = tuple_math(particle['position'], '+', movement)

  def render(self, surface):
    for particle in self._particles:
      pygame.draw.circle(surface, particle['color'], tuple(map(int, particle['position'])), particle['radius'])


#================================================================#
if __name__ == '__main__':
  #================#
  mr_pleasant_frame_1 = scale_frame(load_frame('graphics/mr_pleasant_1.png'), 14)
  mr_pleasant_frame_2 = scale_frame(load_frame('graphics/mr_pleasant_2.png'), 14)
  
  nutcracker_frame_1 = scale_frame(rotate_frame(load_frame('graphics/nutcracker.png'), 180), 14)
  nutcracker_frame_2 = scale_frame(load_frame('graphics/nutcracker.png'), 14)
  nutcracker_frame_3 = scale_frame(rotate_frame(load_frame('graphics/nutcracker.png'), 180), 14)
  #================#
  mr_pleasant = FrameRenderer()
  mr_pleasant.pivot = (0.5, 0.5)
  mr_pleasant.position = tuple_math(screen.get_rect().center, '-', (0, 75))
  mr_pleasant.frame = mr_pleasant_frame_1
  #================#
  nutcracker = FrameRenderer()
  nutcracker.pivot = (0.5, 0.5)
  nutcracker.position = tuple_math(screen.get_rect().center, '+', (0, 125))
  nutcracker.frame = nutcracker_frame_1
  #================#
  particle_emitter = ParticleEmitter()
  particle_emitter.position = tuple_math(nutcracker.position, '+', (0, -150))
  particle_emitter.count = 25
  #================#
  nutcracking_timeline = Timeline()
  nutcracking_timeline.add_event(0, lambda: nutcracker.set_frame(nutcracker_frame_2))
  nutcracking_timeline.add_event(0, lambda: nutcracker.move(0, -80))
  nutcracking_timeline.add_event(0, lambda: particle_emitter.emit())
  #================#
  keyboard = Keyboard()
  keyboard.on_esc += [lambda: done(True)]
  keyboard.on_space += [lambda: nutcracking_timeline.play()]

  while not done():
    clock.tick()
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    particle_emitter.process(events)
    nutcracking_timeline.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    mr_pleasant.render(screen)
    nutcracker.render(screen)
    particle_emitter.render(screen)
    pygame.display.update()
  #================#
