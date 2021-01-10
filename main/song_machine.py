import pygame
from pygame.locals import *

from constants import *
from utils import *

from song_holder import *
from song_selector import *

if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  song_entries =  [
    SongEntry('Gimme Shelter'),
    SongEntry('Sympathy For Devil'),
    SongEntry('Bohemian Rhapsody'),
    SongEntry('Respect'),
    SongEntry('Feeling Good'),
    SongEntry('Unchained Melody'),
    SongEntry('Wish You Were Here'),
    SongEntry('Another Break In The Wall'),
    SongEntry('You Cant Always Get What You Want'),
    SongEntry('California Dreaming'),
    SongEntry('No Woman No Cry'),
    SongEntry('Voodoo Child'),
    SongEntry('Voodoo People')
  ]
  song_holder = SongHolder(song_entries, background_color=WHITE)
  song_holder.scroll_area_size = 4
  song_holder.position = screen.get_rect().midtop
  song_holder.pivot = (0.5, 0)
  song_holder.move(0, 120)

  song_selector = SongSelector()
  song_selector.position = screen.get_rect().midtop
  song_selector.pivot = (0.5, 0)
  song_selector.on_toggle += [lambda switch: print(switch.text)]

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    song_holder.process(events)
    song_selector.process(events)
    #===========================================RENDER==================================================#
    screen.fill(WHITE)
    screen.blit(song_holder.draw(), song_holder.world_space_rect.topleft)
    screen.blit(song_selector.draw(), song_selector.world_space_rect.topleft)
    pygame.display.update()
