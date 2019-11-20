#!/usr/bin/env python
import pygame
import universal_names
from mega_stack import *
from sprite import *
pygame.init()

class Megaman_object(Sprite_surface):
   gravity_speed = 15
   all_sprite_surfaces = {}

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, display_layer=1, gravity=False, direction=True, max_x_vel=0):
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer)
      Megaman_object.add_to_class_dict(self, ID)
      self.all_timers = timer.Timer()
      self.x_vel = 0
      self.max_x_vel = max_x_vel
      self.y_vel = 0
      self.gravity = gravity
      self.no_display = False
      self.direction = direction #False == Left, True == Right
      self.colliding_hori = False
      self.colliding_vert = False


   def push_hori(self, other, coll_box_self, coll_box_other):
      #--repels self in a horizontal direction
      if self.collbox_dict[coll_box_self].x >= other.collbox_dict[coll_box_other].x:
         if self.direction == False:
            self.colliding_hori = True
         self.x_vel = 0
         dist_betw_edges = other.collbox_dict[coll_box_other].right_edge - self.collbox_dict[coll_box_self].left_edge
         self.x += dist_betw_edges 

      elif self.collbox_dict[coll_box_self].x <= other.collbox_dict[coll_box_other].x:
         if self.direction == True:
            self.colliding_hori = True
         self.x_vel = 0
         dist_betw_edges = self.collbox_dict[coll_box_self].right_edge - other.collbox_dict[coll_box_other].left_edge
         self.x -= dist_betw_edges

      Sprite_surface.update(self)
      


   def push_vert(self, other, coll_box_self, coll_box_other):
      #--repels self in a vertical direction
      if self.collbox_dict[coll_box_self].y >= other.collbox_dict[coll_box_other].y:
         dist_betw_edges = self.collbox_dict[coll_box_self].top_edge - other.collbox_dict[coll_box_other].bottom_edge
         self.y -= dist_betw_edges - 1

      elif self.collbox_dict[coll_box_self].y <= other.collbox_dict[coll_box_other].y:
         dist_betw_edges = self.collbox_dict[coll_box_self].bottom_edge - other.collbox_dict[coll_box_other].top_edge
         self.y -= dist_betw_edges

      self.colliding_vert = True
      self.y_vel = 0
      Sprite_surface.update(self)


   def apply_gravity(self):
      if -(self.y_vel) >= Megaman_object.gravity_speed:
         self.y += Megaman_object.gravity_speed
      else:
         if self.y_vel >= 0:
            self.y_vel = 0

         if self.all_timers.countdown('y_accel_flag', 4, loop=True) == True:
            self.y += -(self.y_vel)

         else:
            self.y_vel -= 2


   def accelerate(self, acc_speed=0, max_x_vel=0):
      #--increases self.x_vel according to acc_speed parameter
      if acc_speed != 0:
         if self.all_timers.countdown('move_flag', acc_speed, loop=True) == False:
            if self.x_vel != max_x_vel:
               self.x_vel += 1



   def deccelerate(self, decc_speed=0):
      #--decreases self.x_vel according to acc_speed parameter
      if self.all_timers.countdown('move_flag', decc_speed, loop=True) == False:
         if self.x_vel != 0:
            self.x_vel -= 1


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


   def display(self, surf):
      self.update_sprite(universal_names.main_sprite)
      self.display_animation(universal_names.main_sprite, surf, self.get_sprite(universal_names.main_sprite, 0)[0])
      #self.display_collboxes(surf)

#-----------------------------------------

class Platform(Megaman_object):
   all_sprite_surfaces = {}

   def __init__(self, ID, x, y, sprites, coll_boxes=None, is_active=True, width=0, height=0, display_layer=2, gravity=False, max_x_vel=0):
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer, gravity, max_x_vel)
      Platform.add_to_class_dict(self, ID)


   def update(self):
      if self.gravity == True:
         self.apply_gravity()
      Sprite_surface.update(self)

   def display(self, surf):
      self.update_sprite(universal_names.main_sprite)
      self.display_animation(universal_names.main_sprite, surf, 'platform')
      #self.display_collboxes(surf)
