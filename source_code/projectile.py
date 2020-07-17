#!/usr/bin/env python
import pygame
import math
import mega_stack
import megaman_object
import sprite
import universal_var
from timer import Timer
from misc_function import play_sound


class Projectile(sprite.Sprite_surface):

   def init_projectile_properties(self):
      self.init_x = 0
      self.init_y = 0
      self.angle = 0
      self.gravity = 0
      self.vel = 0
      self.launched = False
      self.time_start = 0
      self.time_now = 0

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=False, width=0, height=0, display_layer=3):
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer)
      self.init_projectile_properties()
      self.row = 0


   def set(self, x, y, vel=0, angle=0, gravity=0): #call init_projectile_properties on other class objects if you want to use this
      self.x = x
      self.y = y
      self.vel = vel
      self.init_x = x
      self.init_y = y
      self.angle = angle
      self.gravity = gravity
      self.time_start = self.time_now
      self.is_active = True
      self.launched = True
      sprite.Sprite_surface.update(self)


   def update(self):
      if self.is_on_screen():
         if self.launched and universal_var.game_pause != True and universal_var.game_reset != True:
            Projectile.move(self)

      else:
         self.is_active = False
         self.launched = False

   def display(self, surf, loop=True, game_pause=True):
      if self.sprite_dict != None:
         if (game_pause and universal_var.game_pause != True) or (game_pause == False):
            self.update_sprite(universal_var.main_sprite, auto_reset=loop)
         self.display_animation(universal_var.main_sprite, surf, self.get_sprite(universal_var.main_sprite, self.row)[0])


   def move(self): #code link: https://stackoverflow.com/questions/59267501/how-to-make-bullet-like-projectile-motion/59277125#59277125
      angle = math.radians(90 - self.angle)
      time_change = (self.time_now - self.time_start) 
      if ( time_change > 0 ):
         time_change /= 100.0  # fudge for metres/second to pixels/millisecond
         # re-calculate the displacement
         # x
         displacement_x  = self.vel * time_change * math.sin(angle) 
         # y
         half_gravity_time_squared = -self.gravity * time_change * time_change / 2.0
         displacement_y = self.vel * time_change * math.cos(angle) + half_gravity_time_squared 

         # reposition sprite
         self.x, self.y = self.init_x + int(displacement_x), self.init_y - int(displacement_y)
         sprite.Sprite_surface.update(self)
      self.time_now += 15

   def is_alive(self):
      return self.is_active


#-------------------------------------------------------------------------------


class Enemy_projectile_1(Projectile, megaman_object.Megaman_object):
   all_p_stack = mega_stack.Stack()
   all_p_lst = []

   def __init__(self, x, y, damage_points=10):
      width = 18
      height = 18
      bullet_sprite = sprite.Sprite(universal_var.main_sprite, x, y, width, height, [('enemy_projectile_1', [universal_var.projectiles['enemy_projectile_1']], 1)])
      main_coll_box = sprite.Collision_box(universal_var.hitbox, 0, 0, width, height, (240, 240, 0))

      super().__init__('Enemy_projectile_1', x, y, [bullet_sprite], [main_coll_box], width=width, height=height)
      self.damage_points = damage_points
      Enemy_projectile_1.add_to_class_lst(self, megaman_object.Megaman_object.hazards, self.ID)
      Enemy_projectile_1.add_to_class_lst(self, Enemy_projectile_1.all_p_lst, self.ID)
      Enemy_projectile_1.all_p_stack.push(self)

   @classmethod
   def set(cls, x, y, vel=0, angle=0, gravity=0):
      if cls.all_p_stack.is_empty() != True:
         p = cls.all_p_stack.pop()
         Projectile.set(p, x, y, vel, angle=angle, gravity=gravity)

   def display(self, surf):
      if universal_var.game_pause != True:
         self.update_sprite(universal_var.main_sprite)
      self.display_animation(universal_var.main_sprite, surf, 'enemy_projectile_1')

   def update(self):
      if self.is_active == False and self not in Enemy_projectile_1.all_p_stack.lst:
         Enemy_projectile_1.all_p_stack.push(self)
      Projectile.update(self)

#----------------------------------------------------------------------
