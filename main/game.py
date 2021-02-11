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
  midi_output = mido.open_output(None)
  #================================================================================================#
  beats = Midi('Breath.mid').beats()
  #================#
  levels = []
  levels.append(
    Fruityloops(
      beats_to_solve=null_beats(beats, [5, 11, -1]),
      answer=pickle.dumps(beats),
      piano=Piano(midi_output, Piano.generate_pianokeys_from_beats(beats))
    )
  )
  levels.append(
    Fruityloops(
      beats_to_solve=null_beats(beats, [3, 8, -1]),
      answer=pickle.dumps(beats),
      piano=Piano(midi_output, Piano.generate_pianokeys_from_beats(beats))
    )
  )
  levels.append(
    Fruityloops(
      beats_to_solve=null_beats(beats, [4, 13, -1]),
      answer=pickle.dumps(beats),
      piano=Piano(midi_output, Piano.generate_pianokeys_from_beats(beats))
    )
  )
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
    if levels[current_level_index].state == 'FAIL' and levels[current_level_index].beats_roll.playing_progress > 80:
      levels[current_level_index].reset()
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(levels[current_level_index].draw(), levels[current_level_index].world_space_rect)
    pygame.display.update()
