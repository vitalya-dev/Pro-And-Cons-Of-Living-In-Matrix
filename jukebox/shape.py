import pygame

import utils

class Shape(object):
  def __init__(self):
    self.position = (0, 0)
    self.size = (0, 0)
    self.pivot = (0.5, 0.5)

  @property
  def rect(self):
    return pygame.Rect(self._top_left_position(), self.size)

  def _top_left_position(self):
    pivot_position = utils.tuple_math(self.pivot, '*', self.size)
    pivot_position_as_int = tuple(map(int, pivot_position))
    return utils.tuple_math(self.position, '-', pivot_position_as_int)
