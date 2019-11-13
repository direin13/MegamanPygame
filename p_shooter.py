#!/usr/bin/env python
import pygame
from sprite import *
import mega_stack
import universal_names
from misc_function import *
from megaman_object import *

class P_shooter(Megaman_object):
   all_p = mega_stack.Stack() #the stack acts as ammo source
   x_vel = 8

   def __init__(self, ID, x, y, sprite=None, coll_boxes=None, gravity=False, x_vel=0, y_vel=0, direction=True, width=1, height=1, is_alive=False):
      sprite = Sprite(x, y, 30, 18, [('p_shooter', [universal_names.megaman_images['p_shooter']])])
      coll_boxes = [Collision_box(universal_names.hitbox, x, y, 30, 18)]
      super().__init__(ID, x, y, sprite, coll_boxes, gravity, x_vel, y_vel, direction, is_alive, width, height)
      self.is_alive = is_alive
      P_shooter.all_p.push(self)

   def display(self, surf):
      self.sprite.update(1)
      self.sprite.display_animation(surf, 'p_shooter')

   def move(self):
      self.x += self.x_vel

   def sprite_surf_check(self):
      self.check_platform()

   def check_platform(self):
      for platform in Platform.all_sprite_surfaces.values():
         if platform.is_on_screen(universal_names.screen_width,universal_names.screen_height) == True:
            if self.check_collision(platform, universal_names.hitbox, universal_names.hitbox) == True:
               self.is_alive = False
               play_sound('impact_p', universal_names.megaman_sounds, channel=1, volume=universal_names.sfx_volume)
               break
            pass

   def refill(self):
      if self.is_on_screen(universal_names.screen_width, universal_names.screen_height) == False:
         self.is_alive = False
      if self.is_alive == False:
         if self not in P_shooter.all_p.lst:
            P_shooter.all_p.push(self)

   def update(self):
      #--if p_shooter not o the screen
      self.refill()
      #--else
      if self.is_alive == True:
         self.sprite_surf_check()
         self.move()
      Sprite_surface.update(self)

   @classmethod
   def fire(cls, x, y, speed):
      #--fires bullet by popping of the stack and changing some properties
      p = cls.all_p.pop()
      p.x, p.y = x, y
      Sprite_surface.update(p)
      p.is_alive = True
      p.x_vel = speed

for i in range(0, 3): #--making p_shooter bullets
         P_shooter('p_shooter', 0, 0)
