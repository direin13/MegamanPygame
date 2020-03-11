#!/usr/bin/env python
import pygame
import universal_var
from mega_stack import *
from sprite import *
pygame.init()

class Megaman_object(Sprite_surface):
   gravity_speed = 17
   all_sprite_surfaces = []
   platforms = []
   hazards = []

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, display_layer=1, gravity=False, direction=True, max_x_vel=1):
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer)
      Megaman_object.add_to_class_lst(self, Megaman_object.all_sprite_surfaces, ID)
      self.all_timers = timer.Timer()
      self.x_vel = 0
      self.max_x_vel = max_x_vel
      self.y_vel = 0
      self.gravity = gravity
      self.no_display = False
      self.direction = direction #False == Left, True == Right
      self.colliding_hori = False
      self.colliding_vert = False
      self.row = 0 # for displaying the 0th row for default display function
      self.sprite_loop = True


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
      if self.colliding_vert == True or universal_var.game_pause == True:
         return
      
      if -(self.y_vel) >= Megaman_object.gravity_speed:
         self.y += Megaman_object.gravity_speed
      else:

         self.all_timers.countdown('y_accel_flag', 4, loop=True)
         if self.all_timers.is_empty('y_accel_flag') != True:
            self.y += -(self.y_vel)

         else:
            self.y_vel -= 2


   def accelerate(self, acc_speed=0, max_x_vel=0):
      #--increases self.x_vel according to acc_speed parameter
      if acc_speed != 0:
         self.all_timers.countdown('move_flag', acc_speed, loop=True)
         if self.all_timers.is_empty('move_flag'):
            if self.x_vel != max_x_vel:
               self.x_vel += 1



   def deccelerate(self, decc_speed=0):
      #--decreases self.x_vel according to acc_speed parameter
      self.all_timers.countdown('move_flag', decc_speed, loop=True)
      if self.all_timers.is_empty('move_flag'):
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

   def move(self, x_vel=0, y_vel=0):
      self.x_vel = x_vel
      self.y_vel = y_vel
      self.x += x_vel
      self.y += y_vel


   def teleport(self, x, y):
      self.x = x
      self.y = y



   def display(self, surf, game_pause=True):
      if self.sprite_dict != None:
         if (game_pause and universal_var.game_pause != True) or (game_pause == False):
            self.update_sprite(universal_var.main_sprite, auto_reset=self.sprite_loop)
         self.display_animation(universal_var.main_sprite, surf, self.get_sprite(universal_var.main_sprite, self.row)[0])
         #self.display_collboxes(surf)

   def follow(self, x=None, y=None, x_vel=0, y_vel=0):
      if self.x != x and x != None:
         if self.x < x:
            self.x += x_vel
         elif self.x > x:
            self.x -= x_vel

      if self.y != y and y != None:
         if self.y < y:
            self.y += y_vel
         elif self.y > y:
            self.y -= y_vel

   def is_alive(self):
      return self.is_active

#-----------------------------------------

