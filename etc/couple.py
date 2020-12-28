import math

class Couple(object):
  def __init__(self, a=0.0, b=0.0):
    self.a = float(a)
    self.b = float(b)
    self.thresh = 0.0001

  def copy(self):
    return Couple(self.a, self.b)

  def as_tuple(self):
    return (self.a, self.b)

  def __add__(self, other):
    if hasattr(other, "__getitem__"):
      a, b = other
      return Couple(self.a + a, self.b + b)
    else:
      return Couple(self.a + other, self.b + other)

  def __iadd__(self, other):
    if hasattr(other, "__getitem__"):
      a, b = other
      self.a += a
      self.b += b
    else:
      self.a += other
      self.b += other
    return self

  def __radd__(self, other):
    return self + other


  def __sub__(self, other):
    if hasattr(other, "__getitem__"):
      a, b = other
      return Couple(self.a - a, self.b - b)
    else:
      return Couple(self.a - other, self.b - other)

  def __rsub__(self, other):
    if hasattr(other, "__getitem__"):
      a, b = other
      return Couple(a - self.a, b - self.b)
    else:
      return Couple(other - self.a, other - self.b)


  def __neg__(self):
    return self * -1

  def __mul__(self, other):
    if hasattr(other, "__getitem__"):
      a, b = other
      return Couple(self.a * float(a), self.b * float(b))
    else:
      return Couple(self.a * float(other), self.b * float(other))

  def __rmul__(self, other):
    return self * other


  def __truediv__(self, other):
    if hasattr(other, "__getitem__"):
      a, b = other
      return Couple(self.a / a, self.b / b)
    else:
      return Couple(self.a / other, self.b / other)

  def __rtruediv__(self, other):
    if hasattr(other, "__getitem__"):
      a, b = other
      return Couple(a / self.a, b / self.b)
    else:
      return Couple(other / self.a, other / self.b)

  def __eq__(self, other):
    a, b = other
    return abs(self.a - a) < self.thresh and abs(self.b - b) < self.thresh

  def __getitem__(self, index):
    return self.a if index == 0 else self.b

  def __str__(self):
    return '(%f, %f)' % (self.a, self.b)

  def __iter__(self):
    return iter([self.a, self.b])


if __name__ == '__main__':
  assert -Couple(1, 2) == (-1, -2)

  assert Couple(1, 2) == Couple(1, 2)

  assert Couple(1, 2) + 3 == (4, 5)
  assert Couple(1, 2) + (3, 4) == (4, 6)
  assert 3 + Couple(1, 2) == (4, 5)
  assert (3, 4) + Couple(1, 2) == (4, 6)

  assert Couple(1, 2) - 3 == (-2, -1)
  assert Couple(1, 2) - (3, 4) == (-2, -2)
  assert 3 - Couple(1, 2) == (2, 1)
  assert (3, 4) - Couple(1, 2) == (2, 2)

  assert Couple(1, 2) * 3 == (3, 6)
  assert Couple(1, 2) * (3, 4) == (3, 8)
  assert 3 * Couple(1, 2) == (3, 6)
  assert (3, 4) * Couple(1, 2) == (3, 8)

  assert Couple(1, 2) / 3 == (1/3, 2/3)
  assert Couple(1, 2) / (3, 4) == (1/3, 2/4)
  assert 3 / Couple(1, 2) == (3, 3/2)
  assert (3, 4) / Couple(1, 2) == (3, 2)
  
  a = Couple(1, 2)
  a += 3
  assert a == Couple(4, 5)

  a = Couple(1, 2)
  a += a
  assert a == (2, 4)

  print('All Test Ist Pass')
