#!/usr/bin/env python
import pygame
from sprite import *
import mega_stack
import universal_names
from misc_function import *
from megaman_object import *
from enemy import *

class P_shooter(Megaman_object):
   all_p = mega_stack.Stack() #the stack acts as ammo source
   x_vel = 9

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=False, width=28, height=16, display_layer=3, gravity=False, direction=True, max_x_vel=0):
      sprites = [Sprite(universal_names.main_sprite, x, y, width, height, [('p_shooter', [universal_names.megaman_images['p_shooter']], 1)])]
      coll_boxes = [Collision_box(universal_names.hitbox, x, y, width, height)]
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer, gravity, direction, max_x_vel)
      self.is_active = is_active
      self.damage_points = 10
      P_shooter.all_p.push(self)

   def display(self, surf):
      self.display_animation(universal_names.main_sprite, surf, 'p_shooter')

   def move(self):
      self.x += self.x_vel

   def sprite_surf_check(self):
      self.check_enemy()

   def damage_enemy(self, ):
      pass

   def check_enemy(self):
      collisions = self.check_collision_lst(Enemy.all_sprite_surfaces, universal_names.hitbox, universal_names.hitbox)
      if collisions.is_empty() != True:
         enemy = collisions.pop()
         enemy.reduce_hp(self.damage_points)
         self.is_active = False
         play_sound('impact_p', universal_names.megaman_sounds, channel=1, volume=universal_names.sfx_volume - 0.1)


   def refill(self):
      if self.is_on_screen(universal_names.screen_width, universal_names.screen_height) == False:
         self.is_active = False
      if self.is_active == False:
         if self not in P_shooter.all_p.lst:
            P_shooter.all_p.push(self)

   def update(self):
      #--if p_shooter not o the screen
      self.refill()
      #--else
      if self.is_active == True:
         self.sprite_surf_check()
         self.move()
      Sprite_surface.update(self)

   @classmethod
   def fire(cls, x, y, speed):
      #--fires bullet by popping of the stack and changing some properties
      p = cls.all_p.pop()
      p.x, p.y = x, y
      Sprite_surface.update(p)
      p.is_active = True
      p.x_vel = speed

for i in range(0, 3): #--making p_shooter bullets
         P_shooter('p_shooter', 0, 0)
