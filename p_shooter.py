#!/usr/bin/env python
import pygame
from sprite import *
import mega_stack
import universal_var
from misc_function import *
from megaman_object import *
import enemy

class P_shooter(Megaman_object):
   all_p_lst = []
   all_p_stack = mega_stack.Stack() #the stack acts as ammo source
   x_vel = 9

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=False, width=28, height=16, display_layer=3, gravity=False, direction=True, max_x_vel=0):
      sprites = [Sprite(universal_var.main_sprite, x, y, width, height, [('p_shooter', [universal_var.megaman_images['p_shooter']], 1)])]
      coll_boxes = [Collision_box(universal_var.hitbox, x, y, width, height)]
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer, gravity, direction, max_x_vel)
      self.is_active = is_active
      self.damage_points = 10
      P_shooter.all_p_stack.push(self)
      P_shooter.all_p_lst.append(self)

   def display(self, surf):
      self.display_animation(universal_var.main_sprite, surf, 'p_shooter')

   def move(self):
      self.x += self.x_vel


   def refill(self):
      if self.is_on_screen(universal_var.screen_width, universal_var.screen_height) == False:
         self.is_active = False
      if self.is_active == False:
         if self not in P_shooter.all_p_stack.lst:
            P_shooter.all_p_stack.push(self)

   def update(self):
      self.refill()
      if self.is_active == True and universal_var.game_pause == False:
         self.move()
      Sprite_surface.update(self)

   @classmethod
   def fire(cls, x, y, speed):
      #--fires bullet by popping of the stack and changing some properties
      p = cls.all_p_stack.pop()
      p.x, p.y = x, y
      Sprite_surface.update(p)
      p.is_active = True
      p.x_vel = speed