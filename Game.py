import os
import pygame
import sys
sys.path.insert(1, "source_code")

import universal_var
import game_setup
from debug_mode import Debug
import sprite
import enemy
import camera
import display_layer
import timer
import bar
from bit_text import Bit_text
from misc_function import play_sound
from title_screen import Title_screen
import boss_room 

#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300,50)

pygame.init()
display_layer.init()

game_timers = timer.Timer()
game_timers.add_ID('ready', 14)
game_timers.add_ID('reset', 350)
game_timers.add_ID('jump_to_start', 190)
game_timers.add_ID('game_over', 290)

ready_text = Bit_text('ready', 240, 250, 3, 3, pattern_interval=14)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 600), pygame.FULLSCREEN, pygame.NOFRAME)
sprite.Sprite_surface.display_screen = screen

pygame.mouse.set_visible(False)

Title_screen.screen = screen

checkpoint_1 = [(3594,1200), (340,367)]

checkpoint_2 = [(4200,3600), (250,359)]

megaman = None

intro_has_ended = False
game_has_started = False
game = True

def load_level(level):
   global game_has_started
   global game_timers
   global megaman
   game_setup.clear_all_lists()

   game_has_started = False
   level_objs = game_setup.level_dict[level]
   game_setup.load_megaman_objects(level_objs[0], level_objs[1], level_objs[2], level_objs[3], spawn_megaman=True, m_x=250, m_y=410)
   for sprite_surf in sprite.Sprite_surface.all_sprite_surfaces: 
      if sprite_surf.ID == 'megaman':
         megaman = sprite_surf
         camera.World_camera.target_focus = megaman
   game_timers.replenish_timer('ready')
   game_timers.replenish_timer('jump_to_start')
   game_timers.replenish_timer('reset')
   game_timers.replenish_timer('game_over')
   universal_var.checkpoint = [0, 0]
   camera.World_camera.world_location = [0, 0]
   Debug.debug_init()
   boss_room.Boss_room.battle_has_end = False
   sprite.Sprite_surface.all_sprite_surfaces.sort(key=lambda x: x.display_layer)


def jump_to_start(sprite_surf):
   global game_timers
   global screen
   global ready_text

   if game_timers.is_full('jump_to_start'): #reset everything back to the previous checkpoint
      universal_var.songs.play_list(song_number=0, loop=True, restart_pos=9.0)
      screen.fill((0,0,0))
      universal_var.game_reset = True
      xdist = camera.World_camera.world_location[0] - universal_var.checkpoint[0] #distance to checkpoint and current location
      ydist = camera.World_camera.world_location[1] - universal_var.checkpoint[1]
      for s in sprite.Sprite_surface.all_sprite_surfaces: #move everything back
         if not(isinstance(s, bar.Energy_bar)) and s != sprite_surf:
            s.x += xdist
            s.y += ydist
            s.spawn_point[0] += xdist
            s.spawn_point[1] += ydist
            
      camera.World_camera.world_location[0] -= xdist
      camera.World_camera.world_location[1] -= ydist
      
      for t_box in camera.Transition_box.all_transition_box:
         t_box.direction = t_box.original_direction


   elif game_timers.is_finished('jump_to_start') != True: #display ready text
      ready_text.display(screen, pattern='flash', pattern_interval=14)

   elif not sprite_surf.is_alive() or not sprite_surf.is_active:
      sprite_surf.respawn() #wait for sprite_surf to respawn
      if sprite_surf.is_alive() and universal_var.game_reset == True and sprite_surf.is_active:
         universal_var.game_reset = False
         for e in enemy.Enemy.all_sprite_surfaces:
            e.respawn()
         game_timers.replenish_timer('ready')
         game_timers.replenish_timer('jump_to_start')
         game_timers.replenish_timer('reset')
         return

   game_timers.countdown('jump_to_start')


def check_game_pause():
   k = pygame.key.get_pressed()
   if k[pygame.K_p] and game_has_started == True and megaman.is_alive() and not(camera.camera_transitioning()): #pause game
      if universal_var.game_pause == False:
         play_sound('pause', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume + 0.1)
         universal_var.songs.toggle()
      universal_var.game_pause = True

   elif k[pygame.K_o] and megaman.is_alive() and not(camera.camera_transitioning()): #unpause
      if universal_var.game_pause == True:
         play_sound('pause', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume + 0.1)
         universal_var.songs.toggle()
      universal_var.game_pause = False

   if k[pygame.K_v] and k[pygame.K_b]: #debug
      universal_var.debug = True
   elif k[pygame.K_c]:
      universal_var.debug = False


