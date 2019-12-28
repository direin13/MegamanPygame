import universal_names
import pygame
from megaman import *
import music_player
import sprite
import camera
import platform_setup
import character_setup
import camera_setup
import display_layer
from timeit import default_timer as timer

#--Game--

pygame.init()
pygame.font.init()
pygame.mixer.init()
display_layer.init() #layer 1 displayed first, then 2, then 3 etc.

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)

songs = music_player.Song_player('1', ['audio/Snake man.mp3', 'audio/Concrete man.mp3', 'audio/Hornet man.mp3',
                          'audio/Cut man.mp3', 'audio/Heat man.mp3', 'audio/Metal man.mp3',
                          'audio/Quick man.mp3'], volume=0.4)

screen = pygame.display.set_mode((universal_names.screen_width, universal_names.screen_height))

game = True

while game:
   screen.fill((104, 236, 255))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         game = False

   for sprite_surf in sprite.Sprite_surface.all_sprite_surfaces: #Updating every sprite in the game
      sprite_surf.update()
      display_layer.push_onto_layer(sprite_surf)

      if sprite_surf == character_setup.player_1:
         megaman = sprite_surf
         universal_names.camera.sprite_surf = megaman
#         print('HP: {}'.format(megaman.health_points))

   if megaman.y > universal_names.screen_height + 550:
      megaman.kill()
      megaman.health_bar.points -= megaman.health_bar.points

   camera.update(universal_names.camera) #adjusts all sprite surf according to the comera's position

   display_layer.display_all_sprite_surf(screen, universal_names.screen_width, universal_names.screen_height)

   if megaman.is_alive():
      songs.play_list(50, fade_time=3)
   else:
      songs.stop()
   pygame.display.update()
   clock.tick(75)

