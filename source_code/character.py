#!//usr/bin/env python
from sprite import *
from megaman_object import *
from misc_function import *
import camera
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
      self.all_timers.add_ID('invincibility', 160)
      self.all_timers.add_ID('invincibility_frame', 3)
      self.all_timers.add_ID('spark_effect', 30)
      self.all_timers.add_ID('grounded_sound', 0)

   def knock_back(self, speed):
      if camera.camera_transitioning() != True and universal_var.game_pause != True:
         self.x_vel = speed
         if self.direction == True:
            self.x -= self.x_vel
         else:
            self.x += self.x_vel

   def spawn(self):
      xdist = self.spawn_point[0] - self.x
      ydist = self.spawn_point[1] - self.y
      self.x, self.y = self.x + xdist, self.y + ydist


   def is_alive(self):
      return self.health_points > 0

   def reduce_hp(self, amount):
      self.health_points -= amount
      if self.health_points < 0:
         self.health_points = 0

   def kill(self):
      self.reduce_hp(self.health_points)

   def restore(self, amount):
      self.health_points += amount

   def check_hp(self):
      if self.is_alive() == False:
         self.is_active = False


   def check_ground_collision(self, coll_box):
      collision = self.check_collision_lst(Megaman_object.platforms, coll_box, universal_var.hitbox, quota=1)
      if collision.is_empty() != True:
         platform = collision.pop()
         self.push_vert(platform, coll_box, universal_var.hitbox)
         self.is_grounded = True
         self.gravity = False

         if self.all_timers.is_finished('grounded_sound') != True:
            play_sound('grounded', universal_var.megaman_sounds, channel=0, volume=universal_var.sfx_volume + 0.1)
            self.all_timers.countdown('grounded_sound')

      else:
         self.is_grounded = False
         self.all_timers.replenish_timer('grounded_sound', 1)


   def check_ceiling_collision(self, coll_box):
      collision = self.check_collision_lst(Megaman_object.platforms, coll_box, universal_var.hitbox, quota=1)
      if collision.is_empty() != True:
         ceiling = collision.pop()
         self.gravity = True
         self.push_vert(ceiling, coll_box, universal_var.hitbox)


   def check_wall_collision(self, coll_box):
      collisions = self.check_collision_lst(Megaman_object.platforms, coll_box, universal_var.hitbox, quota=4)
      if collisions.is_empty() != True:
         for wall in collisions:
            self.push_hori(wall, coll_box, universal_var.hitbox)