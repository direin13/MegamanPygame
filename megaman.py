#!/usr/bin/env python
import universal_names
from sprite import *
import pygame
import timer
from misc_function import *
from p_shooter import *
from megaman_object import *

class Megaman(Megaman_object):
   def __init__(self, ID, x, y, sprite, coll_boxes, run_frame_speed, idle_frame_speed, gravity=False, controls=None, x_vel=1, jump_speed=1, direction=True, camera=None, is_alive=True):
      super().__init__(ID, x, y, sprite, coll_boxes, gravity, x_vel, direction, is_alive)
      if controls == None:
         self.controls = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_p, pygame.K_w]
      else:
         self.controls = controls #--right, up, left, down, action, jump--

      self.current_key = pygame.key.get_pressed()
      self.jump_speed = jump_speed
      self.acc_speed = 3
      self.decc_speed = 3
      self.can_jump = False
      self.run_frame_speed = run_frame_speed
      self.idle_frame_speed = idle_frame_speed
      self.can_jump = False
      self.can_shoot = True
      self.is_grounded = False
      self.camera = camera
      self.all_timers.add_ID('rise_flag', 4)
      self.all_timers.add_ID('shooting_flag', 0)

      for i in range(0, 3): #--making p_shooter bullets
         P_shooter('P_shooter', 0, 0)

   def set_direction(self):
      #--To change the direction of self, note that direction == False means direction == Left, whereas True == Right

      if self.current_key[self.controls[0]] and self.current_key[self.controls[2]]:
         #--if pressing left and right at the same time
         self.direction = self.direction

      elif self.current_key[self.controls[0]]:
         #--left
         if self.is_grounded != True:
            self.direction = True
         else:
            if self.x_vel == 0:
               self.direction = True

      elif self.current_key[self.controls[2]]:
         #--right
         if self.is_grounded != True:
            self.direction = False
         else:
            if self.x_vel == 0:
               self.direction = False


   def sprite_surf_check(self):
      #This will check all the sprite surfaces and there relation with self and act accordingly
      
      grounded_flag = 0
      camera_flag = 0
      for sprite_surf in Sprite_surface.all_sprite_surfaces.values():
         if sprite_surf != self:
            if isinstance(sprite_surf, Platform):
               if self.check_collision(sprite_surf, universal_names.feet, universal_names.hitbox) == True and self.gravity == True:
                  self.push_vert(sprite_surf, universal_names.feet, universal_names.hitbox)
                  grounded_flag += 1

               elif self.check_collision(sprite_surf, universal_names.head, universal_names.hitbox) == True:
                  self.gravity = True
                  self.y += 1
                  self.push_vert(sprite_surf, universal_names.head, universal_names.hitbox)

               elif self.check_collision(sprite_surf, universal_names.hitbox, universal_names.hitbox) == True:
                  self.push_hori(sprite_surf, universal_names.hitbox, universal_names.hitbox)

            if isinstance(sprite_surf, Camera_box):
               if self.check_collision(sprite_surf, universal_names.hitbox, universal_names.hitbox) == True:
                  if sprite_surf.ID.split('-')[0] == 'special_static' and self.camera != None:
                     self.camera.transition('right', 10, 50)
                  camera_flag += 1

      if grounded_flag == 0:
         self.is_grounded = False
      else:
         self.is_grounded = True

      if self.camera != None:
         if camera_flag == 0:
            self.camera.static = False
         else:
            self.camera.static = True

         


   def move(self, x=None, y=None):
      #moves the character, if co_ordinates not specified then the keys pressed will be checked
      if x != None and y != None:
         self.x = x
         self.y = y
         return

         #--if moving right and left at the same time
      if self.current_key[self.controls[0]] and self.current_key[self.controls[2]]:
         if self.is_grounded == True:
            self.deccelerate(self.decc_speed)
         else:
            self.x_vel = 0

         if self.direction == True:
            self.x += self.x_vel
         else:
            self.x -= self.x_vel

      else:
         #--if moving right
         if self.current_key[self.controls[0]] and self.colliding_hori != True:
            if self.is_grounded == True:
               if self.direction == True:
                  self.accelerate(self.acc_speed)
                  self.x += self.x_vel
               else:
                  self.deccelerate(self.decc_speed)
                  self.x -= self.x_vel

            else:
               if self.colliding_hori != True:
                  self.x_vel = self.max_x_vel
                  self.x += self.x_vel

         #--if moving left
         elif self.current_key[self.controls[2]] and self.colliding_hori != True:
            if self.is_grounded == True:
               if self.direction == False:
                  self.accelerate(self.acc_speed)
                  self.x -= self.x_vel
               else:
                  self.deccelerate(self.decc_speed)
                  self.x += self.x_vel

            else:
               if self.colliding_hori != True:
                  self.x_vel = self.max_x_vel
                  self.x -= self.x_vel

         #--if not moving right or left
         else:
            if self.is_grounded == True:
               self.deccelerate(self.decc_speed)
            else:
               self.x_vel = 0

            if self.direction == True:
               self.x += self.x_vel
            else:
               self.x -= self.x_vel


   def accelerate(self, acc_speed=0):
      #--increases self.x_vel according to acc_speed parameter
      if acc_speed != 0:
         if self.all_timers.countdown('move_flag', acc_speed, loop=True) == False:
            if self.x_vel != self.max_x_vel:
               self.x_vel += 1



   def deccelerate(self, decc_speed=0):
      #--decreases self.x_vel according to acc_speed parameter
      if self.all_timers.countdown('move_flag', decc_speed, loop=True) == False:
         if self.x_vel != 0:
            self.x_vel -= 1



   def jump(self):
      if self.is_grounded == True and self.can_jump == True:
         self.gravity = False
         self.all_timers.replenish_timer('rise_flag')
         if self.current_key[self.controls[5]]:
            self.y_vel = self.jump_speed
            self.can_jump = False
            self.is_grounded = False

      if self.gravity == False and self.current_key[self.controls[5]]:
         self.rise()
      else:
         self.gravity = True

      if self.current_key[self.controls[5]] != True and self.is_grounded == True:
         self.can_jump = True
      else:
         self.can_jump = False



   def rise(self):
      if self.y_vel <= 0:
         self.gravity = True
      else:
         if self.all_timers.countdown('rise_flag', 4, loop=True) == True:
            self.y -= self.y_vel
         else:
            self.y_vel -= 2


   def shoot(self):
      #--shoots megaman's p_shooter

      #--if you shoot
      if self.current_key[self.controls[4]] and self.can_shoot == True and P_shooter.all_p.is_empty() == False:
         self.can_shoot = False
         self.all_timers.replenish_timer('shooting_flag') #the display function will countdown this timer

         #--right
         if self.direction == True:
            P_shooter.fire(self.x + self.width//2, self.y + self.height//4, P_shooter.x_vel)

         #--left
         else:
            P_shooter.fire(self.x + self.width//2, self.y + self.height//4, -P_shooter.x_vel)

      if self.current_key[self.controls[4]] != True:
         self.can_shoot = True



   def display(self, surf):
      #--displays self's sprites depending on the circumstances i.e if he's on the ground, if he shoots etc.

      shooting = self.all_timers.countdown('shooting_flag', 23) #--to get wether player has shot or not, will change the animation displayed via variable 's'
      if shooting == False:
         s = ''
      else:
         s = 'shoot_'


      if self.is_grounded == True:

         #--idle
         if self.x_vel == 0:
            self.sprite.update(self.idle_frame_speed)
            if self.direction == True:
               self.sprite.display_animation(surf, '{}idle_right'.format(s))
            else:
               self.sprite.display_animation(surf, '{}idle_left'.format(s))

         #--walking
         else:
            self.sprite.update(self.run_frame_speed)
            if self.direction == True:
               if self.x_vel == self.max_x_vel or (self.x_vel > 0 and shooting == True):
                  self.sprite.display_animation(surf, '{}walk_right'.format(s))
               if self.x_vel != self.max_x_vel and shooting == False:
                  self.sprite.display_animation(surf, 'step_right')

            else:
               if self.x_vel == self.max_x_vel or (self.x_vel > 0 and shooting == True):
                  self.sprite.display_animation(surf, '{}walk_left'.format(s))
               if self.x_vel != self.max_x_vel and shooting == False:
                  self.sprite.display_animation(surf, 'step_left')

      #jump
      else: 
         self.sprite.update(self.run_frame_speed)
         if self.direction == True:
            self.sprite.display_animation(surf, '{}jump_right'.format(s))
         else:
            self.sprite.display_animation(surf, '{}jump_left'.format(s))



   def update(self):
      self.current_key = pygame.key.get_pressed()
      self.set_direction()
      self.sprite_surf_check()
      if self.camera != None and self.camera.static == False:
         self.camera.follow_x(self)
      self.move()
      self.shoot()
      self.colliding_hori = False
      self.colliding_vert = False
      self.jump()
      if self.gravity == True:
         self.apply_gravity()
      Sprite_surface.update(self)
