import pygame
from pygame.locals import *

from constants import *
from utils import *
from midi import * 

from fruityloops import *



if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()
  #================#
  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  beats = Midi('Breath.mid').beats()
  piano = Piano(mido.open_output(None), Piano.generate_pianokeys_from_beats(beats))
  #================#
  levels = []
  levels.append(Fruityloops(null_beats(beats, [5, 11, -1]), piano))
  levels.append(Fruityloops(null_beats(beats, [3, 8, -1]), piano))
  levels.append(Fruityloops(null_beats(beats, [4, 13, -1]), piano))
 #================#
  for level in levels:
    level.primary_color = CHARLESTON
    level.secondary_color = EBONY
    level.tertiary_color = JET
  #================#
  current_level_index = 0
  #================================================================================================#
  while not done():
    clock.tick(60)
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    levels[current_level_index].process(events)
    #================#
    if levels[current_level_index].state == 'COMPLETE' and levels[current_level_index].beats_roll.playing_progress > 80:
      current_level_index += 1
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(levels[current_level_index].draw(), levels[current_level_index].world_space_rect)
    pygame.display.update()
