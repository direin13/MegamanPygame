#!/usr/bin/env python
import pygame
from sprite import *
from megaman_object import *
import universal_var
import timer
from mega_stack import Stack
import projectile


class Death_orb(projectile.Projectile):
   all_orbs_lst = []
   all_orbs_stack = Stack()

   def __init__(self):
      x, y = 0, 0
      width = 50
      height = 50
      display_layer = 4
      is_active = False
      orb_animation = [universal_var.misc_images['explosion_1'], universal_var.misc_images['explosion_2'], universal_var.misc_images['explosion_3'],
              universal_var.misc_images['explosion_4'], universal_var.misc_images['explosion_5'], universal_var.misc_images['blank']]

      orb_sprite = Sprite(universal_var.main_sprite, x, y, width, height, [('orb', orb_animation, 20)])
      super().__init__('Death_orb', x, y, [orb_sprite], None, is_active, width, height, display_layer)
      self.spawned = False
      self.vel = 0
      self.all_timers = timer.Timer()
      self.all_timers.add_ID('start_time', 0)
      Death_orb.add_to_class_lst(self, Death_orb.all_orbs_lst, self.ID)
      Death_orb.all_orbs_stack.push(self)

   def update(self):
      if self.spawned == True and self.all_timers.is_finished('start_time'):
         self.set(self.x, self.y, self.vel, self.angle)
         self.spawned = False
         self.all_timers.replenish_timer('start_time')
      elif self.spawned == True:
         self.all_timers.countdown('start_time')
      elif self not in Death_orb.all_orbs_stack.lst:
         Death_orb.all_orbs_stack.push(self)
      projectile.Projectile.update(self)

#-----------------------------------------------------------------------
   @staticmethod
   def init(amount=1):
      for i in range(amount):
         Death_orb()

   @classmethod
   def set_orb_active(cls, x, y, start_time, angle, vel):
      orb = cls.all_orbs_stack.pop()
      orb.x, orb.y = x, y
      orb.angle = angle
      orb.vel = vel
      orb.spawned = True
      orb.all_timers.replenish_timer('start_time', start_time)

   @classmethod
   def reset(cls):
      for orb in cls.all_orbs_lst:
         orb.is_active = False
         orb.launched = False
         orb.spawned = False
         sprite = orb.get_sprite(universal_var.main_sprite)
         sprite.current_frame = 0