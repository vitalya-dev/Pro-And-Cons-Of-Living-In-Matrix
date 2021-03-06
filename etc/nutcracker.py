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
    if not self._is_playing:
      self._input_time = 0
      self._is_playing = True
      self._non_played_timeline_events = self._timeline_events.copy()

  def process(self, events):
    if self._is_playing:
      self._input_time += clock.get_time()
      self._call_events_if_time_comes()
      self._remove_played_events()
      if len(self._non_played_timeline_events) == 0:
        self._is_playing = False
        
  def _call_events_if_time_comes(self):
    for event in self._non_played_timeline_events:
      if self._input_time >= event['time']:
        event['func'].__call__()

  def _remove_played_events(self):
    self._non_played_timeline_events = [e for e in self._non_played_timeline_events if e['time'] > self._input_time]


class Effects:
  def __init__(self):
    self._effects = []
  
  def process(self, events):
    for e in self._effects:
      e.process(events)

  def render(self, surface):
    for e in self._effects:
      e.render(surface)

  def create_particle_effect(self, pos, count):
    particle_effect = ParticleEffect()
    particle_effect.position = pos
    particle_effect.count = count
    particle_effect.burst() 
    self._effects.append(particle_effect)

  def create_running_text_effect(self, text, font_size, velocity, pos):
    running_text_effect = RunningTextEffect()
    running_text_effect.velocity = velocity
    running_text_effect.text = text
    running_text_effect.font_size = font_size
    running_text_effect.foreground = '#ffffff'
    running_text_effect.position = pos
    self._effects.append(running_text_effect)


class ParticleEffect:
  def __init__(self):
    self._particles = []
    self.position = (0, 0)
    self.count = 0

  def burst(self):
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

class RunningTextEffect:
  def __init__(self):
    self.position = (0, 0)
    self.velocity = (0, 0)
    #================#
    self._text = ''
    self._font_size = FONT_SIZE
    self._foreground = pygame.Color('#000000')
    self._surface = font.render(self._text, False, self._foreground)
    #================#

  @property
  def text(self):
    return self._text

  @text.setter
  def text(self, value):
    self._text = value
    self._update_surface()
  
  @property
  def font_size(self):
    return self._font_size

  @font_size.setter
  def font_size(self, value):
    self._font_size = value
    self._update_surface()

  @property
  def foreground(self):
    return self._foreground

  @foreground.setter
  def foreground(self, value):
    self._foreground = pygame.Color(value) if type(value) == type('') else value
    self._update_surface()


  def _update_surface(self):
    font = pygame.font.Font('data/FSEX300.ttf', self._font_size)
    self._surface = font.render(self._text, False, self._foreground)

  def process(self, events):
    movement = tuple_math(self.velocity, '*', clock.get_time() * MSEC2SEC)
    self.position = tuple_math(self.position, '+', movement)

  def render(self, surface):
    surface.blit(self._surface, self.position)


#================================================================#
if __name__ == '__main__':
  #================#
  clang = pygame.mixer.Sound('sounds/clang.wav')
  pain_1 = pygame.mixer.Sound('sounds/pain_1.wav')
  #================#
  effects = Effects()
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

  nutcracker = FrameRenderer()
  nutcracker.pivot = (0.5, 0.5)
  nutcracker.position = tuple_math(screen.get_rect().center, '+', (0, 125))
  nutcracker.frame = nutcracker_frame_1
  #================#
  nutcracking_timeline = Timeline()
  nutcracking_timeline.add_event(0, lambda: clang.play())
  nutcracking_timeline.add_event(100, lambda: nutcracker.set_frame(nutcracker_frame_2))
  nutcracking_timeline.add_event(100, lambda: nutcracker.move(0, -80))

  nutcracking_timeline.add_event(110, lambda: effects.create_particle_effect(pos=tuple_math(nutcracker.position, '-', (0, 75)), count=10))

  nutcracking_timeline.add_event(200, lambda: mr_pleasant.set_frame(mr_pleasant_frame_2))

  nutcracking_timeline.add_event(2000, lambda: nutcracker.set_frame(nutcracker_frame_1))
  nutcracking_timeline.add_event(2000, lambda: nutcracker.move(0, 80))

  nutcracking_timeline.add_event(3000, lambda: pain_1.play())
  nutcracking_timeline.add_event(3000, lambda: effects.create_running_text_effect(text='A'*20, font_size=150, velocity=(-500, 0), pos=(640, 0)))

  nutcracking_timeline.add_event(9000, lambda: mr_pleasant.set_frame(mr_pleasant_frame_1))
  #================#
  keyboard = Keyboard()
  keyboard.on_esc += [lambda: done(True)]
  keyboard.on_space += [lambda: nutcracking_timeline.play()]

  while not done():
    clock.tick()
    #PROCESS INPUT
    events = pygame.event.get()
    keyboard.process(events)
    effects.process(events)
    nutcracking_timeline.process(events)
    #RENDER
    screen.fill(pygame.Color('#000000'))
    mr_pleasant.render(screen)
    nutcracker.render(screen)
    effects.render(screen)
    pygame.display.update()
  #================#
