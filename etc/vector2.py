import math

class Vector2(object):
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
    self.thresh = 0.00001

  def copy(self):
    return Vector2(self.x, self.y)

  def dot(self, other):
    return self.x * other.x + self.y * other.y

  def normalize(self):
    mag = self.magnitude()
    if mag != 0:
      return self.__div__(mag)
    return None

  def magnitude(self):
    return math.sqrt(self.x**2 + self.y**2)

  def __add__(self, other):
    return Vector2(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Vector2(self.x - other.x, self.y - other.y)

  def __neg__(self):
    return Vector2(-self.x, -self.y)

  def __mul__(self, scalar):
    return Vector2(self.x * scalar, self.y * scalar)

  def __div__(self, scalar):
    if scalar != 0:
      return Vector2(self.x / scalar, self.y / scalar)
    return None
    
  def __eq__(self, other):
    if abs(self.x - other.x) < self.thresh and abs(self.y - other.y) < self.thresh:
      return True
    else:
      return False

