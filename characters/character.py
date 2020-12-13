import pygame
from pygame.locals import *

from constants import *
from utils import *

from shape import *

class Character(Shape):
  def __init__(self, head, body, parent=None):
    super().__init__(parent)
    self.head = head
    self.body = body
    self._rebuild_surface()

  def _rebuild_surface(self):
    self._surface = pygame.surface.Surface(self._head_and_body_union_size()).convert()
    self._surface.set_colorkey((0, 0, 0))

  def _head_and_body_union_size(self):
    head_area = self.head.get_rect()
    body_area = self.body.get_rect()
    body_area.midtop = head_area.midbottom
    return head_area.union(body_area).size

  def draw(self):
    self._surface.fill((0, 0, 0))
    self._surface.blit(self.head, self._head_position())
    self._surface.blit(self.body, self._body_position())
    return self._surface

  def _head_position(self):
    return self.head.get_rect(midtop=self._surface.get_rect().midtop)

  def _body_position(self):
    return self.body.get_rect(midbottom=self._surface.get_rect().midbottom)

  def process(self, events):
    pass

  def scale(self, scale_factor):
    self.head = scale_frame(self.head, scale_factor)
    self.body = scale_frame(self.body, scale_factor)
    self._rebuild_surface()


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  #================================================================================================#
  head_1 = load_frame('graphics/Head_1.png')
  head_2 = load_frame('graphics/Head_2.png')
  head_3 = load_frame('graphics/Head_3.png')

  body_1 = load_frame('graphics/Body_1.png')
  body_2 = load_frame('graphics/Body_2.png')
  body_3 = load_frame('graphics/Body_3.png')
  #================================================================================================#

  bob = Character(head_1, body_1)
  bob.scale(7)

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    bob.process(events)
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    screen.blit(bob.draw(), bob.world_space_rect.topleft)
    pygame.display.update()


