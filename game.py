import universal_var
import pygame
import game_setup
from megaman import *
import music_player
import debug_mode
import sprite
import camera
import character_setup
import enemy
import megaman_death_orb
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
game_timers.add_ID('jump_to_start', 190)

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)

songs = music_player.Song_player('1', ['audio/Snake man.mp3'], volume=0.6)

screen = pygame.display.set_mode((universal_var.screen_width, universal_var.screen_height))

checkpoint_1 = [(3594,1200), (340,367)]

checkpoint_2 = [(4200,3600), (250,359)]


def jump_to_start(sprite_surf):
   global game_timers
   global screen
   global songs

   if game_timers.is_full('jump_to_start'): #reset everything back to the previous checkpoint
      songs.play_list(130, fade_time=3)
      screen.fill((0,0,0))
      universal_var.game_reset = True
      xdist = universal_var.world_location[0] - universal_var.checkpoint[0] #distance to checkpoint and current location
      ydist = universal_var.world_location[1] - universal_var.checkpoint[1]
      for s in Sprite_surface.all_sprite_surfaces: #move everything back
         if not(isinstance(s, bar.Bar)) and s != sprite_surf:
            s.x += xdist
            s.y += ydist
            s.spawn_point[0] += xdist
            s.spawn_point[1] += ydist
            
      universal_var.world_location[0] -= xdist
      universal_var.world_location[1] -= ydist
      sprite_surf.respawn_obj.y = sprite_surf.spawn_point[1] - universal_var.screen_height + 100 # set sprite_surf's falling spawn animation above screen
      
      for t_box in camera.Transition_box.all_transition_box:
         t_box.direction = t_box.original_direction


   elif game_timers.is_empty('jump_to_start') != True: #display ready text
      if game_timers.is_empty('ready'):
         game_timers.replenish_timer('ready')
      elif game_timers.check_ID('ready') > game_timers.all_timers['ready'] // 2:
         bit_text.display_text(screen, (240, 140), 'ready', 3, 3)
      game_timers.countdown('ready')

   elif not sprite_surf.is_alive() or not sprite_surf.is_active:
      sprite_surf.respawn() #wait for sprite_surf to respawn
      if sprite_surf.is_alive() and universal_var.game_reset == True and sprite_surf.is_active:
         universal_var.game_reset = False
         for e in enemy.Enemy.all_sprite_surfaces:
            e.respawn()
         game_timers.replenish_timer('reset')
         game_timers.replenish_timer('ready')
         game_timers.replenish_timer('jump_to_start')
         return

   game_timers.countdown('jump_to_start')


#--------------------------------------------------------------------------------GAME-----------------------------------------------------------------------------

for sprite_surf in sprite.Sprite_surface.all_sprite_surfaces: 
      if sprite_surf == character_setup.player_1:
         megaman = sprite_surf
         universal_var.camera.sprite_surf = megaman

start = False

game = True

while game:
   screen.fill((0,0,0))
   for e in pygame.event.get():
      if e.type == pygame.QUIT:
         game = False

   k = pygame.key.get_pressed()
   if k[pygame.K_p] and start == True and megaman.is_alive() and not(camera.camera_transitioning()): #pause game
      if universal_var.game_pause == False:
         play_sound('pause', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume + 0.1)
         songs.toggle()
      universal_var.game_pause = True
      bit_text.display_text(screen, (500, 20), 'ii', 3, 4)

   elif k[pygame.K_o] and megaman.is_alive() and not(camera.camera_transitioning()): #unpause
      if universal_var.game_pause == True:
         play_sound('pause', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume + 0.1)
         songs.toggle()
      universal_var.game_pause = False

   if k[pygame.K_v]: #debug
      universal_var.debug = True
   elif k[pygame.K_c]:
      universal_var.debug = False


   #print(universal_var.world_location)
   for sprite_surf in sprite.Sprite_surface.all_sprite_surfaces: #Updating every sprite in the game

      if sprite_surf.is_on_screen(universal_var.screen_width, universal_var.screen_height):
         display_layer.push_onto_layer(sprite_surf, sprite_surf.display_layer)
      sprite_surf.update()

   camera.update(universal_var.camera) #adjusts all sprite surf according to the comera's position

   display_layer.display_all_sprite_surf(screen, display_collboxes=universal_var.debug)


   if universal_var.debug == True:
      megaman.is_active = True
      debug_mode.debug(screen)
      songs.play_list(130, fade_time=3)
   else:
      universal_var.camera.sprite_surf = megaman
      if megaman.is_alive() and start == True:
         songs.play_list(130, fade_time=3)
         if megaman.y > universal_var.screen_height + 550:
            megaman.health_points -= megaman.health_points #death
            megaman.health_bar.points -= megaman.health_bar.points

      elif start == True: #When megaman dies
         if universal_var.game_reset == False:
            songs.stop()

         reset_time = game_timers.check_ID('reset')

         if game_timers.is_empty('reset'):
            megaman_death_orb.reset()
            jump_to_start(megaman)

         elif reset_time < 100: #when the screen turns black
            screen.fill((0,0,0))
            megaman_death_orb.reset()
            for c in enemy.Enemy.all_sprite_surfaces:
               c.is_active = False
         game_timers.countdown('reset')

      else:
         jump_to_start(megaman)
         if megaman.is_active:
            start = True

   if universal_var.world_location[1] == 1200: #checkpoint 1
      new_checkpoint_x, new_checkpoint_y = checkpoint_1[0][0], checkpoint_1[0][1]
      new_megaman_x, new_megaman_y = checkpoint_1[1][0], checkpoint_1[1][1]
      universal_var.checkpoint = [new_checkpoint_x, new_checkpoint_y]
      megaman.spawn_point = [new_megaman_x, new_megaman_y]

   elif universal_var.world_location[0] >= 4200: #checkpoint 2
      new_checkpoint_x, new_checkpoint_y = checkpoint_2[0][0], checkpoint_2[0][1]
      new_megaman_x, new_megaman_y = checkpoint_2[1][0], checkpoint_2[1][1]
      universal_var.checkpoint = [new_checkpoint_x, new_checkpoint_y]
      megaman.spawn_point = [new_megaman_x, new_megaman_y]


   pygame.display.update()
   clock.tick(75)
