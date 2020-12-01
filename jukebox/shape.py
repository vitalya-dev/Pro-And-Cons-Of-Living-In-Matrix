import pygame

import utils

class Shape(object):
  def __init__(self):
    self.position = (0, 0)
    self.pivot = (0, 0)
    self._surface = pygame.surface.Surface((0, 0)).convert()

  @property
  def world_space_rect(self):
    return self._surface.get_rect(topleft=self._calculate_topleft_position())

  @property
  def self_space_rect(self):
    return self._surface.get_rect()

  def _calculate_topleft_position(self):
    pivot_position = utils.tuple_math(self.pivot, '*', self._surface.get_size())
    pivot_position_as_int = tuple(map(int, pivot_position))
    return utils.tuple_math(self.position, '-', pivot_position_as_int)
