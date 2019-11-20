#!//usr/bin/env python
from sprite import *
from megaman_object import *
from misc_function import *
import pygame

class Character(Megaman_object):
   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, display_layer=4,
               gravity=False, direction=True, max_x_vel=0, health_points=100):
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer, gravity, direction, max_x_vel)
      self.health_points = health_points
      self.invincibility = False
      self.is_grounded = False
      self.stun = False
      self.knock_back_time = 10
      self.all_timers.add_ID('knock_back', self.knock_back_time)

   def knock_back(self, speed):
      if self.direction == True:
         self.x -= speed
      else:
         self.x += speed

   def is_alive(self):
      return self.health_points > 0

   def reduce_hp(self, amount):
      self.health_points -= amount

   def kill(self):
      self.reduce_hp(self.health_points)

   def restore(self, amount):
      self.health_points += amount

   def check_hp(self):
      if self.is_alive() == False:
         self.is_active = False


   def check_ground_collision(self):
      collision = self.check_collision_dict(Platform.all_sprite_surfaces, universal_names.feet, universal_names.hitbox, quota=1)
      if collision.is_empty() != True:
         platform = collision.pop()
         self.push_vert(platform, universal_names.feet, universal_names.hitbox)
         self.is_grounded = True
         self.gravity = False

         if self.all_timers.is_empty('grounded_sound') != True:
            play_sound('grounded', universal_names.megaman_sounds, channel=0, volume=universal_names.sfx_volume)
            self.all_timers.countdown('grounded_sound', 1)

      else:
         self.is_grounded = False
         self.all_timers.replenish_timer('grounded_sound')


   def check_ceiling_collision(self):
      collision = self.check_collision_dict(Platform.all_sprite_surfaces, universal_names.head, universal_names.hitbox, quota=1)
      if collision.is_empty() != True:
         ceiling = collision.pop()
         self.gravity = True
         self.push_vert(ceiling, universal_names.head, universal_names.hitbox)


   def check_wall_collision(self):
      collisions = self.check_collision_dict(Platform.all_sprite_surfaces, universal_names.hitbox, universal_names.hitbox, quota=4)
      if collisions.is_empty() != True:
         for wall in collisions:
            self.push_hori(wall, universal_names.hitbox, universal_names.hitbox)