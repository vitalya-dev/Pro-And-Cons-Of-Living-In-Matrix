from horizontal_button import *


class HorizontalSwitch(HorizontalButton):
  def __init__(self, text, background_color=BLACK, text_color=GRAY, parent=None):
    super().__init__(text, background_color, text_color, parent)

  def process(self, events):
    pass

  def toggle(self):
    self._clicked = not self._clicked

  @property
  def is_on(self):
    return self._clicked



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  a_switch = HorizontalSwitch('A')
  a_switch.pivot = (0, 0)
  a_switch.position = screen.get_rect().center

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    a_switch.process(events)
    #===========================================RENDER==================================================#
    screen.fill((0, 0, 0))
    screen.blit(a_switch.draw(), a_switch.world_space_rect.topleft)

    pygame.display.update()


