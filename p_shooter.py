#!/usr/bin/env python
import pygame
from sprite import *
import mega_stack
import universal_names
from megaman_object import *

class P_shooter(Megaman_object):
   all_p = mega_stack.Stack() #the stack acts as ammo source
   x_vel = 6

   def __init__(self, ID, x, y, sprite=None, coll_boxes=None, gravity=False, x_vel=0, y_vel=0, direction=True, width=1, height=1, is_alive=False):
      sprite = Sprite(x, y, 30, 20, [('p_shooter', [universal_names.megaman_images['p_shooter']])])
      coll_boxes = [Collision_box(universal_names.hitbox, x, y, 30, 20)]
      super().__init__(ID, x, y, sprite, coll_boxes, gravity, x_vel, y_vel, direction, is_alive, width, height)
      self.is_alive = is_alive
      P_shooter.all_p.push(self)

   def display(self, surf):
      self.sprite.update(1)
      self.sprite.display_animation(surf, 'p_shooter')

   def move(self):
      self.x += self.x_vel

   def update(self):
      #--if p_shooter not o the screen
      if self.is_on_screen(universal_names.screen_width, universal_names.screen_height) == False:
         self.is_alive = False
         if self not in P_shooter.all_p.lst:
            P_shooter.all_p.push(self)

      #--else
      if self.is_alive == True:
         self.move()
      Sprite_surface.update(self)
      pass

   @classmethod
   def fire(cls, x, y, speed):
      #--fires bullet by popping of the stack and changing some properties
      p = cls.all_p.pop()
      p.x, p.y = x, y
      p.is_alive = True
      p.x_vel = speed