import pygame
from music_player import *
from sprite import *
from platform_setup import *
from megaman import *
import character_setup
from mega_queue import *
from camera_setup import *

def is_on_screen(sprite_surf, screen_width, screen_height):
   #checks if sprite_surf is on
   if (sprite_surf.x < screen_width -10 and sprite_surf.x + sprite_surf.sprite.width > 10) and (sprite_surf.y < screen_height -10 and sprite_surf.y + sprite_surf.sprite.width > 10):
      return True
   else:
      return False

def update_all_surf(update_queue, surf, screen_width, screen_height):
   while len(update_queue.lst) > 0:
      try:
         sprite_surf = update_queue.dequeue()
         if is_on_screen(sprite_surf, screen_width, screen_height) == True:
            sprite_surf.display(screen)
      except AttributeError:
         sprite_surf.display_collboxes(surf)
         pass

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,50)

pygame.init()
pygame.font.init()
pygame.mixer.init()

clock = pygame.time.Clock()

font_1 = pygame.font.SysFont(None, 20)

update_queue = Queue()

songs = Song_player('1', ['audio/Metal man.mp3', 'audio/Quick man.mp3', 'audio/Heat man.mp3', 'audio/Cut man.mp3', 'audio/Air man.mp3'], volume=0.6)

width, height = 600, 600

screen = pygame.display.set_mode((width, height))

game_on = True


while game_on:
   pygame.display.update()
   screen.fill((100, 255, 255))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         game_on = False

   for sprite_surf in Sprite_surface.all_sprite_surfaces.values():

      if isinstance(sprite_surf, Main_character) == True:
         if sprite_surf.y > width:
            sprite_surf.move(250, 0)

         sprite_surf.update_character()
         update_queue.enqueue(sprite_surf)

      else:
         if sprite_surf.sprite != None:
            update_queue.enqueue_start(sprite_surf)
         else:
            update_queue.enqueue(sprite_surf)

      Sprite_surface.update(sprite_surf)
   update_all_surf(update_queue, screen, width, height)

   clock.tick(100)
   songs.play_list(40, fade_time=3)
