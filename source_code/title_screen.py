import pygame
import universal_var
from megaman_object import Megaman_object
from sprite import Sprite
from timer import Timer
from bit_text import Bit_text
from misc_function import play_sound

class Title_screen(object):
   all_timers = Timer()
   all_timers.add_ID('show_text', 160)
   all_timers.add_ID('blackout_screen', 130)
   all_timers.add_ID('move_logo_offscreen', 30)
   begin_game = Bit_text('press x', 50, 330, 3, 3, pattern_interval=60)
   is_running = False
   confirmation = False
   screen = None

   def init():
      for timer in Title_screen.all_timers:
         Title_screen.all_timers.replenish_timer(timer)
         
      title_logo_img = [universal_var.misc_images['title']]
      width, height = 500, 300
      title_logo_sprite = Sprite(universal_var.main_sprite, 0, 0, width, height, [('title', title_logo_img, 1)])
      Title_screen.title_logo = Megaman_object('title_logo', 50, 2000, sprites=[title_logo_sprite], width=width, height=height, is_active=True)

      megaman_face_img = [universal_var.misc_images['megaman_face']]
      width, height = 200, 300
      megaman_face_sprite = Sprite(universal_var.main_sprite, 0, 0, width, height, [('world', megaman_face_img, 1)])
      Title_screen.megaman_face = Megaman_object('megaman_face', -width*13, 230, sprites=[megaman_face_sprite], width=width, height=height, is_active=True)

      Title_screen.is_running = True

   @classmethod
   def run(cls):
      k = pygame.key.get_pressed()
      if cls.all_timers.is_finished('show_text') != True:
         cls.all_timers.countdown('show_text')

      else:
         if k[pygame.K_x] and cls.confirmation == False:
            play_sound('select', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.1)
            cls.confirmation = True

         if cls.confirmation != True:
            cls.begin_game.display(cls.screen, 'flash')
            Bit_text.display_text(cls.screen, (20, 530), '©capcom co.,  ltd', 3, 3)
            Bit_text.display_text(cls.screen, (20, 560), 'a short pygame project', 3, 3)
            universal_var.songs.play_list(song_number=4)

      
      if cls.confirmation != True:
         cls.title_logo.follow(x=50, y=-20, x_vel=20, y_vel=20)
         cls.megaman_face.follow(x=340, y=230, x_vel=20, y_vel=20)

      else:
         if cls.all_timers.is_finished('move_logo_offscreen') != True:
            cls.all_timers.countdown('move_logo_offscreen')
         else:
            cls.title_logo.follow(x=50, y=1000, x_vel=20, y_vel=20)
         cls.megaman_face.follow(x=-200, y=230, x_vel=20, y_vel=20)
         universal_var.songs.stop()
         if cls.all_timers.is_finished('blackout_screen') != True:
            cls.all_timers.countdown('blackout_screen')
         else:
            cls.is_running = False