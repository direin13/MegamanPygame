#!/usr/bin/env python

import universal_names
from sprite import *
from character import *
from megaman import *
import camera

class Enemy(Character):
   all_sprite_surfaces = []

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, display_layer=4, 
               gravity=False, direction=True, max_x_vel=0, health_points=100, damage_points=0):
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer, gravity, direction, max_x_vel, health_points)
      Enemy.add_to_class_lst(self, Enemy.all_sprite_surfaces, ID)
      Enemy.add_to_class_lst(self, Megaman_object.hazards, ID)
      self.damage_points = damage_points
      self.all_timers.add_ID('explosion_animation', 15)


   def display(self, surf):
      if self.is_alive():
         Megaman_object.display(self, surf)
      else:
         self.update_sprite(universal_names.main_sprite)
         self.display_animation(universal_names.main_sprite, surf, 'explosion')




   def update(self):
      if camera.camera_transitioning() == True:
         self.is_active = False
      else:
         if self.is_on_screen(universal_names.screen_width, universal_names.screen_height):
            self.is_active = True

      if self.is_alive() == False:
         self.all_timers.countdown('explosion_animation')

      if self.all_timers.is_empty('explosion_animation'):
         self.is_active = False
      Sprite_surface.update(self)