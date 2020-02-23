#!/usr/bin/env python

import universal_var
from sprite import *
import pygame
from character import *
import megaman
import camera
import p_shooter
import projectile

class Enemy(Character):
   all_sprite_surfaces = []

   def __init__(self, ID, x, y, sprites=None, coll_boxes=None, is_active=True, width=0, height=0, display_layer=4, 
               gravity=False, direction=True, max_x_vel=0, health_points=100, damage_points=0, x_clip_offset=0, y_clip_offset=0):
      super().__init__(ID, x, y, sprites, coll_boxes, is_active, width, height, display_layer, gravity, direction, max_x_vel, health_points)
      self.damage_points = damage_points
      self.health_points_copy = self.health_points
      self.x_clip_offset = x_clip_offset
      self.y_clip_offset = y_clip_offset
      self.can_spawn = False
      self.all_timers.add_ID('explosion_animation', 12)

   def respawn(self): #restoring everything
      x, y = self.spawn_point[0], self.spawn_point[1]
      if (x > 0 and x < universal_var.screen_width + self.x_clip_offset) and (y > 0 and y < universal_var.screen_height + self.y_clip_offset):
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

         if (self.is_on_screen(universal_var.screen_width + self.x_clip_offset, universal_var.screen_height + self.y_clip_offset) 
            and universal_var.game_reset != True):
            if self.is_alive():
               self.is_active = True
            else:
               self.all_timers.countdown('explosion_animation')
         else:
            self.is_active = False #respawn if offscreen
            self.health_points = 0


         if self.is_alive() != True:
            x, y = self.spawn_point[0], self.spawn_point[1]
            if self.can_spawn == True and self.is_active != True:
               self.respawn()

            elif (x < 0 or x > universal_var.screen_width) or (y < 0 or y > universal_var.screen_height): #if spawn point is off screen
               self.can_spawn = True

         if self.all_timers.is_empty('explosion_animation'): #explosion when enemy dies
            self.is_active = False
      Sprite_surface.update(self)

#-----------------------------------------------------------

