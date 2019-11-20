import universal_names
import pygame
from music_player import *
from sprite import *
from megaman import *
from enemy import *
import megaman_object
import character
import p_shooter
import platform_setup
import character_setup
import mega_stack
import camera_setup
import display_layer

#--Game--

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,50)

pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)

display_order = display_layer.Display_layer(5) #layer 1 displayed first, then 2, then 3 etc.

display_stack = mega_stack.Stack()

songs = Song_player('1', ['audio/Concrete man.mp3', 'audio/Cut man.mp3', 'audio/Heat man.mp3', 'audio/Metal man.mp3', 'audio/Quick man.mp3', 'audio/Air man.mp3'], volume=0.6)

screen = pygame.display.set_mode((universal_names.screen_width, universal_names.screen_height))

game = True

while game:
   screen.fill((0, 0, 0))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         game = False

   for sprite_surf in Sprite_surface.all_sprite_surfaces.values():
      display_layer.Display_layer.push_onto_layer(sprite_surf)
      sprite_surf.update()
      if isinstance(sprite_surf, character.Character) == True:
         if sprite_surf.y > universal_names.screen_height:
            sprite_surf.health_points -= sprite_surf.health_points

   display_layer.Display_layer.display_all_surf(screen, universal_names.screen_width, universal_names.screen_height)

   if character_setup.player_1.is_alive():
      songs.play_list(40, fade_time=3)
   else:
      songs.stop()
   pygame.display.update()
   clock.tick(100)
