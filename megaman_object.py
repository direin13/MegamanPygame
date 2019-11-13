#!/usr/bin/env python
import pygame
from sprite import *
pygame.init()

class Megaman_object(Sprite_surface):
   gravity_speed = 15
   all_sprite_surfaces = {}

   def __init__(self, ID, x, y, sprite, coll_boxes=None, gravity=False, x_vel=0, y_vel=0, direction=True, width=0, height=0, is_alive=True):
      super().__init__(ID, x, y, sprite, coll_boxes, is_alive)
      Megaman_object.add_to_dict(self, ID)
      self.all_timers = timer.Timer()
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
         self.x_vel = 0
         dist_betw_edges = other.all_collboxes[coll_box_other].right_edge - self.all_collboxes[coll_box_self].left_edge
         self.x += dist_betw_edges 
         return

      elif self.all_collboxes[coll_box_self].x <= other.all_collboxes[coll_box_other].x:
         if self.direction == True:
            self.colliding_hori = True
         self.x_vel = 0
         dist_betw_edges = self.all_collboxes[coll_box_self].right_edge - other.all_collboxes[coll_box_other].left_edge
         self.x -= dist_betw_edges
         return


   def push_vert(self, other, coll_box_self, coll_box_other):
      #--repels self in a vertical direction
      if self.all_collboxes[coll_box_self].y >= other.all_collboxes[coll_box_other].y:
         self.colliding_vert = True
         self.y_vel = 0
         dist_betw_edges = self.all_collboxes[coll_box_self].top_edge - other.all_collboxes[coll_box_other].bottom_edge
         self.y -= dist_betw_edges
         Sprite_surface.update(self)
         return

      elif self.all_collboxes[coll_box_self].y <= other.all_collboxes[coll_box_other].y:
         self.colliding_vert = True
         self.y_vel = 0
         dist_betw_edges = self.all_collboxes[coll_box_self].bottom_edge - other.all_collboxes[coll_box_other].top_edge
         self.y -= dist_betw_edges
         Sprite_surface.update(self)


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

   def display(self, surf, speed=1):
      self.sprite.update(speed)
      self.sprite.display_animation(surf, self.sprite.active_frames[0][0])
      #self.display_collboxes(surf)

#-----------------------------------------

class Platform(Megaman_object):
   all_sprite_surfaces = {}

   def __init__(self, ID, x, y, sprite, coll_boxes=None, gravity=False, x_vel=0):
      super().__init__(ID, x, y, sprite, coll_boxes, gravity, x_vel)
      Platform.add_to_dict(self, ID)


   def update(self):
      if self.gravity == True:
         self.apply_gravity()
      Sprite_surface.update(self)

   def display(self, surf, speed=1):
      self.sprite.update(speed)
      self.sprite.display_animation(surf, self.sprite.active_frames[0][0])
      #self.display_collboxes(surf)