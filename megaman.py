#!/usr/bin/env python
import pygame
from sprite import *
pygame.init()

class Megaman_object(Sprite_surface):
   gravity_speed = 15

   def __init__(self, ID, x, y, sprite, coll_boxes, x_vel=1, gravity=False, direction=True):
      super().__init__(ID, x, y, sprite, coll_boxes)
      self.x_vel = 0
      self.max_x_vel = x_vel
      self.y_vel = 0
      self.gravity = gravity
      self.direction = direction #False == Left, True == Right
      self.colliding_hori = False
      self.colliding_vert = False


   def push_hori(self, other, coll_box_self, coll_box_other):
      #--repels self in a horizontal direction
      if self.all_collboxes[coll_box_self].x >= other.all_collboxes[coll_box_other].x:
         if self.direction == False:
            self.colliding_hori = True
         dist_betw_edges = other.all_collboxes[coll_box_other].right_edge - self.all_collboxes[coll_box_self].left_edge
         self.x += dist_betw_edges 
         self.update()
         return

      elif self.all_collboxes[coll_box_self].x <= other.all_collboxes[coll_box_other].x:
         if self.direction == True:
            self.colliding_hori = True
         dist_betw_edges = self.all_collboxes[coll_box_self].right_edge - other.all_collboxes[coll_box_other].left_edge
         self.x -= dist_betw_edges
         self.update()
         return


   def push_vert(self, other, coll_box_self, coll_box_other):
      #--repels self in a vertical direction
      if self.all_collboxes[coll_box_self].y >= other.all_collboxes[coll_box_other].y:
         self.colliding_vert = True
         dist_betw_edges = self.all_collboxes[coll_box_self].top_edge - other.all_collboxes[coll_box_other].bottom_edge
         self.y -= dist_betw_edges
         self.update()
         return

      elif self.all_collboxes[coll_box_self].y <= other.all_collboxes[coll_box_other].y:
         self.colliding_vert = True
         dist_betw_edges = self.all_collboxes[coll_box_self].bottom_edge - other.all_collboxes[coll_box_other].top_edge
         self.y -= dist_betw_edges
         self.update()


   def check_collision(self, other, coll_box_self, coll_box_other):
      if self.all_collboxes[coll_box_self].collision_sprite(other.all_collboxes[coll_box_other]):
         return True
      else:
         return False

   def apply_gravity(self):
      if -(self.y_vel) >= Megaman_object.gravity_speed:
         self.y += Megaman_object.gravity_speed
      else:
         if self.y_vel >= 0:
            self.y_vel = 0

         if self.jump_flag <= 2:
            self.jump_flag += 1
            self.y += -(self.y_vel)

         else:
            self.jump_flag = 0
            self.y_vel -= 2

#---------------------------------------------------------------------------------------------


class Main_character(Megaman_object):
   def __init__(self, ID, x, y, sprite, coll_boxes, run_frame_speed, idle_frame_speed, controls=None, x_vel=1, jump_speed=1, gravity=False, direction=True, camera=None):
      if controls == None:
         self.controls = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_p, pygame.K_w]
      else:
         self.controls = controls #--right, up, left, down, action, jump--

      self.current_key = pygame.key.get_pressed()
      self.jump_speed = jump_speed
      self.acc_speed = 3
      self.decc_speed = 3
      self.standstill = True
      self.can_jump = False
      self.run_frame_speed = run_frame_speed
      self.idle_frame_speed = idle_frame_speed
      self.can_jump = False
      self.jump_flag = 0
      self.move_flag = 0
      self.is_grounded = False
      self.camera = camera
      super().__init__(ID, x, y, sprite, coll_boxes, x_vel, gravity, direction)

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
               if self.check_collision(sprite_surf, 'feet', 'hit_box') == True and self.gravity == True:
                  self.push_vert(sprite_surf, 'feet', 'hit_box')
                  grounded_flag += 1

               elif self.check_collision(sprite_surf, 'head', 'hit_box') == True:
                  self.gravity = True
                  self.y += 1
                  self.push_vert(sprite_surf, 'head', 'hit_box')

               elif self.check_collision(sprite_surf, 'hit_box', 'hit_box') == True:
                  self.push_hori(sprite_surf, 'hit_box', 'hit_box')

            if isinstance(sprite_surf, Camera_box):
               if self.check_collision(sprite_surf, 'hit_box', 'hit_box') == True:
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
         if self.move_flag < acc_speed:
            self.move_flag += 1

         elif self.move_flag >= acc_speed:
            self.move_flag = 0
            if self.x_vel != self.max_x_vel:
               self.x_vel += 1




   def deccelerate(self, decc_speed=0):
      #--decreases self.x_vel according to acc_speed parameter
      if decc_speed != 0:
         if self.move_flag < decc_speed:
            self.move_flag += 1

         elif self.move_flag >= decc_speed:
            self.move_flag = 0
            if self.x_vel != 0:
               self.x_vel -= 1


   def jump(self):
      if self.is_grounded == True and self.can_jump == True:
         self.gravity = False
         self.jump_flag = 0
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
         if self.jump_flag <= 2:
            self.jump_flag += 1
            self.y -= self.y_vel
         else:
            self.jump_flag = 0
            self.y_vel -= 2



   def display(self, surf):
      if self.is_grounded == True:
         #hold right
         if self.x_vel == 0:
            self.sprite.update(self.idle_frame_speed)
            if self.direction == True:
               self.sprite.display_animation(surf, 'idle_right')
            else:
               self.sprite.display_animation(surf, 'idle_left')

         #hold left
         else:
            self.sprite.update(self.run_frame_speed)
            if self.direction == True:
               if self.x_vel == self.max_x_vel:
                  self.sprite.display_animation(surf, 'right')
               else:
                  self.sprite.display_animation(surf, 'step_right')

            else:
               if self.x_vel == self.max_x_vel:
                  self.sprite.display_animation(surf, 'left')
               else:
                  self.sprite.display_animation(surf, 'step_left')

      #jump
      else: 
         self.sprite.update(self.run_frame_speed)
         if self.direction == True:
            self.sprite.display_animation(surf, 'jump_right')
         else:
            self.sprite.display_animation(surf, 'jump_left')



   def update_character(self):
      self.current_key = pygame.key.get_pressed()
      self.set_direction()
      self.sprite_surf_check()

      if self.colliding_hori:
         self.x_vel = 0
      if self.colliding_vert:
         self.y_vel = 0
         pass
      self.move()
      self.colliding_hori = False
      self.colliding_vert = False
      self.jump()
      if self.gravity == True:
         self.apply_gravity()
      self.update()
      if self.camera != None and self.camera.static == False:
         self.camera.follow_x(self)


#-----------------------------------------

class Platform(Megaman_object):
   def __init__(self, ID, x, y, sprite, coll_boxes, gravity=False):
      super().__init__(ID, x, y, sprite, coll_boxes, gravity)
      self.jump_flag = 0

   def display(self, surf, speed=1):
      self.sprite.update(speed)
      self.sprite.display_animation(surf, self.sprite.active_frames[0][0])
      #self.display_collboxes(surf)
