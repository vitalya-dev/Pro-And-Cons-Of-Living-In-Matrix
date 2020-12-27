import pygame
from pygame.locals import *

from constants import *
from utils import *

from piano import *
from piano_roll import *
from midi import *
from melody_editor import *
from melody_viewer import *


      
if __name__ == '__main__':
  #===========================================INIT=================================================#
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE)
  clock = pygame.time.Clock()
  #================================================================================================#
  midioutput = mido.open_output(None)
  piano = Piano(midioutput, Piano.generate_pianokeys_from_midi(Midi('Breath.mid')))

  piano_roll = PianoRoll(midioutput)

  melody_viewer = MelodyViewer(Midi('Breath.mid').beats(), 640, 480)

  melody_editor = MelodyEditor(Piano.generate_pianokeys_from_midi(Midi('Breath.mid')), melody_viewer.time_to_pixel_scale, 640, 480)
  melody_editor.set_colorkey(BLACK)
  melody_editor.foreground_color = RED
  melody_editor.text_color = GREEN

  keyboard = Keyboard()
  keyboard.on_space += [lambda: piano_roll.start_or_stop_playing_beats(melody_editor.melody)]

  while not done():
    clock.tick()
    #===========================================PROCESS=================================================#
    events = pygame.event.get()
    melody_viewer.process(events)
    melody_editor.process(events)
    piano.process(events)
    keyboard.process(events)
    #===========================================RENDER==================================================#
    screen.fill(BLACK)
    screen.blit(melody_viewer.draw(), melody_viewer.world_space_rect.topleft)
    screen.blit(melody_editor.draw(), melody_editor.world_space_rect.topleft)
    pygame.display.update()
