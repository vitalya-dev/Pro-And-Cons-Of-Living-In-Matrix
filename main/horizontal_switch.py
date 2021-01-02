from horizontal_button import *


class HorizontalSwitch(HorizontalButton):
  pass


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


