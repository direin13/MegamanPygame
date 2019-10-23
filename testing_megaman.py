import pygame
import universal_names
from music_player import *
from sprite import *
from megaman_object import *
from megaman import *
import platform_setup
import character_setup
import mega_queue
import camera_setup

def display_all_surf(display_queue, surf, screen_width, screen_height):
   #displays every surf that is on the screen

   while display_queue.is_empty() != True:
      sprite_surf = display_queue.dequeue()
      try:
         if sprite_surf.is_on_screen(screen_width, screen_height) == True and sprite_surf.is_alive == True:
            sprite_surf.display(screen)
            #sprite_surf.display_collboxes(screen)
      except AttributeError:
         #sprite_surf.display_collboxes(surf)
         pass
#-----------------------------------------------------------

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,50)

pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()

font_1 = pygame.font.SysFont(None, 20)

display_queue = mega_queue.Queue()

songs = Song_player('1', ['audio/Air man.mp3', 'audio/Metal man.mp3', 'audio/Quick man.mp3', 'audio/Heat man.mp3', 'audio/Cut man.mp3'], volume=0.6)

screen = pygame.display.set_mode((universal_names.screen_width, universal_names.screen_height))

game_on = True


while game_on:
   pygame.display.update()
   screen.fill((100, 255, 255))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         game_on = False

   #--checking every sprite_surface in the game
   for sprite_surf in Sprite_surface.all_sprite_surfaces.values():

      if isinstance(sprite_surf, Megaman) == True:
         if sprite_surf.y > universal_names.screen_height:
            sprite_surf.move(sprite_surf.x, 0)

         #--I want to display characters last so i put him at the beginning of queue
         display_queue.enqueue(sprite_surf)

      else:
         if sprite_surf.sprite != None:
            #--for collision boxes
            display_queue.enqueue_start(sprite_surf)
         else:
            display_queue.enqueue(sprite_surf)

      sprite_surf.update()
   display_all_surf(display_queue, screen, universal_names.screen_width, universal_names.screen_height)

   clock.tick(100)
   songs.play_list(40, fade_time=3)
