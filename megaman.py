#!/usr/bin/env python
import universal_names
from sprite import *
import pygame
import timer
from misc_function import *
from p_shooter import *
from megaman import *
import megaman_object
from enemy import *
from character import *
from bar import *
import megaman_death_orb
import camera

class Megaman(Character):
   def __init__(self, ID, x, y, sprites, coll_boxes, is_active=False, width=0, height=0, display_layer=3, gravity=False, 
               direction=True, max_x_vel=1, health_points=100, controls=None, jump_speed=1):
      
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer, gravity, direction, max_x_vel, health_points)
      if controls == None:
         self.controls = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_p, pygame.K_w]
      else:
         self.controls = controls #--right, up, left, down, action, jump--

      self.keys_pressed = pygame.key.get_pressed()
      self.jump_speed = jump_speed
      self.acc_speed = 3
      self.decc_speed = 3
      self.can_jump = False
      self.health_points_copy = self.health_points
      self.health_bar = Bar('megaman_health', x=30, y=20, points=self.health_points, colour=(255, 223, 131))

      respawn_sprite = Sprite(universal_names.main_sprite, 0, 0, self.width, self.height, [('drop_down', [universal_names.effect_images['spawn_1']], 15),
                              ('spawn', [universal_names.effect_images['spawn_2'], universal_names.effect_images['spawn_3'], universal_names.effect_images['spawn_1']], 15)])
      self.respawn_obj = megaman_object.Megaman_object('respawn', 0, 0, [respawn_sprite], None, is_active=False, display_layer=3)
      self.all_timers.add_ID('respawn_animation', 15)

      self.all_timers.add_ID('rise_flag', 4)
      self.all_timers.add_ID('shooting_flag', 0)
      self.all_timers.add_ID('can_shoot', 1)
      self.all_timers.add_ID('startup_flag', 0)
      self.all_timers.add_ID('startup_animation', 0)
      self.all_timers.add_ID('death_sound', 1)
      self.all_timers.add_ID('death', 30)
      megaman_death_orb.init(self) #These orbs are shot out when megaman dies
      for i in range(0, 3): #--making p_shooter bullets
         P_shooter('p_shooter', 0, 0)




   def is_pressing(self, n):
      #'n' refers to index in self.controls
      if self.stun is True or self.keys_pressed == None:
         return False
      else:
         return self.keys_pressed[self.controls[n]]

   def is_stunned(self):
      return self.all_timers.is_empty('stun') != True

   def is_standstill(self):
      return (not(self.is_pressing(0) or self.is_pressing(2)) or 
            (self.is_pressing(0) and self.is_pressing(2)))

   def is_shooting(self):
      return self.all_timers.is_empty('shooting_flag') == False
   
   def check_stun(self):
      if universal_names.game_pause != True:
         self.all_timers.countdown('stun') #Knock back until timer is finished

      if self.all_timers.is_empty('stun'):
         self.stun = False
      else:
         self.knock_back(1)
      
   def set_direction(self):
      #--note that direction == False means direction == Left, whereas True == Right

      if self.is_standstill():
         self.direction = self.direction

      elif self.is_pressing(0):
         #--right
         if self.is_grounded != True:
            self.direction = True
         else:
            if self.x_vel == 0:
               self.direction = True

      elif self.is_pressing(2):
         #--left
         if self.is_grounded != True:
            self.direction = False
         else:
            if self.x_vel == 0:
               self.direction = False

   def stop(self):
      #brings player to a halt
      if self.is_grounded == True:
         self.deccelerate(self.decc_speed)
      else:
         self.x_vel = 0

      if self.direction == True:
         self.x += self.x_vel
      else:
         self.x -= self.x_vel

   def move_L(self):
      if self.is_grounded == True:
         if self.direction == False:
            self.accelerate(self.acc_speed, self.max_x_vel)
            self.x -= self.x_vel
         else:
            self.deccelerate(self.decc_speed)
            self.x += self.x_vel

      else:
         self.x_vel = self.max_x_vel
         self.x -= self.x_vel


   def move_r(self):
      if self.is_grounded == True:
         if self.direction == True:
            self.accelerate(self.acc_speed, self.max_x_vel)
            self.x += self.x_vel
         else:
            self.deccelerate(self.decc_speed)
            self.x -= self.x_vel

      else:
         self.x_vel = self.max_x_vel
         self.x += self.x_vel


   def check_hazard_collision(self):
      collision = self.check_collision_lst(Megaman_object.hazards, universal_names.hitbox, universal_names.hitbox, quota=1)
      if collision.is_empty() != True:
         hazard = collision.pop()
         self.damage_megaman(hazard)

   def damage_megaman(self, hazard):
      if hazard.is_alive() == True:
         self.reduce_hp(hazard.damage_points)
         self.health_bar.points -= hazard.damage_points
         if self.is_alive() == False:
            pass
         else:
            self.y_vel = 0
            self.invincibility = True
            self.stun = True
            play_sound('megaman_damage', universal_names.megaman_sounds, channel=2, volume=universal_names.sfx_volume + 0.1)
            self.all_timers.replenish_timer('spark_effect')
            self.all_timers.replenish_timer('stun')


   def check_all_collisions(self):
      #This will check all the sprite surfaces and there relation with self and act accordingly
      if camera.camera_transitioning() != True:
         self.check_ground_collision()
         self.check_ceiling_collision()
         self.check_wall_collision()
         if self.invincibility == False:
            self.check_hazard_collision()


   def shoot(self):

      #--if you shoot
      if self.all_timers.is_empty('can_shoot') == False and P_shooter.all_p.is_empty() == False:
         self.all_timers.countdown('can_shoot')
         self.all_timers.replenish_timer('shooting_flag') #the display function will countdown this timer
         play_sound('p_shooter', universal_names.megaman_sounds, volume=universal_names.sfx_volume)

         #--right
         if self.direction == True:
            P_shooter.fire(self.x + self.width - 15, self.y + self.height//4, P_shooter.x_vel)

         #--left
         else:
            P_shooter.fire(self.x + 4, self.y + self.height//4, -P_shooter.x_vel)


   def check_key_pressed(self):
      if self.is_standstill() == True:
         if self.stun != True:
            self.stop()

         #--if pressing right
      elif self.is_pressing(0) and self.colliding_hori != True and camera.camera_transitioning() != True:
         self.move_r()

      #--if pressing left
      elif self.is_pressing(2) and self.colliding_hori != True and camera.camera_transitioning() != True:
         self.move_L()

      #--if you shoot
      if self.is_pressing(4) and camera.camera_transitioning() != True:
         self.shoot()
      else:
         self.all_timers.replenish_timer('can_shoot') #the player can shoot after he lets go of the shoot button

      if camera.camera_transitioning() != True:
         self.jump()



   def jump(self):
      if self.is_grounded is True and self.can_jump is True:
         self.all_timers.replenish_timer('rise_flag')
         if self.is_pressing(5) and camera.camera_transitioning() != True:
            self.y_vel = self.jump_speed

      if self.gravity is False and self.is_pressing(5):
         self.rise()
      else:
         self.gravity = True

      if self.is_pressing(5) != True and self.is_grounded is True:
         self.can_jump = True
      else:
         self.can_jump = False


   def rise(self):
      if self.y_vel <= 0:
         self.gravity = True
      else:
         if self.all_timers.countdown('rise_flag', 5, loop=True) == True:
            self.y -= self.y_vel
         else:
            self.y_vel -= 2


   def startup_check(self):
      #will return true if startup animation is valid
      if universal_names.game_pause == False:
         self.all_timers.countdown('startup_animation')

      if self.is_standstill() and self.all_timers.is_empty('startup_flag') == False:
         if universal_names.game_pause == False:
            self.all_timers.countdown('startup_flag')
         return True

      elif self.is_standstill() != True and self.all_timers.is_empty('startup_flag'):
         self.all_timers.replenish_timer('startup_flag', 1)
         return True
      else:
         return False


   def startup_animation(self, surf):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, 'step')

      else:
         self.display_animation(universal_names.main_sprite, surf, 'step', flip=True)



   def idle_animation(self, surf, s=''):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, '{}idle'.format(s))
      else:
         self.display_animation(universal_names.main_sprite, surf, '{}idle'.format(s), flip=True)



   def walk_animation(self, surf, s=''):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, '{}walk'.format(s))

      else:
         self.display_animation(universal_names.main_sprite, surf, '{}walk'.format(s), flip=True)



   def ground_animation(self, surf, s=''):
      #--displaying any ground animations

      if self.all_timers.is_empty('startup_animation') is not True and s == '':
         self.startup_animation(surf)

      else:
         if self.is_standstill() == True:
            self.idle_animation(surf, s)
         else:
            self.walk_animation(surf, s)



   def jump_animation(self, surf, s=''):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, '{}jump'.format(s))
      else:
         self.display_animation(universal_names.main_sprite, surf, '{}jump'.format(s), flip=True)

   def diplay_effects(self, surf):
      if self.all_timers.is_empty('spark_effect') is False:
         self.display_animation('effects', surf, 'spark_effect')
         if universal_names.game_pause == False:
            self.all_timers.countdown('spark_effect')

   def stun_animation(self, surf):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, 'damage')
      else:
         self.display_animation(universal_names.main_sprite, surf, 'damage', flip=True)


   def display_megaman(self, surf, s=''):
      if self.startup_check() is True:
         self.all_timers.replenish_timer('startup_animation', 8)

      if self.no_display is False or camera.camera_transitioning() is True:
         if self.stun is True:
            self.stun_animation(surf)

         elif self.is_grounded is True:
            self.ground_animation(surf, s)
         else: 
            self.jump_animation(surf, s)

   def display(self, surf):
      #--displays self's sprites depending on the circumstances i.e if he's on the ground, if he shoots etc.
      if self.is_shooting():
         s = 'shoot_'
      else:
         s = ''

      if self.is_alive():
         self.update_sprite(universal_names.main_sprite)

      if self.invincibility is True:
         self.diplay_effects(surf)

      self.display_megaman(surf, s)


   def invincibility_frames(self):
      if self.all_timers.is_empty('invincibility_frame'):
         if self.no_display is True:
            self.no_display = False
         else:
            self.no_display = True
         self.all_timers.replenish_timer('invincibility_frame')

      else:
         if universal_names.game_pause != True:
            self.all_timers.countdown('invincibility_frame')


   def check_invincibility(self):
      if self.all_timers.is_empty('invincibility'):
         self.invincibility = False
         self.no_display = False
         self.all_timers.replenish_timer('invincibility')

      else:
         if universal_names.game_pause != True:
            self.all_timers.countdown('invincibility')
         self.invincibility_frames()


   def update(self):
      if self.is_alive() is True and self.is_active:
         if camera.camera_transitioning() != True and universal_names.game_pause != True:
            self.keys_pressed = pygame.key.get_pressed() #if the camera is not transitioning the I can catch input

         self.set_direction()
         if universal_names.game_pause == False:
            self.all_timers.countdown('shooting_flag', 20)
         self.check_all_collisions()

         if self.stun is True:
            self.check_stun()

         if self.invincibility is True:
            self.check_invincibility()

         if universal_names.game_pause != True:
            self.check_key_pressed()
         
         if self.gravity is True and camera.camera_transitioning() != True:
            self.apply_gravity()

         Sprite_surface.update(self)
         self.colliding_hori = False
         self.colliding_vert = False

      elif self.is_alive() != True:
         self.keys_pressed = None
         if self.all_timers.is_empty('death') is True:
            universal_names.game_pause = False
            self.is_active = False
            if self.all_timers.is_empty('death_sound') is not True:
               megaman_death_orb.set_orb_active()
               play_sound('death', universal_names.megaman_sounds, channel=1, volume=universal_names.sfx_volume + 0.1)
               self.all_timers.countdown('death_sound')

         else:
            self.all_timers.countdown('death')
            megaman_death_orb.spawn_orbs(self)
            universal_names.game_pause = True

         megaman_death_orb.move_orbs()


   def respawn(self):
      if self.respawn_obj.y < self.spawn_point[1] - 35:
         self.respawn_obj.row = 0
         self.respawn_obj.x = self.spawn_point[0]
         self.respawn_obj.is_active = True
         self.respawn_obj.move(0, 18)
      else:
         if self.all_timers.is_empty('respawn_animation') != True:
            self.respawn_obj.row = 1
            self.respawn_obj.x, self.respawn_obj.y = self.spawn_point[0], self.spawn_point[1] - 35
            self.all_timers.countdown('respawn_animation')
         else:
            play_sound('megaman_spawn', universal_names.megaman_sounds, channel=1, volume=universal_names.sfx_volume + 0.1)
            self.respawn_obj.is_active = False
            self.health_points = self.health_points_copy
            self.health_bar.points = self.health_points_copy
            self.is_active = True
            self.stun = False
            self.no_display = False
            self.invincibility = False
            self.x, self.y = self.spawn_point[0], self.spawn_point[1]
            self.x_vel = 0
            self.y_vel = 0
            Sprite_surface.update(self)
            self.all_timers.replenish_timer('startup_flag', 0)
            self.all_timers.replenish_timer('shooting_flag', 0)
            self.all_timers.replenish_timer('grounded_sound', 0)
            self.all_timers.replenish_timer('startup_animation', 0)
            for timer in self.all_timers:
               if timer not in ['shooting_flag', 'startup_animation', 'startup_flag', 'grounded_sound']:
                  self.all_timers.replenish_timer(timer)