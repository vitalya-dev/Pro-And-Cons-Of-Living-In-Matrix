import pygame
from pygame.locals import *

from constants import *
from utils import *

from song_selector import *
from song_holder import *
from scroll import *


if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#

  #================#
  song_selector = SongSelector()
  song_selector.position = screen.get_rect().center
  song_selector.move(0, -150)
  song_selector.pivot = (0.5, 0.5)

  for i in 'ABCDEF':
    song_selector.add_selector(HorizontalButton(i))
  song_selector.add_selector(VerticalButton('SELECT'))
  for i in '123456':
    song_selector.add_selector(HorizontalButton(i)) 
  #================#

  #================#
  song_holder_scroller = Scroll(SongHolder())
  song_holder_scroller.limit = tuple_math(SCREEN_SIZE, '/', (1, 2))
  song_holder_scroller.position = screen.get_rect().center
  song_holder_scroller.move(0, 50)
  song_holder_scroller.pivot = (0.5, 0.5)

  song_holder_scroller.child.add_song_entry(SongEntry('You Cant Always Get What You Want', 'A1'))
  song_holder_scroller.child.add_song_entry(SongEntry('Sympathy For Devil', 'A2'))
  song_holder_scroller.child.add_song_entry(SongEntry('Another Break In The Wall', 'A3'))
  song_holder_scroller.child.add_song_entry(SongEntry('California Dreaming', 'B1'))
  song_holder_scroller.child.add_song_entry(SongEntry('No Woman No Cry', 'B2'))
  song_holder_scroller.child.add_song_entry(SongEntry('Voodoo Child', 'B3'))
  #================#


  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    song_selector.process(events)
    song_holder_scroller.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(song_selector.draw(), song_selector.world_space_rect.topleft)
    screen.blit(song_holder_scroller.draw(), song_holder_scroller.world_space_rect.topleft)
    pygame.display.update()

