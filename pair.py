import math

class Pair(object):
  def __init__(self, a=0, b=0):
    self.a = a
    self.b = b
    self.thresh = 0.00001

  def as_tuple(self):
    return (self.a, self.b)

  def __add__(self, other):
    if type(other) == type(self):
      return Pair(self.a + other.a, self.b + other.b)
    elif type(other) == type(tuple()):
      return Pair(self.a + other[0], self.b + other[1])
    else:
      raise Exception('Something wrong added to pair')

  def __sub__(self, other):
    if type(other) == type(self):
      return Pair(self.a + other.a, self.b + other.b)
    elif type(other) == type(tuple()):
      return Pair(self.a + other[0], self.b + other[1])
    else:
      raise Exception('Something wrong added to pair')
    return Pair(self.a - other.a, self.b - other.b)

  def __neg__(self):
    return Pair(-self.a, -self.b)

  def __mul__(self, scalar):
    return Pair(self.a * scalar, self.b * scalar)

  def __div__(self, scalar):
    if scalar != 0:
      return Pair(self.a / scalar, self.b / scalar)
    return None
    
  def __eq__(self, other):
    if abs(self.a - other.a) < self.thresh and abs(self.b - other.b) < self.thresh:
      return True
    else:
      return False
