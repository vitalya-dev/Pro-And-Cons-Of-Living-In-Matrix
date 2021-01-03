from horizontal_switch  import *


class VerticalSwitch(HorizontalSwitch):
  def __init__(self, text, background_color=BLACK, text_color=GRAY, parent=None):
    super().__init__(text, background_color, text_color, parent)
    self.padding = (2, 0)
    self.rotate(-90)

  def draw(self):
    self._draw_background()
    self._draw_text()
    if self._clicked:
      self._draw_highlight()
    return self._surface
  

if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  select_switch = VerticalSwitch('SELECT')
  select_switch.pivot = (0.5, 0.5)
  select_switch.position = screen.get_rect().center

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    select_switch.process(events)
    #===========================================RENDER==================================================#
    screen.fill((0, 0, 0))
    screen.blit(select_switch.draw(), select_switch.world_space_rect.topleft)

    pygame.display.update()

