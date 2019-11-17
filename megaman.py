#!/usr/bin/env python
import universal_names
from sprite import *
import pygame
import timer
from misc_function import *
from p_shooter import *
from megaman import *
from enemy import *
from character import *

class Megaman(Character):
   def __init__(self, ID, x, y, sprites, coll_boxes, is_active=True, width=0, height=0, gravity=False, 
               direction=True, max_x_vel=1, health_points=100, controls=None, jump_speed=1, camera=None):
      
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, gravity, direction, max_x_vel, health_points)
      if controls == None:
         self.controls = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_p, pygame.K_w]
      else:
         self.controls = controls #--right, up, left, down, action, jump--

      self.current_key = pygame.key.get_pressed()
      self.jump_speed = jump_speed
      self.acc_speed = 3
      self.decc_speed = 3
      self.can_jump = False
      self.is_grounded = False
      self.camera = camera
      self.all_timers.add_ID('rise_flag', 4)
      self.all_timers.add_ID('shooting_flag', 0)
      self.all_timers.add_ID('grounded_sound', 1)
      self.all_timers.add_ID('can_shoot', 1)
      self.all_timers.add_ID('startup_flag', 0)
      self.all_timers.add_ID('startup_animation', 0)
      self.all_timers.add_ID('invincibility', 210)
      self.all_timers.add_ID('invincibility_frame', 3)
      self.all_timers.add_ID('spark_effect', 30)
      self.all_timers.add_ID('stun', 50)


   def is_pressing(self, n):
      #to see which key a player is pressing, 'n' refers to index in self.controls
      if self.stun == True:
         return False
      else:
         return self.current_key[self.controls[n]]

   def is_stunned(self):
      return self.all_timers.is_empty('stun') != True

   def is_standstill(self):
      return (not(self.is_pressing(0) or self.is_pressing(2)) or 
            (self.is_pressing(0) and self.is_pressing(2)))

   def is_shooting(self):
      return self.all_timers.is_empty('shooting_flag') == False
   
   def check_stun(self):
      self.all_timers.countdown('stun')
      if self.all_timers.is_empty('stun'):
         self.stun = False
      else:
         self.knock_back(1)
      
   def set_direction(self):
      #--To change the direction of self, note that direction == False means direction == Left, whereas True == Right

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


   def sprite_surf_check(self):
      #This will check all the sprite surfaces and there relation with self and act accordingly
      self.check_platform()
      self.check_camera()
      if self.invincibility == False:
         self.check_enemy()


   def check_camera(self):
      camera_flag = 0
      for sprite_surf in Camera_box.all_sprite_surfaces.values():
         if self.check_collision(sprite_surf, universal_names.hitbox, universal_names.hitbox) == True:
            if sprite_surf.ID == 'special_static' and self.camera != None:
               self.camera.transition('right', 10, 53)
            camera_flag += 1

      if self.camera != None:
         if camera_flag == 0:
            self.camera.static = False
         else:
            self.camera.static = True


   def check_enemy(self):
      for enemy in Enemy.all_sprite_surfaces.values():
         if self.check_collision(enemy, universal_names.hitbox, universal_names.hitbox) == True and enemy.is_alive() == True:
            self.health_points -= enemy.damage_points
            if self.is_alive() == False:
               break
            else:
               self.invincibility = True
               self.stun = True
               play_sound('megaman_damage', universal_names.megaman_sounds, channel=2, volume=universal_names.sfx_volume + 0.1)
               self.all_timers.replenish_timer('spark_effect')
               self.all_timers.replenish_timer('stun')
               break


   def check_platform(self):
      #checking if megaman has collided with any ceiling
      grounded_flag = 0
      for platform in Platform.all_sprite_surfaces.values():
         if platform.is_on_screen(universal_names.screen_width,universal_names.screen_height) == True:
            if self.check_collision(platform, universal_names.feet, universal_names.hitbox) == True and self.gravity == True:
               if grounded_flag < 1:
                  self.push_vert(platform, universal_names.feet, universal_names.hitbox)
               grounded_flag += 1

            elif self.check_collision(platform, universal_names.head, universal_names.hitbox) == True:
               self.gravity = True
               self.y += 1
               self.push_vert(platform, universal_names.head, universal_names.hitbox)

            elif self.check_collision(platform, universal_names.hitbox, universal_names.hitbox) == True:
               self.push_hori(platform, universal_names.hitbox, universal_names.hitbox)


      if grounded_flag == 0:
         self.is_grounded = False
         self.all_timers.replenish_timer('grounded_sound')
      else:
         self.is_grounded = True
         self.gravity = False
         if self.all_timers.is_empty('grounded_sound') == False:
            play_sound('grounded', universal_names.megaman_sounds, channel=0, volume=universal_names.sfx_volume)
            self.all_timers.countdown('grounded_sound', 1)

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
         if self.colliding_hori != True:
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
         if self.colliding_hori != True:
            self.x_vel = self.max_x_vel
            self.x += self.x_vel


   def shoot(self):
      #--shoots megaman's p_shooter

      #--if you shoot
      if self.all_timers.is_empty('can_shoot') == False and P_shooter.all_p.is_empty() == False:
         self.all_timers.countdown('can_shoot')
         self.all_timers.replenish_timer('shooting_flag') #the display function will countdown this timer
         play_sound('p_shooter', universal_names.megaman_sounds, volume=universal_names.sfx_volume)

         #--right
         if self.direction == True:
            P_shooter.fire(self.x + self.width//2, self.y + self.height//4, P_shooter.x_vel)

         #--left
         else:
            P_shooter.fire(self.x + self.width//3, self.y + self.height//4, -P_shooter.x_vel)


   def check_key_pressed(self):

         #--if pressing right and left
      if self.is_standstill() == True:
         self.stop()

         #--if pressing right
      elif self.is_pressing(0) and self.colliding_hori != True:
         self.move_r()

      #--if pressing left
      elif self.is_pressing(2) and self.colliding_hori != True:
         self.move_L()

      #--if you shoot
      if self.is_pressing(4):
         self.shoot()
      else:
         self.all_timers.replenish_timer('can_shoot') #the player can shoot after he lets go of the shoot button



   def jump(self):
      if self.is_grounded == True and self.can_jump == True:
         self.all_timers.replenish_timer('rise_flag')
         if self.is_pressing(5):
            self.y_vel = self.jump_speed

      if self.gravity == False and self.is_pressing(5):
         self.rise()
      else:
         self.gravity = True

      if self.is_pressing(5) != True and self.is_grounded == True:
         self.can_jump = True
      else:
         self.can_jump = False


   def startup_check(self):
      #will return true if startup animation is valid
      self.all_timers.countdown('startup_animation')

      if self.is_standstill() and self.all_timers.is_empty('startup_flag') == False:
         self.all_timers.countdown('startup_flag')
         return True

      elif self.is_standstill() != True and self.all_timers.is_empty('startup_flag'):
         self.all_timers.replenish_timer('startup_flag', 1)
         return True
      else:
         return False


   def startup_animation(self, surf):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, 'step_right')

      else:
         self.display_animation(universal_names.main_sprite, surf, 'step_left')



   def rise(self):
      if self.y_vel <= 0:
         self.gravity = True
      else:
         if self.all_timers.countdown('rise_flag', 5, loop=True) == True:
            self.y -= self.y_vel
         else:
            self.y_vel -= 2



   def idle_animation(self, surf, s=''):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, '{}idle_right'.format(s))
      else:
         self.display_animation(universal_names.main_sprite, surf, '{}idle_left'.format(s))



   def walk_animation(self, surf, s=''):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, '{}walk_right'.format(s))

      else:
         self.display_animation(universal_names.main_sprite, surf, '{}walk_left'.format(s))



   def ground_animation(self, surf, s=''):
      #--displaying any ground animations

      if self.all_timers.is_empty('startup_animation') != True and s == '':
         self.startup_animation(surf)

      else:
         if self.is_standstill() == True:
            self.idle_animation(surf, s)
         else:
            self.walk_animation(surf, s)



   def jump_animation(self, surf, s=''):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, '{}jump_right'.format(s))
      else:
         self.display_animation(universal_names.main_sprite, surf, '{}jump_left'.format(s))

   def diplay_effects(self, surf):
      if self.all_timers.is_empty('spark_effect') == False:
         self.display_animation('effects', surf, 'spark_effect')
         self.all_timers.countdown('spark_effect')

   def stun_animation(self, surf):
      if self.direction == True:
         self.display_animation(universal_names.main_sprite, surf, 'damage_right')
      else:
         self.display_animation(universal_names.main_sprite, surf, 'damage_left')


   def display_megaman(self, surf, s=''):
      if self.no_display == False:
         if self.startup_check() == True:
            self.all_timers.replenish_timer('startup_animation', 8)

         if self.stun == True:
            self.stun_animation(surf)

         elif self.is_grounded == True:
            self.ground_animation(surf, s)
         else: 
            self.jump_animation(surf, s)

   def display(self, surf):
      #--displays self's sprites depending on the circumstances i.e if he's on the ground, if he shoots etc.
      if self.is_shooting():
         s = 'shoot_'
      else:
         s = ''

      self.update_sprite(universal_names.main_sprite)

      if self.invincibility == True:
         self.diplay_effects(surf)

      self.display_megaman(surf, s)


   def invincibility_frames(self):
      if self.all_timers.is_empty('invincibility_frame'):
         if self.no_display == True:
            self.no_display = False
         else:
            self.no_display = True
         self.all_timers.replenish_timer('invincibility_frame')

      else:
         self.all_timers.countdown('invincibility_frame')


   def check_invincibility(self):
      if self.all_timers.is_empty('invincibility'):
         self.invincibility = False
         self.no_display = False
         self.all_timers.replenish_timer('invincibility')

      else:
         self.all_timers.countdown('invincibility')
         self.invincibility_frames()


   def teleport(self, x, y):
      self.x = x
      self. y = y



   def update(self):
      if self.is_active == True:
         self.current_key = pygame.key.get_pressed()
         self.set_direction()
         self.all_timers.countdown('shooting_flag', 23)
         if self.stun == True:
            self.check_stun()
         self.sprite_surf_check()
         if self.invincibility == True:
            self.check_invincibility()

         if self.camera != None and self.camera.static == False:
            self.camera.follow_x(self)

         self.check_key_pressed()
         self.jump()
         self.colliding_hori = False
         self.colliding_vert = False
         if self.gravity == True:
            self.apply_gravity()

         Sprite_surface.update(self)