class Met(Enemy):
   def __init__(self, ID, x, y, direction, trigger_width, trigger_height):
      width = 40
      height = 35
      display_layer = 4
      max_x_vel = 0
      direction = direction
      health_points = 10
      damage_points = 20
      gravity = False
      is_active = True
      x_clip_offset, y_clip_offset = 0, 0
      idle_animation = [universal_var.enemies['met_1']]
      shoot_animation = [universal_var.enemies['met_2']]
      explosion_enemy = [universal_var.effect_images['explosion_1'], universal_var.effect_images['explosion_2'], 
                         universal_var.effect_images['explosion_3']]

      met = Sprite(universal_var.main_sprite, 200, 200, width, height, [('idle', idle_animation, 1),
                                                                        ('shoot', shoot_animation, 1),
                                                                        ('explosion', explosion_enemy, 12)])

      main_collbox = Collision_box(universal_var.hitbox, 400, 290, 34, 30, (240, 240, 0), x_offset=4)
      trigger_box = Collision_box('trigger_box', 0, 0, trigger_width * 2, trigger_height * 2, (240, 140, 20), x_offset=-trigger_width + (width//2),
                                  y_offset=-trigger_height + (height//2))

      super().__init__(ID, x, y, [met], [main_collbox, trigger_box], is_active, width, height, display_layer, gravity, direction, max_x_vel, health_points, 
                       damage_points, x_clip_offset, y_clip_offset)

      self.shooting_phase = False
      Enemy.add_to_class_lst(self, Enemy.all_sprite_surfaces, ID)
      Enemy.add_to_class_lst(self, Megaman_object.hazards, ID)
      self.all_timers.add_ID('shoot', 40)
      self.all_timers.add_ID('idle_wait', 180)
      for i in range(3):
         projectile.Enemy_projectile_1(self.x, self.y, 17)


   def respawn(self):
      for timer in self.all_timers:
         self.all_timers.replenish_timer(timer)

      self.shooting_phase = False
      Enemy.respawn(self)

   def display(self, surf):
      self.update_sprite(universal_var.main_sprite, game_pause=True)
      if self.is_alive() and self.shooting_phase:
         if self.direction == False:
            self.display_animation(universal_var.main_sprite, surf, 'shoot')
         else:
            self.display_animation(universal_var.main_sprite, surf, 'shoot', flip=True)

      elif self.is_alive():
         if self.direction == False:
            self.display_animation(universal_var.main_sprite, surf, 'idle')
         else:
            self.display_animation(universal_var.main_sprite, surf, 'idle', flip=True)

      else:
         self.display_animation(universal_var.main_sprite, surf, 'explosion')

   def update(self):
      if self.is_active and universal_var.game_pause != True and universal_var.game_reset != True:
         megaman_collision = self.check_collision_lst(megaman.Megaman.all_sprite_surfaces, 'trigger_box', universal_var.hitbox)
         if megaman_collision.is_empty() != True:
            m = megaman_collision.pop()
            self.shooting_phase = True

         wait_interval = False
         if self.all_timers.is_empty('shoot') != True and self.shooting_phase:
            if self.all_timers.is_full('shoot') and m.x > self.x:
               self.direction = True
            elif self.all_timers.is_full('shoot') and m.x <= self.x:
               self.direction = False
            else:
               self.direction = self.direction

            if self.all_timers.is_full('shoot'):
               play_sound('det_fire', universal_var.megaman_sounds, channel=4, volume=universal_var.sfx_volume - 0.3)
               if self.direction == False:
                  vel = -30
               else:
                  vel = 30

               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=vel, angle=45)
               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=vel, angle=0)
               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=vel, angle=315)

            self.all_timers.replenish_timer('idle_wait')
            self.all_timers.countdown('shoot')

         else:
            self.shooting_phase = False
            wait_interval = True

         if wait_interval:
            if self.all_timers.is_empty('idle_wait') != True:
               self.all_timers.countdown('idle_wait')
            else:
               self.all_timers.replenish_timer('shoot')

         pshooter_collisions = self.check_bullet_contact(quota=1)
         if pshooter_collisions.is_empty() != True and self.is_alive():
            p = pshooter_collisions.pop()
            if self.shooting_phase and p.reflected == False:
               self.reduce_hp(p.damage_points)
               p.is_active = False
               p.launched = False
               play_sound('impact_p', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume - 0.1)
            elif wait_interval and p.reflected == False:
               if p.x < self.x:
                  projectile.Projectile.set(p, p.x, p.y, vel=90, angle=130)
               else:
                  projectile.Projectile.set(p, p.x, p.y, vel=90, angle=70)
               p.reflected = True
               play_sound('p_reflected', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume + 0.1)

      Enemy.update(self)

#----------------------------------------------------------

class Lasor(Megaman_object):
   def __init__(self, ID, x, y, start_offset, x_vel):
      width = 1400
      height = 42
      img = Sprite(universal_var.main_sprite, 0, 0, width, height, [('idle', [universal_var.effect_images['lasor']], 1)])
      sprites = [img]
      is_active = False
      main_collbox = Collision_box(universal_var.hitbox, 0, 0, width, height, (240, 240, 0))

      display_layer = 2
      gravity = False
      direction = False
      max_x_vel = x_vel
      super().__init__(ID, x, y, sprites, [main_collbox], is_active, width, height, display_layer, gravity, direction, max_x_vel)
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

#----------------------------------------------