arrow = Bit_text('>', 160, 240, 3, 3)
play_again_text = Bit_text('play again', 200, 240, 3, 3)
exit_text = Bit_text('exit', 200, 290, 3, 3)
option = 'play_again'

def game_over():
   global game
   global screen
   global option
   global play_again_text
   global exit_text
   global megaman
   global game_has_started
   
   screen.fill((0,0,0))
   if game_timers.is_finished('game_over') != True:
      universal_var.songs.play_list(song_number=1)
      Bit_text.display_text(screen, (180, 140), 'game over', 3, 3)
      game_timers.countdown('game_over')
      game_setup.clear_all_lists()
   else:
      universal_var.songs.play_list(song_number=2)
      play_again_text.display(screen)
      exit_text.display(screen)
      arrow.display(screen, pattern='flash', pattern_interval=20)
      k = pygame.key.get_pressed()

      if k[pygame.K_UP]:
         if option != 'play_again':
            play_sound('pause', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume)
         option = 'play_again'
         arrow.x, arrow.y = play_again_text.x - 40, play_again_text.y

      elif k[pygame.K_DOWN]:
         if option != 'exit':
            play_sound('pause', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume)
         option = 'exit'
         arrow.x, arrow.y = exit_text.x - 40, exit_text.y

      elif k[pygame.K_x]:
         universal_var.songs.stop()
         play_sound('pause', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume)
         if option == 'exit':
            game = False
         else:
            load_level('concrete_man')

def check_checkpoint():
   global megaman
   global checkpoint_1
   global checkpoint_2
   if camera.World_camera.world_location[1] == 1200: #checkpoint 1
      new_checkpoint_x, new_checkpoint_y = checkpoint_1[0][0], checkpoint_1[0][1]
      new_megaman_x, new_megaman_y = checkpoint_1[1][0], checkpoint_1[1][1]
      universal_var.checkpoint = [new_checkpoint_x, new_checkpoint_y]
      megaman.spawn_point = [new_megaman_x, new_megaman_y]

   elif camera.World_camera.world_location[0] >= 4200: #checkpoint 2
      new_checkpoint_x, new_checkpoint_y = checkpoint_2[0][0], checkpoint_2[0][1]
      new_megaman_x, new_megaman_y = checkpoint_2[1][0], checkpoint_2[1][1]
      universal_var.checkpoint = [new_checkpoint_x, new_checkpoint_y]
      megaman.spawn_point = [new_megaman_x, new_megaman_y]

def check_megaman_alive():
   global megaman
   global screen
   global game_has_started
   global game_timers

   if megaman.lives < 0:
      game_over()
   else:
      if universal_var.debug == True:
         megaman.is_active = True
         Debug.debug_mode(screen)
      else:
         camera.World_camera.target_focus = megaman
         if megaman.is_alive() and game_has_started == True:
            pass

         elif game_has_started == True: #When megaman dies
            if universal_var.game_reset != True:
               universal_var.songs.stop()

            reset_time = game_timers.get_ID('reset')['curr_state']

            if game_timers.is_finished('reset'):
               jump_to_start(megaman)

            elif reset_time == 100:
               megaman.lives -= 1

            elif reset_time < 100: #when the screen turns black
               screen.fill((0,0,0))
               universal_var.game_reset = True
               for e in enemy.Enemy.all_sprite_surfaces:
                  e.is_active = False
            game_timers.countdown('reset')

         else:
            jump_to_start(megaman)
            if megaman.is_active:
               game_has_started = True

#--------------------------------------------------------------------------------GAME-----------------------------------------------------------------------------

while game:
   k = pygame.key.get_pressed()
   screen.fill((0,0,0))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         game = False

   for sprite_surf in sprite.Sprite_surface.all_sprite_surfaces:
      sprite_surf.update()

   camera.World_camera.update() #adjusts all sprite surf according to the camera's position 
                                #and displays sprite_surf


   if Title_screen.is_running:
      Title_screen.run()
   elif game_setup.game_timers.is_finished('time_till_game_start') != True:
      game_setup.boss_intro_sequence('concrete_man')
      if game_setup.game_timers.is_almost_finished('time_till_game_start', 20):
         screen.fill((0,0,0))
   else:
      if intro_has_ended == False:
         intro_has_ended = True
         load_level('concrete_man')

      elif boss_room.Boss_room.battle_has_end != True:
         check_megaman_alive()
         check_checkpoint()
         check_game_pause()

      else:
         game_over()
   pygame.display.update()
   clock.tick(75)

universal_var.songs.stop()