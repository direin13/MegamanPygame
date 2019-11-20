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

def display_all_surf(display_stack, surf, screen_width, screen_height):
   #displays every surf that is on the screen

   for sprite_surf in display_stack:
      try:
         if sprite_surf.is_on_screen(screen_width, screen_height) == True and sprite_surf.is_active == True:
            sprite_surf.display(surf)
      except AttributeError:
         #sprite_surf.display_collboxes(surf)
         pass
      #sprite_surf.display_collboxes(surf)


def update_display_stack(display_order):
   #push everythinh from display order onto display stack
   global display_stack
   for lst in display_order: #--putting sprite surfaces in order for displaying
      display_stack.push_update(lst)
      lst.clear()


def get_characters(sprite_surf):
   global character_stack
   if isinstance(sprite_surf, character.Character) == True:
      if sprite_surf.y > universal_names.screen_height:
         sprite_surf.health_points -= sprite_surf.health_points
         sprite_surf.teleport(sprite_surf.x, 0)
      if isinstance(sprite_surf, Megaman):
         print('ID: {}, HP: {}'.format(sprite_surf.ID, sprite_surf.health_points))
      #--I want to display characters last so i put him at the beginning of queue
      character_stack.push(sprite_surf)

   elif sprite_surf.sprites == None:
      character_stack.push(sprite_surf)


def get_background(sprite_surf):
   global background_stack
   if isinstance(sprite_surf, megaman_object.Platform):
      background_stack.push(sprite_surf)


def get_weapons(sprite_surf):
   global weapon_stack
   if isinstance(sprite_surf, p_shooter.P_shooter):
      weapon_stack.push(sprite_surf)
#-----------------------------------------------------------

#--Game--

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,50)

pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)

background_stack, weapon_stack, character_stack = mega_stack.Stack(), mega_stack.Stack(), mega_stack.Stack()

display_order = [background_stack, weapon_stack, character_stack] #background is displayed first, then weapon, then character

display_stack = mega_stack.Stack()

songs = Song_player('1', ['audio/Cut man.mp3', 'audio/Heat man.mp3', 'audio/Metal man.mp3', 'audio/Quick man.mp3', 'audio/Air man.mp3'], volume=0.6)

screen = pygame.display.set_mode((universal_names.screen_width, universal_names.screen_height))

game = True

while game:
   screen.fill((50, 255, 255))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         game = False

   #--checking every sprite_surface in the game
   for sprite_surf in Sprite_surface.all_sprite_surfaces.values():
      get_background(sprite_surf)
      get_weapons(sprite_surf)
      get_characters(sprite_surf)
      sprite_surf.update()

   update_display_stack(display_order)
   display_all_surf(display_stack, screen, universal_names.screen_width, universal_names.screen_height)

   songs.play_list(40, fade_time=3)
   pygame.display.update()
   clock.tick(100)
