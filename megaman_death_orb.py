#!/usr/bin/env python
import pygame
from sprite import *
from megaman_object import *
import universal_var
import timer
import projectile

all_orbs = []
orb = {}
orb_timers = timer.Timer()
spawned = True


class Death_orb(projectile.Projectile):
   all_orbs = []

   def __init__(self, x, y, start_time):
      width = 50
      height = 50
      display_layer = 5
      is_active = False
      orb_animation = [universal_var.misc_images['explosion_1'], universal_var.misc_images['explosion_2'], universal_var.misc_images['explosion_3'],
              universal_var.misc_images['explosion_4'], universal_var.misc_images['explosion_5']]

      orb_sprite = Sprite(universal_var.main_sprite, x, y, width, height, [('orb', orb_animation, 20)])
      super().__init__('Death_orb', x, y, [orb_sprite], None, is_active, width, height, display_layer)
      self.spawned = False
      self.all_timers = timer.Timer()
      self.all_timers.add_ID('start_time', start_time)
      Death_orb.add_to_class_lst(self, Death_orb.all_orbs, self.ID)

   def update(self):
      if self.spawned == True and self.all_timers.is_empty('start_time'):
         self.set(self.x, self.y, 15, self.angle)
         self.spawned = False
         self.all_timers.replenish_timer('start_time')
      elif self.spawned == True:
         self.all_timers.countdown('start_time')
      projectile.Projectile.update(self)

#-----------------------------------------------------------------------

def init(sprite_surf):
   start_time = [0, 15, 35]
   for i in range(3):
      Death_orb(sprite_surf.x, sprite_surf.y, start_time[i])
      Death_orb(sprite_surf.x, sprite_surf.y, start_time[i])
      Death_orb(sprite_surf.x, sprite_surf.y, start_time[i])
      Death_orb(sprite_surf.x, sprite_surf.y, start_time[i])

def set_orb_active(x, y):
   angles = [0, 90, 180, 270, 45, 135, 225, 315, 0, 90, 180, 270]
   for i in range(len(Death_orb.all_orbs)):
      orb = Death_orb.all_orbs[i]
      orb.x, orb.y = x, y
      orb.angle = angles[i]
      orb.spawned = True

def reset():
   for orb in Death_orb.all_orbs:
      orb.is_active = False
      orb.launched = False
      orb.spawned = False