import universal_names
import pygame
from megaman import *
import music_player
import sprite
import camera
import platform_setup
import character_setup
import enemy
import megaman_death_orb
import camera_setup
import display_layer
import timer
import bar
import bit_text

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,50)

pygame.init()
pygame.font.init()
pygame.mixer.init()
display_layer.init() #layer 1 displayed first, then 2, then 3 etc.


game_timers = timer.Timer()
game_timers.add_ID('ready', 20)
game_timers.add_ID('reset', 350)
game_timers.add_ID('jump_to_start', 180)

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)

songs = music_player.Song_player('1', ['audio/Snake man.mp3'], volume=0.4)

screen = pygame.display.set_mode((universal_names.screen_width, universal_names.screen_height))



def jump_to_start(sprite_surf, text=''):
   global game_timers
   global screen
   global songs

   if game_timers.is_full('jump_to_start'): #reset everything back to the previous checkpoint
      songs.play_list(130, fade_time=3)
      screen.fill((0,0,0))
      universal_names.game_reset = True
      xdist = universal_names.world_location[0] - universal_names.checkpoint[0] #distance from checkpoint and current location
      ydist = universal_names.world_location[1] - universal_names.checkpoint[1]
      for s in Sprite_surface.all_sprite_surfaces: #move everything back
         if not(isinstance(s, bar.Bar)) and s != sprite_surf:
            s.x += xdist
            s.y += ydist
            s.spawn_point[0] += xdist
            s.spawn_point[1] += ydist
      universal_names.world_location[0] -= xdist
      universal_names.world_location[1] -= ydist
      sprite_surf.respawn_obj.y = sprite_surf.spawn_point[1] - universal_names.screen_height + 100 # set sprite_surf's falling spawn animation above screen
      for t_box in camera.Transition_box.all_transition_box:
         t_box.direction = t_box.original_direction


   elif game_timers.is_empty('jump_to_start') != True: #display ready text
      if game_timers.is_empty('ready'):
         game_timers.replenish_timer('ready')
      elif game_timers.check_ID('ready') > game_timers.all_timers['ready'] // 2:
         bit_text.display_text(screen, (240, 140), text, 3, 3)
      game_timers.countdown('ready')

   elif not sprite_surf.is_alive() or not sprite_surf.is_active:
      sprite_surf.respawn() #wait for sprite_surf to respawn
      if sprite_surf.is_alive() and universal_names.game_reset == True and sprite_surf.is_active:
         universal_names.game_reset = False
         for e in enemy.Enemy.all_sprite_surfaces:
            e.respawn()
         game_timers.replenish_timer('reset')
         game_timers.replenish_timer('ready')
         game_timers.replenish_timer('jump_to_start')
         return

   game_timers.countdown('jump_to_start')


#--------------------------------------------------------------------------------GAME-----------------------------------------------------------

display_collbox = False

start = False

game = True

while game:
   screen.fill((0,0,0))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         game = False

   k = pygame.key.get_pressed()
   if k[pygame.K_p]: #pause game
      universal_names.game_pause = True
   elif k[pygame.K_o]:
      universal_names.game_pause = False

   if k[pygame.K_d]: #displays all collision boxes for helping with debug
      display_collbox = True
   elif k[pygame.K_s]:
      display_collbox = False

   for sprite_surf in sprite.Sprite_surface.all_sprite_surfaces: #Updating every sprite in the game
      if sprite_surf == character_setup.player_1:
         megaman = sprite_surf
         universal_names.camera.sprite_surf = megaman

      sprite_surf.update()
      display_layer.push_onto_layer(sprite_surf)


   if megaman.y > universal_names.screen_height + 550:
      megaman.kill()
      megaman.health_bar.points -= megaman.health_bar.points

   camera.update(universal_names.camera) #adjusts all sprite surf according to the comera's position

   display_layer.display_all_sprite_surf(screen, universal_names.screen_width, universal_names.screen_height, display_collboxes=display_collbox)


   if megaman.is_alive() and start == True:
      songs.play_list(130, fade_time=3)

   elif start == True: #When megaman dies
      if universal_names.game_reset == False:
         songs.stop()

      reset_time = game_timers.check_ID('reset')

      if game_timers.is_empty('reset'):
         megaman_death_orb.reset()
         jump_to_start(megaman, 'ready')

      elif reset_time < 100: #when the screen turns black
         screen.fill((0,0,0))
         megaman_death_orb.reset()
         for c in enemy.Enemy.all_sprite_surfaces:
            c.is_active = False
      game_timers.countdown('reset')

   else:
      jump_to_start(megaman, 'ready')
      if megaman.is_active:
         start = True


   pygame.display.update()
   clock.tick(75)
