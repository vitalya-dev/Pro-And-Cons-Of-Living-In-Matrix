from horizontal_selector_switch_button import *

class VerticalSelectorSwitchButton(HorizontalSelectorSwitchButton):
  def __init__(self, text):
    super().__init__(text)
    self._rendered_text = pygame.transform.rotate(self._rendered_text, -90)
    self._text_offset = (0, 0)

  def render(self, surface):
    self._draw_background(surface)
    self._draw_text(surface)



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
    select_btn.render(screen)
    pygame.display.update()
    
