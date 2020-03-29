#!/usr/bin/env python

import universal_var
from sprite import *
import pygame
from character import *
import megaman
import camera
import p_shooter
import projectile
import mega_stack
from misc_function import load_images
from items import Item

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
      self.explosion_timers = timer.Timer()
      self.explosion_dict = {}
      self.all_timers.add_ID('explosion_animation', 14)
      self.all_timers.add_ID('no_display', 7)
      self.all_explosion_ID_index = 0

   def add_explosion_animation(self, time_offset=0, width=0, height=0, x_offset=0, y_offset=0):
      ID = 'explosion-{}'.format(self.all_explosion_ID_index)
      self.all_explosion_ID_index += 1
      self.explosion_timers.add_ID(ID, time_offset)
      explosion_img = [universal_var.misc_images['explosion_1'], universal_var.misc_images['explosion_2'], 
                       universal_var.misc_images['explosion_3'], universal_var.misc_images['explosion_4'], 
                       universal_var.misc_images['explosion_5'], universal_var.misc_images['blank']]

      sprite = Sprite(universal_var.main_sprite, self.x, self.y, width, height, [('explosion', explosion_img, 12)])
      sprite_surf = Megaman_object(ID, self.x, self.y, [sprite], None, width=width, height=height, is_active=False, display_layer=3)
      sprite_surf.sprite_loop = False
      self.explosion_dict[ID] = [sprite_surf, (x_offset, y_offset)]


   def add_big_explosion(self, time_offset=0, x_offset=0, y_offset=0, width=50, height=50, radius=0):
      xy_offsets = [(5,5), 
                    (1-radius//1.5,1-radius//1.5), (9+radius//1.5,1-radius//1.5), (1-radius//1.5,9+radius//1.5), (9+radius//1.5,9+radius//1.5), 
                    (-1-radius,5), (5,-1-radius), (11+radius,5), (5, 11+radius)]

      explosion_time_offsets = [5, 10, 10, 10, 10, 15, 15, 15, 15]
      for i in range(9):
         self.add_explosion_animation(time_offset=explosion_time_offsets[i] + time_offset, width=width, height=height, 
                                      x_offset=xy_offsets[i][0] + x_offset, y_offset=xy_offsets[i][1] + y_offset)

   def display_explosions(self, surf):
      all_finished = True
      for timer in self.explosion_timers:
         if self.explosion_timers.is_finished(timer) != True:
            self.explosion_timers.countdown(timer)
            all_finished = False
         else:
            sprite_surf = self.explosion_dict[timer][0]
            x_offset, y_offset = self.explosion_dict[timer][1][0], self.explosion_dict[timer][1][1]
            sprite_surf.x, sprite_surf.y = self.x + x_offset, self.y + y_offset
            Sprite_surface.update(sprite_surf)

            sprite = sprite_surf.get_sprite(universal_var.main_sprite)
            if sprite.current_frame != len(sprite.get_frames(sprite.current_animation)) - 1:
               if self.is_active == False:
                  sprite_surf.is_active = False
               else:
                  sprite_surf.is_active = True
               all_finished = False

      if all_finished:
         for timer in self.explosion_timers:
            self.explosion_timers.replenish_timer(timer)
            sprite_surf = self.explosion_dict[timer][0]
            sprite_surf.is_active = False
            sprite = sprite_surf.get_sprite(universal_var.main_sprite)
            sprite.current_frame = 0
         self.is_active = False
            


   def respawn(self): #restoring everything
      x, y = self.spawn_point[0], self.spawn_point[1]
      if ((x > 0 - self.x_clip_offset and x < universal_var.screen_width + self.x_clip_offset) and 
         (y > 0 - self.y_clip_offset and y < universal_var.screen_height + self.y_clip_offset)):
         self.x, self.y = x - self.width//2, y - self.height//2

         self.health_points = self.health_points_copy
         self.can_spawn = False

   def check_pshooter_contact(self, reflect=False, drop_item=True, randint_drop_offset=0):
      collision = False
      pshooter_collisions = self.check_collision_lst(p_shooter.P_shooter.all_p_lst, universal_var.hitbox, universal_var.hitbox, quota=1)

      if pshooter_collisions.is_empty() != True and self.is_alive():
         collision = True
         p = pshooter_collisions.pop()
         if p.reflected == False and reflect == False:
            self.reduce_hp(p.damage_points)
            p.is_active = False
            p.launched = False
            play_sound('impact_p', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.1)
            if self.is_alive() and self.all_timers.is_finished('no_display'):
                  self.all_timers.replenish_timer('no_display')
            elif drop_item == True and self.is_alive() == False:
               Item.drop_item(self.x+self.width//2, self.y+self.height//2, randint_drop_offset)


         elif p.reflected == False:
            if p.x < self.x:
               projectile.Projectile.set(p, p.x, p.y, vel=90, angle=130)
            else:
               projectile.Projectile.set(p, p.x, p.y, vel=90, angle=70)
            p.reflected = True
            play_sound('p_reflected', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume + 0.1)

      return collision

   def update(self):
      if camera.camera_transitioning() == True or universal_var.game_reset:
         self.is_active = False
         self.health_points = 0
         self.can_spawn = True
      elif universal_var.game_pause == True:
         pass
      else:
         if (self.is_on_screen(universal_var.screen_width, universal_var.screen_height, self.x_clip_offset, self.y_clip_offset) 
            and universal_var.game_reset != True):
            if self.is_alive():
               self.is_active = True
         else:
            self.is_active = False #respawn if offscreen
            self.health_points = 0


         if self.is_alive() != True:
            x, y = self.spawn_point[0], self.spawn_point[1]
            if self.can_spawn == True and self.is_active != True:
               self.respawn()

            elif (x < 0 or x > universal_var.screen_width) or (y < 0 or y > universal_var.screen_height): #if spawn point is off screen
               self.can_spawn = True

      Sprite_surface.update(self)



#---------------------------------------------------------------------------------------------------------------



class Met(Enemy):
   sprite_img = load_images('resources/enemies/met')
   def __init__(self, ID, x, y, direction, trigger_width, trigger_height):
      width = 40
      height = 35
      display_layer = 4
      max_x_vel = 0
      direction = direction
      health_points = 10
      damage_points = 20
      gravity = False
      is_active = False
      x_clip_offset, y_clip_offset = 0, 0
      idle_animation = [Met.sprite_img['met_1']]
      shoot_animation = [Met.sprite_img['met_2']]

      met = Sprite(universal_var.main_sprite, 200, 200, width, height, [('idle', idle_animation, 1),
                                                                        ('shoot', shoot_animation, 1)])

      main_collbox = Collision_box(universal_var.hitbox, 400, 290, 34, 30, (240, 240, 0), x_offset=4)
      trigger_box = Collision_box('trigger_box', 0, 0, trigger_width * 2, trigger_height * 2, (240, 140, 20), x_offset=-trigger_width + (width//2),
                                  y_offset=-trigger_height + (height//2))

      super().__init__(ID, x, y, [met], [main_collbox, trigger_box], is_active, width, height, display_layer, gravity, direction, max_x_vel, health_points, 
                       damage_points, x_clip_offset, y_clip_offset)

      self.shooting_phase = False
      self.add_explosion_animation(time_offset=0, width=50, height=50, x_offset=0, y_offset=0)
      Enemy.add_to_class_lst(self, Enemy.all_sprite_surfaces, ID)
      Enemy.add_to_class_lst(self, Megaman_object.hazards, ID)
      self.all_timers.add_ID('open_up', 40)
      self.all_timers.add_ID('time_till_shoot', 20)
      self.all_timers.add_ID('idle_wait', 180)
      for i in range(3):
         projectile.Enemy_projectile_1(self.x, self.y, 17)


   def respawn(self):
      for timer in self.all_timers:
         self.all_timers.replenish_timer(timer)

      self.shooting_phase = False
      Enemy.respawn(self)

   def display(self, surf):
      if universal_var.game_pause != True:
         self.update_sprite(universal_var.main_sprite)
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
         self.display_explosions(surf)

   def update(self):
      if self.is_active and universal_var.game_pause != True and universal_var.game_reset != True:
         megaman_collision = self.check_collision_lst(megaman.Megaman.all_sprite_surfaces, 'trigger_box', universal_var.hitbox)
         if megaman_collision.is_empty() != True:
            m = megaman_collision.pop()
            self.shooting_phase = True

         wait_interval = False
         if self.all_timers.is_finished('open_up') != True and self.shooting_phase:
            if self.all_timers.is_full('open_up') and m.x > self.x:
               self.direction = True
            elif self.all_timers.is_full('open_up') and m.x <= self.x:
               self.direction = False
            else:
               self.direction = self.direction

            if self.all_timers.is_finished('time_till_shoot') != True:
               self.all_timers.countdown('time_till_shoot')

            if self.all_timers.get_ID('time_till_shoot')['curr_state'] == 1 and self.is_alive():
               play_sound('det_fire', universal_var.megaman_sounds, channel=4, volume=universal_var.sfx_volume - 0.3)
               if self.direction == False:
                  vel = -20
               else:
                  vel = 20

               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=vel, angle=45)
               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=vel, angle=0)
               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=vel, angle=315)

            self.all_timers.replenish_timer('idle_wait')
            self.all_timers.countdown('open_up')

         else:
            self.shooting_phase = False
            wait_interval = True

         if wait_interval:
            if self.all_timers.is_finished('idle_wait') != True:
               self.all_timers.countdown('idle_wait')
            else:
               self.all_timers.replenish_timer('open_up')
               self.all_timers.replenish_timer('time_till_shoot')

         if wait_interval:
            self.check_pshooter_contact(True, True)
         elif self.shooting_phase:
            self.check_pshooter_contact(False, True, 70)

      Enemy.update(self)



#--------------------------------------------------------------------------------------------------



class Lasor(Megaman_object):
   def __init__(self, ID, x, y, start_offset, x_vel):
      width = 1400
      height = 42
      img = Sprite(universal_var.main_sprite, 0, 0, width, height, [('idle', [universal_var.misc_images['lasor']], 1)])
      is_active = False
      main_collbox = Collision_box(universal_var.hitbox, 0, 0, width, height, (240, 240, 0))

      display_layer = 2
      gravity = False
      direction = False
      max_x_vel = x_vel
      super().__init__(ID, x, y, [img], [main_collbox], is_active, width, height, display_layer, gravity, direction, max_x_vel)
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

         if self.all_timers.is_finished('start_offset'):
            self.is_active = True
            if (self.x_vel >= 0 and self.x + self.width <= universal_var.screen_width) or (self.x_vel < 0 and self.x > 0):
               self.move(self.x_vel)
            if self.lasor_sound == True:
               play_sound('lasor', universal_var.megaman_sounds, channel=3, volume=universal_var.sfx_volume)
               self.lasor_sound = False

      Sprite_surface.update(self)



#---------------------------------------------------------------------------------------------------------



class Detarnayappa(Enemy):
   sprite_img = load_images('resources/enemies/detarnayappa')
   def __init__(self, ID, x, y, start_time, time_to_apex, trigger_width, trigger_height):
      width = 50
      height = 38
      max_x_vel = 0
      direction = False
      gravity = False
      is_active = False
      display_layer = 4
      health_points = 10
      damage_points = 20
      x_clip_offset, y_clip_offset = 0, 50

      idle_animation = [Detarnayappa.sprite_img['Detarnayappa_2'], Detarnayappa.sprite_img['Detarnayappa_1']]
      shoot_animation = [Detarnayappa.sprite_img['Detarnayappa_2'], Detarnayappa.sprite_img['Detarnayappa_3']]

      sprites = Sprite(universal_var.main_sprite, 200, 200, width, height, [('idle', idle_animation, 20),
                                                                            ('shoot', shoot_animation, 15)
                                                                           ])

      main_coll_box = Collision_box(universal_var.hitbox, 0, 0, width, height, (240, 240, 0))
      trigger_box = Collision_box('trigger_box', 0, 0, trigger_width * 2, trigger_height * 2, (240, 140, 20), x_offset=-trigger_width + (width//2),
                                  y_offset=-trigger_height + (height//2))

      super().__init__(ID, x, y, [sprites], [main_coll_box, trigger_box], is_active, width, height, display_layer, gravity, direction, max_x_vel, 
                       health_points, damage_points, x_clip_offset, y_clip_offset)

      self.can_shoot = True
      self.add_explosion_animation(time_offset=0, width=50, height=50, x_offset=0, y_offset=0)
      Enemy.add_to_class_lst(self, Enemy.all_sprite_surfaces, ID)
      Enemy.add_to_class_lst(self, Megaman_object.hazards, ID)
      self.init = False
      self.all_timers.add_ID('start_time', start_time)
      self.all_timers.add_ID('time_to_apex', time_to_apex)
      self.all_timers.add_ID('interval_frequency', 80)
      self.all_timers.add_ID('stop_time', 30)
      for i in range(2):
         projectile.Enemy_projectile_1(self.x, self.y)


   def display(self, surf):
      if self.all_timers.is_full('stop_time') or self.all_timers.is_finished('stop_time') and universal_var.game_pause != True:
         self.update_sprite(universal_var.main_sprite, auto_reset=False)
      elif universal_var.game_pause != True:
         self.update_sprite(universal_var.main_sprite, auto_reset=True)

      if self.is_alive():
         if self.all_timers.is_full('stop_time') or self.all_timers.is_finished('stop_time'):
            self.display_animation(universal_var.main_sprite, surf, 'idle')
         else:
            self.display_animation(universal_var.main_sprite, surf, 'shoot')
      else:
         self.display_explosions(surf)

   def respawn(self):
      Enemy.respawn(self)
      for timer in self.all_timers:
         self.all_timers.replenish_timer(timer)
      self.get_sprite(universal_var.main_sprite).current_frame = 1


   def update(self):
      self.check_pshooter_contact(False, True, 80)

      spawned, apex_reached = False, False
      if self.is_alive() and universal_var.game_pause != True:
         megaman_collision = self.check_collision_lst(megaman.Megaman.all_sprite_surfaces, 'trigger_box', universal_var.hitbox)
         if self.all_timers.is_finished('start_time'):
            spawned = True
         else:
            if megaman_collision.is_empty() != True: #once megaman in trigger box then timer to start will begin
               self.all_timers.countdown('start_time')
               if self.init == False:
                  self.init = True
                  self.all_timers.get_ID('start_time')['curr_state'] = 20

      if spawned:
         if self.all_timers.is_finished('time_to_apex'):
            apex_reached = True
         else:
            self.move(y_vel=-6)
            self.can_shoot = True
            self.all_timers.countdown('time_to_apex')

      if apex_reached:
         if self.all_timers.is_finished('stop_time') != True:
            self.all_timers.countdown('stop_time')
            if self.can_shoot:
               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=40, angle=0)
               projectile.Enemy_projectile_1.set(self.x + self.width//2, self.y + 5, vel=40, angle=180)
               play_sound('det_fire', universal_var.megaman_sounds, channel=4, volume=universal_var.sfx_volume - 0.3)
               self.can_shoot = False

         elif self.all_timers.is_finished('interval_frequency') != True:
            self.all_timers.countdown('interval_frequency')
            self.move(y_vel=3)

         else:
            self.all_timers.replenish_timer('interval_frequency')
            self.all_timers.replenish_timer('stop_time')
            self.can_shoot = True

      if universal_var.game_reset:
         self.init = False

      Enemy.update(self)



#-----------------------------------------------------------------------------------------------------



class Hoohoo(Enemy):
   sprite_img = load_images('resources/enemies/hoohoo')
   def __init__(self, ID, y, start_time, trigger_collbox):
      width = 55
      height = 45
      gravity = False
      display_layer = 4
      health_points = 10
      damage_points = 17
      gravity = False
      is_active = False
      direction = True
      max_x_vel = 4
      x = -90
      x_clip_offset, y_clip_offset = 145, 145

      idle_animation = [Hoohoo.sprite_img['hoohoo_1'], Hoohoo.sprite_img['hoohoo_2']]
      drop_animation = [Hoohoo.sprite_img['hoohoo_3']]

      hoohoo = Sprite(universal_var.main_sprite, x, y, width, height, [('flying', idle_animation, 20),
                                                                           ('boulder_drop', drop_animation, 20)])

      main_collbox = Collision_box(universal_var.hitbox, 400, 290, width, height, (240, 240, 0), x_offset=4)
      super().__init__(ID, x, y, [hoohoo], [main_collbox], is_active, width, height, display_layer, gravity, direction, max_x_vel, health_points, 
                       damage_points, x_clip_offset, y_clip_offset)

      self.add_explosion_animation(time_offset=0, width=50, height=50, x_offset=0, y_offset=0)
      self.y_copy = y
      self.x_copy = x
      self.trigger_box = trigger_collbox
      self.boulder = Hoohoo_boulder(self.x, self.y, 20)
      self.boulder_drop = False
      self.all_timers.add_ID('start_time', start_time)
      self.all_timers.add_ID('fly_up', 28)
      self.all_timers.add_ID('fly_down', 28)
      self.all_timers.add_ID('drop_boulder_animation', 15)
      Enemy.add_to_class_lst(self, Enemy.all_sprite_surfaces, ID)
      Enemy.add_to_class_lst(self, Megaman_object.hazards, ID)


   def respawn(self):
      Enemy.respawn(self)
      self.boulder_drop = False
      for timer in self.all_timers:
         self.all_timers.replenish_timer(timer)


   def display(self, surf):
      if universal_var.game_pause != True:
         self.update_sprite(universal_var.main_sprite, auto_reset=True)

      if self.is_alive():
         if self.direction == True:
            flip = True
         else:
            flip = False
            
         if self.boulder_drop and self.all_timers.is_finished('drop_boulder_animation') != True:
            self.display_animation(universal_var.main_sprite, surf, 'boulder_drop', flip=flip)
            self.all_timers.countdown('drop_boulder_animation')
         else:
            self.display_animation(universal_var.main_sprite, surf, 'flying', flip=flip)
      else:
         self.display_explosions(surf)



   def update(self):
      self.spawn_point[0], self.spawn_point[1] = self.x_copy, self.y_copy
      self.boulder.spawn_point[0], self.boulder.spawn_point[1] = self.x_copy, self.y_copy
      if self.boulder_drop == False:
         self.boulder.x, self.boulder.y = self.x + 5, self.y + self.height - 10
         self.boulder.spawn_point[0], self.boulder.spawn_point[1] = self.x + 5, self.y + self.height - 10

      init = False
      megaman_collision = self.trigger_box.check_collision_lst(megaman.Megaman.all_sprite_surfaces, universal_var.hitbox, universal_var.hitbox)

      if self.all_timers.is_finished('start_time') != True:
         if megaman_collision.is_empty() != True and universal_var.game_pause != True:
            self.all_timers.countdown('start_time')
            m = megaman_collision.pop()
            if m.direction == False:
               self.direction = True
               self.max_x_vel = 4
               self.x_copy = -90
            else:
               self.direction = False
               self.max_x_vel = -4
               self.x_copy = 690
         else:
            self.all_timers.replenish_timer('start_time')
         self.x = self.x_copy
      else:
         init = True

      if init and universal_var.game_pause != True and self.is_alive():
         if self.all_timers.is_finished('fly_down') != True:
            self.move(x_vel=self.max_x_vel, y_vel=2)
            self.all_timers.countdown('fly_down')
         elif self.all_timers.is_finished('fly_up') != True:
            self.move(x_vel=self.max_x_vel, y_vel=-2)
            self.all_timers.countdown('fly_up')
         else:
            self.all_timers.replenish_timer('fly_down')
            self.all_timers.replenish_timer('fly_up')

         if self.boulder_drop == False and self.boulder.is_alive():
            if (self.direction == False and self.x < 360) or (self.direction == True and self.x > 200):
               self.boulder.set(self.boulder.x, self.boulder.y, 20, 270, 9.8)
               self.boulder_drop = True

      if self.is_on_screen(universal_var.screen_width, universal_var.screen_height) and self.is_active and self.check_pshooter_contact(False, True, 80):
         self.boulder.reduce_hp(self.boulder.health_points)
         self.boulder.launched = False

      Enemy.update(self)


#------------------------------------------------------------------------------------------------



class Hoohoo_boulder(Enemy, projectile.Projectile):
   mini_boulder_1_stack = mega_stack.Stack()
   mini_boulder_2_stack = mega_stack.Stack()

   def __init__(self, x, y, damage_points=1):
      width = 40
      height = 40
      health_points = 10
      is_active = False
      display_layer = 2
      gravity = False
      direction = False
      x_clip_offset, y_clip_offset = 0, 0
      max_x_vel = 0

      boulder_sprite = Sprite(universal_var.main_sprite, x, y, width, height, [
                                                                                 ('boulder', [universal_var.projectiles['boulder_1']], 1)
                                                                              ])

      main_collbox = Collision_box(universal_var.hitbox, 0, 0, width, height, (60, 240, 0))

      super().__init__('boulder', x, y, [boulder_sprite], [main_collbox], is_active, width, height, display_layer, gravity, direction, max_x_vel,
                       health_points, damage_points, x_clip_offset, y_clip_offset)
      Hoohoo_boulder.add_to_class_lst(self, Megaman_object.hazards, self.ID)
      self.add_explosion_animation(time_offset=0, width=50, height=50, x_offset=0, y_offset=0)

      for i in range(2):
         mini_boulder_1_sprite = Sprite(universal_var.main_sprite, self.x, self.y, 20, 20, [
                                                                                            ('mini_boulder_1', [universal_var.projectiles['boulder_{}'.format(i+2)]], 1)
                                                                                            ])
         mini_boulder_1_collbox = Collision_box(universal_var.hitbox, self.x, self.y, 25, 25, (122,122,122))
         mini_boulder_1 = projectile.Projectile('mini_boulder_1', self.x, self.y, [mini_boulder_1_sprite], [mini_boulder_1_collbox], width=20, height=20)
         mini_boulder_1.damage_points = 12
         Hoohoo_boulder.mini_boulder_1_stack.push(mini_boulder_1)
         Hoohoo_boulder.add_to_class_lst(mini_boulder_1, Megaman_object.hazards, mini_boulder_1.ID)

      for i in range(3):
         mini_boulder_2_sprite = Sprite(universal_var.main_sprite, self.x, self.y, 10, 10, [('mini_boulder_2', [universal_var.projectiles['boulder_4']], 1)])
         mini_boulder_2 = projectile.Projectile('mini_boulder_2', self.x, self.y, [mini_boulder_2_sprite], width=10, height=10)
         Hoohoo_boulder.mini_boulder_2_stack.push(mini_boulder_2)


   def display(self, surf):
      if universal_var.game_pause != True:
         self.update_sprite(universal_var.main_sprite)

      if self.is_alive():
         self.display_animation(universal_var.main_sprite, surf, 'boulder')
      else:
         self.display_explosions(surf)

   def move(self, velocity, angle, gravity):
      projectile.Projectile.move(self, velocity, angle, gravity)

   def split(self): #breaks rock into pieces
      all_mini_boulders_1 = []
      all_mini_boulders_2 = []
      angles = [120, 83, 60, 107, 98]
      speeds = [33, 50, 33, 20, 33]
      for i in range(2):
         b1 = Hoohoo_boulder.mini_boulder_1_stack.pop()
         b1.set(self.x, self.y, speeds[i], angles[i], gravity=11.6)
         all_mini_boulders_1.append(b1)

      for i in range(2,5):
         b2 = Hoohoo_boulder.mini_boulder_2_stack.pop()
         b2.set(self.x, self.y, speeds[i], angles[i], gravity=10.6)
         all_mini_boulders_2.append(b2)

      for b in all_mini_boulders_1:
         Hoohoo_boulder.mini_boulder_1_stack.push_start(b)
      for b in all_mini_boulders_2:
         Hoohoo_boulder.mini_boulder_2_stack.push_start(b)


   def update(self):
      if self.is_active:
         if self.check_pshooter_contact(False, True, 80):
            self.launched = False

         if self.launched:
            ground_collision = self.check_collision_lst(Megaman_object.platforms, universal_var.hitbox, universal_var.hitbox, quota=1)
            if ground_collision.is_empty() != True:
               self.health_points -= self.health_points
               play_sound('boulder_break', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.3)
               self.split()
               self.launched = False

      Enemy.update(self)
      projectile.Projectile.update(self)


#-----------------------------------------------------------------------------------------------


class Paozo(Enemy):
   sprite_img = load_images('resources/enemies/paozo')

   def __init__(self, x, y, direction):
      width = 250
      height = 160
      is_active = False
      health_points = 200
      damage_points = 30
      max_x_vel = 0
      display_layer = 2
      gravity = False
      idle_animation = [Paozo.sprite_img['paozo_1']]
      ball_flip_animation = [Paozo.sprite_img['paozo_2'], Paozo.sprite_img['paozo_3']]
      vacuum_animation = [Paozo.sprite_img['paozo_vacuum_1'], Paozo.sprite_img['paozo_vacuum_2']]

      main_sprite = Sprite(universal_var.main_sprite, x, y, width, height, [
                                                                              ('idle', idle_animation, 13),
                                                                              ('ball_flip', ball_flip_animation, 13),
                                                                              ('vacuum', vacuum_animation, 10),
                                                                           ])

      main_collbox = Collision_box(universal_var.hitbox, x, y, width-80, height-20, (40, 80, 100), y_offset=20)
      super().__init__('paozo', x, y, [main_sprite], [main_collbox], is_active, width, height, display_layer, gravity, direction, max_x_vel, health_points, 
                       damage_points)

      respawn_obj_fall = [Paozo.sprite_img['paozo_spawn_1']]
      respawn_obj_collision = [Paozo.sprite_img['paozo_spawn_2'], Paozo.sprite_img['paozo_spawn_3']]
      respawn_obj_sprite = Sprite(universal_var.main_sprite, self.x + 50, self.y + 50, width=200, height=200, active_frames=[
                                                                                                                              ('falling', respawn_obj_fall, 1),
                                                                                                                              ('ground_collision', respawn_obj_collision, 10)
                                                                                                                            ])
      self.respawn_obj = Megaman_object('respawn', 0, 0, [respawn_obj_sprite], None, is_active=False, display_layer=3)
      self.ball = Paozo_Ball(self.x + 57, self.y)
      self.vacuum_mode = False
      self.vacuum_sound = False
      self.all_timers.add_ID('respawn_obj_collision', 10)
      self.all_timers.add_ID('phase_1_wait', 50)
      self.all_timers.add_ID('phase_2_flip_animation', 40)
      self.all_timers.add_ID('phase_3_begin', 90)
      self.all_timers.add_ID('no_display', 7)
      Paozo.add_to_class_lst(self, Megaman_object.hazards, self.ID)
      self.add_big_explosion(x_offset=130, y_offset=50, radius=38)
      self.add_big_explosion(time_offset=10, x_offset=50, y_offset=20, radius=38)

      invisible_wall = [Collision_box(universal_var.hitbox, 0, 0, 20, 600)]
      self.invisible_wall = Megaman_object('platform', 0, 0, sprites=None, coll_boxes=invisible_wall,
                  width=20, height=600, display_layer=5, is_active=False)

   def display(self, surf):
      if universal_var.game_pause != True:
         if self.all_timers.is_almost_finished('phase_3_begin', 30):
            self.update_sprite(universal_var.main_sprite)
         else:
            self.update_sprite(universal_var.main_sprite, auto_reset=False)

      if self.direction == True:
         flip = True
      else:
         flip = False
      if self.all_timers.is_finished('no_display') == True and self.is_alive():
         if self.vacuum_mode or self.all_timers.is_almost_finished('phase_3_begin', 30):
            self.display_animation(universal_var.main_sprite, surf, 'vacuum', flip=flip)
         elif self.all_timers.is_finished('phase_1_wait') != True or self.all_timers.is_finished('phase_2_flip_animation'):
            self.display_animation(universal_var.main_sprite, surf, 'idle', flip=flip)
         else:
            self.display_animation(universal_var.main_sprite, surf, 'ball_flip', flip=flip)
            self.all_timers.countdown('phase_2_flip_animation')
      elif self.is_alive() != True:
         self.display_explosions(surf)

   def respawn(self):
      if universal_var.game_pause != True and universal_var.game_reset != True and self.is_on_screen(universal_var.screen_width, universal_var.screen_height):
         if self.respawn_obj.is_active != True:
            self.respawn_obj.y = self.spawn_point[1] - 600
            self.respawn_obj.is_active = True
         elif (self.respawn_obj.y + self.respawn_obj.height) <= (self.spawn_point[1] - self.height + 30):
            self.respawn_obj.row = 0
            self.respawn_obj.x = self.spawn_point[0] - 120
            self.respawn_obj.is_active = True
            self.respawn_obj.move(0, 10)
         elif self.all_timers.is_finished('respawn_obj_collision') != True:
            self.respawn_obj.row = 1
            self.all_timers.countdown('respawn_obj_collision')
         else:
            self.ball.reset()
            Enemy.respawn(self)
            self.ball.health_points = 10
            self.ball.is_active = True
            self.ball.x = self.ball.spawn_point[0]
            self.respawn_obj.is_active = False
            self.vacuum_mode = False
            self.vacuum_sound = False
            self.invisible_wall.x, self.invisible_wall.y = 0, 0
            Megaman_object.add_to_class_lst(self.invisible_wall, Megaman_object.platforms, 
                                            self.invisible_wall.ID)
            self.invisible_wall.is_active = True
            for timer in self.all_timers:
               if timer != 'no_display':
                  self.all_timers.replenish_timer(timer)



   def update(self):
      if self.is_alive() != True:
         self.ball.health_points -= self.ball.health_points
         if self.invisible_wall.is_active:
            Megaman_object.platforms.remove(self.invisible_wall)
            self.invisible_wall.is_active = False

      elif universal_var.game_pause != True and universal_var.game_reset != True:
         if self.all_timers.is_finished('phase_1_wait') != True:
            self.all_timers.countdown('phase_1_wait')
         elif self.all_timers.is_full('phase_3_begin'):
            projectile.Projectile.set(self.ball, self.ball.x, self.ball.y, 40, 0)
            self.ball.thrown = True
            self.all_timers.countdown('phase_3_begin')
         else:
            if self.all_timers.is_finished('phase_3_begin') != True:
               self.all_timers.countdown('phase_3_begin')
            elif self.vacuum_mode != True:
               projectile.Projectile.set(self.ball, self.ball.x, self.ball.y, 40, 180)
               self.vacuum_mode = True

         if self.all_timers.is_almost_finished('phase_3_begin', 30):
            if self.vacuum_sound == False:
               play_sound('paozo_vacuum', universal_var.megaman_sounds, channel=3, volume=universal_var.sfx_volume - 0.3)
               self.vacuum_sound = True
            m = megaman.Megaman.all_sprite_surfaces[0]
            if m.is_active and m.is_alive():
               m.x -= 2

         if self.ball.x + self.ball.width >= universal_var.screen_width and self.vacuum_mode != True:
            self.ball.launched = False

         if self.ball.x <= self.ball.spawn_point[0] and self.ball.thrown and self.vacuum_mode:
            self.ball.launched = False
            self.ball.thrown = False
            self.ball.x = self.ball.spawn_point[0]
            self.vacuum_mode = False
            self.vacuum_sound = False
            for timer in self.all_timers:
               if timer != "no_display":
                  self.all_timers.replenish_timer(timer)

         if self.check_pshooter_contact(False, True, 30) and self.is_alive() == False:
            play_sound('big_explosion', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume - 0.3)

      self.all_timers.countdown('no_display')
      Enemy.update(self)


#--------------------------------------------------------------------------------------------------


class Paozo_Ball(Enemy):
   def __init__(self, x, y):
      width = 80
      height = 80
      is_active = False
      display_layer = 3
      ball_idle = [Paozo.sprite_img['paozo_ball_1']]
      ball_roll = [Paozo.sprite_img['paozo_ball_2'], Paozo.sprite_img['paozo_ball_3']]
      main_sprite = Sprite(universal_var.main_sprite, x, y, width, height, [
                                                                              ('ball_idle', ball_idle, 1),
                                                                              ('ball_roll', ball_roll, 6)
                                                                           ])
      main_collbox = Collision_box(universal_var.hitbox, x, y, width, height)
      super().__init__('paozo_ball', x, y, [main_sprite], [main_collbox], is_active, width, height, display_layer)
      projectile.Projectile.init_projectile_properties(self)
      self.add_big_explosion(x_offset=10, y_offset=10, radius=36)

      self.health_points = 10
      self.damage_points = 22
      self.thrown = False
      Paozo.add_to_class_lst(self, Megaman_object.hazards, self.ID)

   def reset(self):
      self.is_active = False
      self.launched = False
      self.thrown = False
      self.x, self.y = self.spawn_point[0], self.spawn_point[1]

   def display(self, surf):
      if universal_var.game_pause != True:
         self.update_sprite(universal_var.main_sprite)

      if self.is_alive():
         if self.thrown:
            self.display_animation(universal_var.main_sprite, surf, 'ball_roll')
         else:
            self.display_animation(universal_var.main_sprite, surf, 'ball_idle')
      else:
         self.display_explosions(surf)

   def is_alive(self):
      return self.health_points > 0

   def update(self):
      if self.is_alive():
         self.check_pshooter_contact(True, False)

         projectile.Projectile.update(self)
      elif self.is_on_screen(universal_var.screen_width, universal_var.screen_height) != True:
         self.is_active = False


#------------------------------------------------------------------------------------------


class Big_stomper(Enemy):
   sprite_img = load_images('resources/enemies/big_Stomper')

   def __init__(self, x, y, damage_points=20):
      width = 65
      height = 130
      display_layer = 3
      is_active = False
      health_points = 110
      direction = False
      max_x_vel = 2
      gravity = True
      x_clip_offset, y_clip_offset = 0, 0

      idle_high = [Big_stomper.sprite_img['0'], Big_stomper.sprite_img['1'], Big_stomper.sprite_img['2']]
      idle_low = [Big_stomper.sprite_img['3'], Big_stomper.sprite_img['4'], Big_stomper.sprite_img['5']]
      closed_high = [Big_stomper.sprite_img['6'], Big_stomper.sprite_img['7'], Big_stomper.sprite_img['8']]
      closed_low = [Big_stomper.sprite_img['9'], Big_stomper.sprite_img['10'], Big_stomper.sprite_img['11']]

      frame_speed = 10
      main_sprite = Sprite(universal_var.main_sprite, x, y, width, height, [
                                                                              ('idle_high', idle_high, frame_speed),
                                                                              ('idle_low', idle_low, frame_speed),
                                                                              ('closed_high', closed_high, frame_speed),
                                                                              ('closed_low', closed_low, frame_speed)
                                                                           ])

      main_collbox = Collision_box(universal_var.hitbox, x, y, width, height-30, (40, 80, 100),y_offset=15)
      ceiling_collbox = Collision_box("ceiling_collbox", x, y, width-10, 15, (150, 180, 100), x_offset=5)
      ground_collbox = Collision_box("ground_collbox", x, y, width-20, 15, (150, 180, 100), x_offset=10, y_offset=height-15)

      super().__init__('big_stomper', x, y, [main_sprite], [main_collbox, ceiling_collbox, ground_collbox], is_active, width, height, display_layer, 
                       gravity, direction, max_x_vel, health_points, damage_points, x_clip_offset, y_clip_offset)

      self.grounded = False
      self.max_y_vel = 10
      self.can_jump = False
      self.y_vel = 0
      self.all_timers.add_ID('wait', 20)
      self.all_timers.add_ID('prepare_to_jmp', 30)
      self.all_timers.add_ID('no_display', 7)
      self.all_timers.add_ID('y_accel_flag', 4)
      self.add_big_explosion(x_offset=10, y_offset=20, radius=36)
      Big_stomper.add_to_class_lst(self, Megaman_object.hazards, self.ID)


   def respawn(self):
      Enemy.respawn(self)
      self.grounded = False
      self.max_y_vel = 10
      self.can_jump = False
      self.y_vel = 0
      for timer in self.all_timers:
         self.all_timers.replenish_timer(timer)

   def display(self, surf):
      if self.all_timers.is_finished('no_display') and self.is_alive():
         if universal_var.game_pause != True:
            self.update_sprite(universal_var.main_sprite)

         if self.all_timers.is_finished('prepare_to_jmp') == False:

            if self.all_timers.is_almost_finished('prepare_to_jmp', 15):
               self.display_animation(universal_var.main_sprite, surf, 'closed_low', resume=True)
            else:
               self.display_animation(universal_var.main_sprite, surf, 'closed_high', resume=True)
            self.all_timers.countdown('prepare_to_jmp')

         elif self.all_timers.is_finished('prepare_to_jmp') or self.all_timers.is_finished('wait') != True:
            if self.grounded or self.y_vel > 0:
               self.display_animation(universal_var.main_sprite, surf, 'idle_high', resume=True)
            elif self.y_vel <= 0:
               self.display_animation(universal_var.main_sprite, surf, 'idle_low', resume=True, y_offset=-20)

      elif self.is_alive() == False:
         self.display_explosions(surf)


   def check_all_collisions(self):
      ceiling_collision = self.check_collision_lst(Megaman_object.platforms, "ceiling_collbox", universal_var.hitbox, quota=1)
      if ceiling_collision.is_empty() != True and self.y_vel > 0:
         self.y_vel = 0
         self.all_timers.replenish_timer('y_accel_flag')

      if self.grounded == False and self.y_vel <= 0 and ceiling_collision.is_empty(): #touched ground
         ground_collision = self.check_collision_lst(Megaman_object.platforms, 'ground_collbox', universal_var.hitbox, quota=1)
         if ground_collision.is_empty() != True:
            platform = ground_collision.pop()
            self.push_vert(platform, 'ground_collbox', universal_var.hitbox)
            self.all_timers.replenish_timer('prepare_to_jmp')
            self.all_timers.replenish_timer('wait')
            self.grounded = True
            play_sound('big_stomper_landing', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.1)

      wall_collision = self.check_collision_lst(Megaman_object.platforms, universal_var.hitbox, universal_var.hitbox, quota=1)
      if wall_collision.is_empty() != True:
         wall = wall_collision.pop()
         self.push_hori(wall, universal_var.hitbox, universal_var.hitbox)

      if self.grounded == False and self.is_alive():
         if self.all_timers.is_finished('y_accel_flag'):
            self.all_timers.replenish_timer('y_accel_flag')
            self.y_vel -= 2
         else:
            self.all_timers.countdown('y_accel_flag')
         if self.direction == True:
            self.x += self.max_x_vel
         else:
            self.x -= self.max_x_vel
         self.y -= self.y_vel

      if self.check_pshooter_contact(False, True, 30) and self.is_alive() == False:
         play_sound('big_explosion', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume - 0.3)
               

   def update(self):
      if self.is_alive() and universal_var.game_reset != True and universal_var.game_pause != True:
         if self.grounded:

            if self.all_timers.is_finished('prepare_to_jmp') != True:
               self.all_timers.countdown('prepare_to_jmp')

            elif self.can_jump:
               m = megaman.Megaman.all_sprite_surfaces[0]
               if m.x + m.width//2 < self.x + self.width//2:
                  self.direction = False
               else:
                  self.direction = True
               self.y_vel = self.max_y_vel
               self.can_jump = False
               self.grounded = False

            elif self.grounded:
               if self.all_timers.is_finished('wait') != True:
                  self.all_timers.countdown('wait')
               else:
                  self.all_timers.replenish_timer('prepare_to_jmp')
                  self.all_timers.replenish_timer('wait')
                  self.can_jump = True

         self.check_all_collisions()

      self.all_timers.countdown('no_display')
      Enemy.update(self)