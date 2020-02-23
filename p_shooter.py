#!/usr/bin/env python
import pygame
from sprite import *
import mega_stack
import projectile
import universal_var
from misc_function import *
from megaman_object import *
import enemy

class P_shooter(projectile.Projectile):
   all_p_lst = []
   all_p_stack = mega_stack.Stack() #the stack acts as ammo source

   def __init__(self, ID, x, y):
      is_active = False
      width = 28
      height = 16
      p_sprite = Sprite(universal_var.main_sprite, x, y, width, height, [('p_shooter', [universal_var.projectiles['p_shooter']], 1)])
      main_coll_box = Collision_box(universal_var.hitbox, x, y, width, height)
      super().__init__('p_shooter', x, y, [p_sprite], [main_coll_box], width=width, height=height)
      self.damage_points = 10
      self.reflected = False
      P_shooter.all_p_stack.push(self)
      P_shooter.all_p_lst.append(self)

   def display(self, surf):
      self.display_animation(universal_var.main_sprite, surf, 'p_shooter')


   def update(self):
      if self.is_active == False and self not in P_shooter.all_p_stack.lst:
         P_shooter.all_p_stack.push(self)
         self.reflected = False
      projectile.Projectile.update(self)


   @classmethod
   def set(cls, x, y, vel=0, angle=0, gravity=0):
      if cls.all_p_stack.is_empty() != True:
         p = cls.all_p_stack.pop()
         projectile.Projectile.set(p, x, y, vel, angle=angle, gravity=gravity)
      else:
         print('stack empty')