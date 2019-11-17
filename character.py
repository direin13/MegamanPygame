#!//usr/bin/env python
from sprite import *
from megaman_object import *
import pygame

class Character(Megaman_object):
   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, 
               gravity=False, direction=True, max_x_vel=0, health_points=100):
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, gravity, direction, max_x_vel)
      self.health_points = health_points
      self.invincibility = False
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
      self.is_active = False

   def restore(self, amount):
      self.health_points += amount

   def check_hp(self):
      if self.is_alive() == False:
         self.is_active = False