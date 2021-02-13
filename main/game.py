import pygame
from pygame.locals import *

from constants import *
from utils import *
from midi import * 

from fruityloops import *
from transition import *

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
  for level in levels:
    level.primary_color = CHARLESTON
    level.secondary_color = EBONY
    level.tertiary_color = JET
  current_level_index = 0
  next_level_index = current_level_index
  #================#
  transition = Transition()
  transition.fadein_speed = 100
  transition.fadeout_speed = 200
  transition.primary_color=WHITE
  #================================================================================================#
  main_loop_state = 'GAMEPLAY'
  #================#
  while not done():
    clock.tick(60)
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    #================#
    if main_loop_state == 'GAMEPLAY':
      levels[current_level_index].process(events)
      if levels[current_level_index].state == 'COMPLETE':
        main_loop_state = 'TRANSITION'
        next_level_index = current_level_index + 1
        transition.start()
      elif levels[current_level_index].state == 'FAIL':
        main_loop_state = 'TRANSITION'
        next_level_index = current_level_index
        transition.start()
    elif main_loop_state == 'TRANSITION':
      transition.process(events)
      if transition.state == 'COMPLETE':
        main_loop_state = 'GAMEPLAY'
        current_level_index = next_level_index
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    if main_loop_state == 'GAMEPLAY':
      screen.blit(levels[current_level_index].draw(), levels[current_level_index].world_space_rect)
    elif main_loop_state == 'TRANSITION':
      if transition.state == 'FADE IN':
        screen.blit(levels[current_level_index].draw(), levels[current_level_index].world_space_rect)
      if transition.state == 'FADE OUT':
        screen.blit(levels[next_level_index].draw(), levels[next_level_index].world_space_rect)
      screen.blit(transition.draw(), transition.world_space_rect)
    pygame.display.update()
