class SelectorSwitch(object):
  def __init__(self):
    self.position = (0, 0)
    self.pivot = (0, 0)
    self.button_margin = 25
    self._switches = []
    self._surface = pygame.surface.Surface((0, 0)).convert()

  def add_horizontal_switch_button(self, button_name):
    button = HorizontalSelectorSwitchButton(button_name)
    button.position = self._calculate_position_for_new_button()
    self._switches.append(button)
    #================#
    self._resize_surface()


  def add_vertical_switch_button(self, button_name):
    button = VerticalSelectorSwitchButton(button_name)
    button.position = self._calculate_position_for_new_button()
    self._switches.append(button)
    #================#
    self._resize_surface()

  def _resize_surface(self):
    self._surface = pygame.surface.Surface((self._buttons_total_width(), self._buttons_max_height())).convert()
    self._surface.set_colorkey((0, 0, 0))

  def _calculate_position_for_new_button(self):
    if len(self._switches) == 0:
      return (0, 0)
    else:
      new_button_position = tuple_math(self._switches[-1].position, '+', (self._switches[-1].width, 0))
      new_button_position = tuple_math(new_button_position, '+', (self.button_margin, 0))
      return new_button_position

  def _buttons_total_width(self):
    if len(self._switches) > 0:
      buttons_total_width = sum([button.width for button in self._switches])
      buttons_total_width_with_margin = buttons_total_width + self.button_margin * (len(self._switches) - 1)
      return buttons_total_width_with_margin
    else:
      return 0

  def _buttons_max_height(self):
    if len(self._switches) > 0:
      return max([button.height for button in self._switches])
    else:
      return 0

  def _top_left_position(self):
    pivot_position = tuple_math(self.pivot, '*', self._surface.get_size())
    pivot_position_as_int = tuple(map(int, pivot_position))
    return tuple_math(self.position, '-', pivot_position_as_int)

  def render(self, surface):
    self._surface.fill((0, 0, 0))
    for button in self._switches:
      button.render(self._surface)
    surface.blit(self._surface, self._top_left_position())

  def process(self, events):
    for button in self._switches:
      button.process(events)







