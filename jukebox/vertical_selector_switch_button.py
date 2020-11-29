class VerticalSelectorSwitchButton(HorizontalSelectorSwitchButton):
  def __init__(self, text):
    super().__init__(text)
    self._rendered_text = pygame.transform.rotate(self._rendered_text, -90)

  def render(self, surface):
    self._draw_background(surface)
    self._draw_text(surface)

  def _draw_text(self, surface):
    surface.blit(self._rendered_text, self.position)