class Detarnayappa(Enemy):
   def __init__(self, ID, x, y, start_time, time_to_apex, trigger_width, trigger_height):
      width = 50
      height = 38
      max_x_vel = 0
      direction = False
      gravity = False
      is_active = True
      display_layer = 4
      health_points = 10
      damage_points = 20
      x_clip_offset, y_clip_offset = 0, 50

      idle_animation = [universal_var.enemies['Detarnayappa_2'], universal_var.enemies['Detarnayappa_1']]
      shoot_animation = [universal_var.enemies['Detarnayappa_2'], universal_var.enemies['Detarnayappa_3']]
      explosion_enemy = [universal_var.effect_images['explosion_1'], universal_var.effect_images['explosion_2'], 
                         universal_var.effect_images['explosion_3']]

      sprites = Sprite(universal_var.main_sprite, 200, 200, width, height, [('idle', idle_animation, 20),
                                                                            ('shoot', shoot_animation, 15),
                                                                            ('explosion', explosion_enemy, 12)])

      main_coll_box = Collision_box(universal_var.hitbox, 0, 0, width, height, (240, 240, 0))
      trigger_box = Collision_box('trigger_box', 0, 0, trigger_width * 2, trigger_height * 2, (240, 140, 20), x_offset=-trigger_width + (width//2),
                                  y_offset=-trigger_height + (height//2))

      super().__init__(ID, x, y, [sprites], [main_coll_box, trigger_box], is_active, width, height, display_layer, gravity, direction, max_x_vel, 
                       health_points, damage_points, x_clip_offset, y_clip_offset)

      self.can_shoot = True
      Enemy.add_to_class_lst(self, Enemy.all_sprite_surfaces, ID)
      Enemy.add_to_class_lst(self, Megaman_object.hazards, ID)
      self.all_timers.add_ID('start_time', start_time)
      self.all_timers.add_ID('time_to_apex', time_to_apex)
      self.all_timers.add_ID('interval_frequency', 80)
      self.all_timers.add_ID('stop_time', 30)
      for i in range(2):
         projectile.Enemy_projectile_1(self.x, self.y)


   def display(self, surf):
      if self.is_alive():
         if self.all_timers.is_full('stop_time') or self.all_timers.is_empty('stop_time'):
            self.update_sprite(universal_var.main_sprite, game_pause=True, auto_reset=False)
            self.display_animation(universal_var.main_sprite, surf, 'idle')
         else:
            self.update_sprite(universal_var.main_sprite, game_pause=True, auto_reset=True)
            self.display_animation(universal_var.main_sprite, surf, 'shoot')
      else:
         self.update_sprite(universal_var.main_sprite, game_pause=True, auto_reset=False)
         self.display_animation(universal_var.main_sprite, surf, 'explosion')

   def respawn(self):
      Enemy.respawn(self)
      for timer in self.all_timers:
         self.all_timers.replenish_timer(timer)


   def update(self):
      pshooter_collisions = self.check_bullet_contact(quota=1)
      if pshooter_collisions.is_empty() != True and self.is_alive(): #if shot
         p = pshooter_collisions.pop()
         if p.reflected == False:
            self.reduce_hp(p.damage_points)
            p.is_active = False
            p.launched = False
            play_sound('impact_p', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume - 0.1)

      init, apex_reached = False, False
      if self.is_alive() and universal_var.game_pause != True:
         megaman_collision = self.check_collision_lst(megaman.Megaman.all_sprite_surfaces, 'trigger_box', universal_var.hitbox)
         if self.all_timers.is_empty('start_time'):
            init = True
         else:
            if megaman_collision.is_empty() != True: #once megaman in trigger box then timer to start will begin
               self.all_timers.countdown('start_time')

      if init:
         if self.all_timers.is_empty('time_to_apex'):
            apex_reached = True
         else:
            self.move(y_vel=-6)
            self.can_shoot = True
            self.all_timers.countdown('time_to_apex')

      if apex_reached:
         if self.all_timers.is_empty('stop_time') != True:
            self.all_timers.countdown('stop_time')
            if self.can_shoot:
               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=50, angle=0)
               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=50, angle=180)
               play_sound('det_fire', universal_var.megaman_sounds, channel=4, volume=universal_var.sfx_volume - 0.3)
               self.can_shoot = False

         elif self.all_timers.is_empty('interval_frequency') != True:
            self.all_timers.countdown('interval_frequency')
            self.move(y_vel=3)

         else:
            self.all_timers.replenish_timer('interval_frequency')
            self.all_timers.replenish_timer('stop_time')
            self.can_shoot = True

      Enemy.update(self)
