from horizontal_selector_switch_button import *

class VerticalSelectorSwitchButton(HorizontalSelectorSwitchButton):
  def __init__(self, text):
    super().__init__(text)
    self.margin = (2, 0)
    self.rotate(-90)

  def draw(self):
    self._draw_background()
    self._draw_text()
    return self._surface
    



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  select_btn = VerticalSelectorSwitchButton('SELECT')
  select_btn.pivot = (0.5, 0.5)
  select_btn.position = screen.get_rect().center

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    select_btn.process(events)
    #===========================================RENDER==================================================#
    screen.fill(pygame.Color('#000000'))
    screen.blit(select_btn.draw(), select_btn.world_space_rect.topleft)
    pygame.display.update()
    
