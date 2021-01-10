import pygame
from pygame.locals import *

from constants import *
from utils import *

from song_holder import *
from song_selector import *

song_names =  [
  'Gimme Shelter',
  'Sympathy For Devil',
  'Bohemian Rhapsody',
  'Respect',
  'Feeling Good',
  'Unchained Melody',
  'Wish You Were Here',
  'Another Break In The Wall',
  'You Cant Always Get What You Want',
  'California Dreaming',
  'No Woman No Cry',
  'Voodoo Child',
  'voodoo People'
]

def song_names_filter(filter):
  return [song_name for song_name in song_names if song_name.casefold().startswith(filter.casefold())]

def song_entries_filter(filter):
  return [SongEntry(song_name) for song_name in song_names_filter(filter)]



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  song_holder = SongHolder([SongEntry(song_name) for song_name in song_names], background_color=WHITE)
  song_holder.scroll_area_size = 4
  song_holder.position = screen.get_rect().midtop
  song_holder.pivot = (0.5, 0)
  song_holder.move(0, 120)

  song_selector = SongSelector()
  song_selector.position = screen.get_rect().midtop
  song_selector.pivot = (0.5, 0)
  song_selector.on_toggle += [lambda switch: song_holder.set_song_entries(song_entries_filter(switch.text if switch.is_on else ''))]

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
