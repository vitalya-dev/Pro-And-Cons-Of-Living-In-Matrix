import pygame

from utils import *

class Shape(object):
  def __init__(self, parent=None):
    self.parent = parent
    self.position = (0, 0)
    self.pivot = (0, 0)
    self._surface = pygame.surface.Surface((0, 0)).convert()

  def move(self, dx, dy):
    self.position = tuple_math(self.position, '+', (dx, dy))
  
  @property
  def width(self):
    return self.self_space_rect.width

  @property
  def height(self):
    return self.self_space_rect.height

  @property
  def world_space_rect(self):
    if self.parent:
      top_left_pos_relative_to_world = tuple_math(self.parent.world_space_rect.topleft, '+', self.parent_space_rect.topleft)
      return self._surface.get_rect(topleft=top_left_pos_relative_to_world)
    else:
      return self.parent_space_rect

  @property
  def parent_space_rect(self):
    return self._surface.get_rect(topleft=self._calculate_topleft_position())

  @property
  def self_space_rect(self):
    return self._surface.get_rect()

  def _calculate_topleft_position(self):
    pivot_position = tuple_math(self.pivot, '*', self._surface.get_size())
    pivot_position_as_int = tuple(map(int, pivot_position))
    return tuple_math(self.position, '-', pivot_position_as_int)
