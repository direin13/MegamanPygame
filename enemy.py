#!/usr/bin/env python

import universal_var
from sprite import *
import pygame
from character import *
from megaman import *
import camera
import p_shooter

class Enemy(Character):
   all_sprite_surfaces = []

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, display_layer=4, 
               gravity=False, direction=True, max_x_vel=0, health_points=100, damage_points=0):
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer, gravity, direction, max_x_vel, health_points)
      self.damage_points = damage_points
      self.health_points_copy = self.health_points
      self.all_timers.add_ID('explosion_animation', 13)
      self.can_spawn = False


   def respawn(self): #restoring everything
      x, y = self.spawn_point[0], self.spawn_point[1]
      if (x > 0 and x < universal_var.screen_width) and (y > 0 and y < universal_var.screen_height):
         self.x, self.y = x - self.width//2, y - self.height//2

         self.health_points = self.health_points_copy
         self.all_timers.replenish_timer('explosion_animation')
         self.can_spawn = False

   def check_bullet_contact(self, quota=None):
      collisions = self.check_collision_lst(p_shooter.P_shooter.all_p_lst, universal_var.hitbox, universal_var.hitbox, quota=quota)
      #print(collisions)
      return collisions

   def update(self):
      if camera.camera_transitioning() == True:
         self.is_active = False
         self.health_points = 0
         self.can_spawn = True
      elif universal_var.game_pause == True:
         pass
      else:

         if self.is_on_screen(universal_var.screen_width, universal_var.screen_height) and universal_var.game_reset != True:
            if self.is_alive():
               self.is_active = True
               self.move(-1, 0)
            else:
               self.all_timers.countdown('explosion_animation')
         else:
            self.is_active = False #respawn if offscreen
            self.health_points = 0


         if self.is_alive() != True:
            x, y = self.spawn_point[0], self.spawn_point[1]
            if self.can_spawn == True:
               self.respawn()

            elif (x < 0 or x > universal_var.screen_width) or (y < 0 or y > universal_var.screen_height): #if spawn point is off screen
               self.can_spawn = True

         if self.all_timers.is_empty('explosion_animation'): #explosion when enemy dies
            self.is_active = False
      Sprite_surface.update(self)


class Met(Enemy):
   def __init__(self, ID, x, y, display_layer=4):
      max_x_vel = 0
      direction = False
      health_points = 10
      damage_points = 20
      gravity = False
      is_active = True
      idle_enemy = [universal_var.enemies['met_2']]
      explosion_enemy = [universal_var.effect_images['explosion_1'], universal_var.effect_images['explosion_2'], universal_var.effect_images['explosion_3']]
      met = Sprite(universal_var.main_sprite, 200, 200, 40, 30, [('idle', idle_enemy, 1),
                                                                            ('explosion', explosion_enemy, 15)])
      met_hit_box = Collision_box(universal_var.hitbox, 400, 290, 36, 30, (240, 240, 0), x_offset=2)

      super().__init__(ID, x, y, [met], [met_hit_box], is_active, 40, 30, display_layer, gravity, direction, max_x_vel, health_points, damage_points)
      Enemy.add_to_class_lst(self, Enemy.all_sprite_surfaces, ID)
      Enemy.add_to_class_lst(self, Megaman_object.hazards, ID)

   def display(self, surf):
      if self.is_alive():
         Megaman_object.display(self, surf)
      else:
         self.update_sprite(universal_var.main_sprite)
         self.display_animation(universal_var.main_sprite, surf, 'explosion')

   def update(self):
      pshooter_collisions = self.check_bullet_contact(quota=1)
      if pshooter_collisions.is_empty() != True and self.is_alive():
         p = pshooter_collisions.pop()
         self.reduce_hp(p.damage_points)
         p.is_active = False
         play_sound('impact_p', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume - 0.1)

      Enemy.update(self)


class Lasor(Megaman_object):
   def __init__(self, ID, x, y, start_offset, x_vel):
      width = 1400
      height = 42
      img = Sprite(universal_var.main_sprite, 0, 0, width, height, [('idle', [universal_var.effect_images['lasor']], 1)])
      sprites = [img]
      is_active = False
      coll_boxes = [Collision_box(universal_var.hitbox, 0, 0, width, height, (240, 240, 0))]
      display_layer = 2
      gravity = False
      direction = False
      max_x_vel = x_vel
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer, gravity, direction, max_x_vel)
      self.all_timers.add_ID('start_offset', start_offset)
      self.x = x
      self.y = y
      self.x_vel = x_vel
      self.damage_points = 1000000
      self.lasor_sound = True
      Lasor.add_to_class_lst(self, Enemy.all_sprite_surfaces, ID)
      Lasor.add_to_class_lst(self, Megaman_object.hazards, ID)      


   def is_alive(self):
      return self.is_active

   def respawn(self): #restoring everything
      self.x, self.y = self.spawn_point[0], self.spawn_point[1]
      for t in self.all_timers:
         self.all_timers.replenish_timer(t)
      self.lasor_sound = True

   def update(self):
      if camera.camera_transitioning() == True or universal_var.game_pause == True or universal_var.debug == True:
         pass
      else:
         if (self.y + self.height > 0) and (self.y < universal_var.screen_height):
            self.all_timers.countdown('start_offset')

         if self.all_timers.is_empty('start_offset'):
            self.is_active = True
            if (self.x_vel >= 0 and self.x + self.width <= universal_var.screen_width) or (self.x_vel < 0 and self.x > 0):
               self.move(self.x_vel)
            if self.lasor_sound == True:
               play_sound('lasor', universal_var.megaman_sounds, channel=3, volume=universal_var.sfx_volume)
               self.lasor_sound = False

      Sprite_surface.update(self)