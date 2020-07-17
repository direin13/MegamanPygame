#!/usr/bin/env python
import universal_var
from sprite import *
import pygame
import timer
from misc_function import *
from p_shooter import *
from megaman import *
import megaman_object
from enemy import *
from character import *
from bar import Energy_bar
from megaman_death_orb import Death_orb
import camera
import projectile
from concrete_shot import Concrete_shot

class Megaman(Character):
   all_sprite_surfaces = []
   def __init__(self, ID, x, y, controls=None):

      width = 90
      height = 80
      display_layer = 3
      max_x_vel = 3
      health_points = 100
      is_active = False
      gravity = False
      m_run_speed = 32
      m_idle_speed = 150
      direction = True

      megaman_walk = [universal_var.megaman_images['walk_2'], universal_var.megaman_images['walk_1'], universal_var.megaman_images['walk_2'],
                      universal_var.megaman_images['walk_3']]

      megaman_idle = [universal_var.megaman_images['idle'], universal_var.megaman_images['idle'], universal_var.megaman_images['idle'],
                      universal_var.megaman_images['idle'], universal_var.megaman_images['idle'], universal_var.megaman_images['idle_2']]

      megaman_idle_shoot = [universal_var.megaman_images['idle_shoot']]
      megaman_step = [universal_var.megaman_images['step']]
      megaman_shoot = [universal_var.megaman_images['walk_shoot_2'], universal_var.megaman_images['walk_shoot_1'],
                       universal_var.megaman_images['walk_shoot_2'], universal_var.megaman_images['walk_shoot_3']]

      megaman_jump = [universal_var.megaman_images['jump']]
      megaman_shoot_jump = [universal_var.megaman_images['shoot_jump']]
      megaman_damage = [universal_var.megaman_images['damage']]

      megaman_concretized = [universal_var.megaman_images['concretized']]

      megaman_sprite = Sprite(universal_var.main_sprite, x, y, width, height, [('walk', megaman_walk, m_run_speed),
                                                               ('idle', megaman_idle, m_idle_speed),
                                                             ('step', megaman_step, m_run_speed),
                                                             ('shoot_walk', megaman_shoot, m_run_speed),
                                                             ('shoot_idle', megaman_idle_shoot, m_run_speed),
                                                             ('jump', megaman_jump, m_run_speed),
                                                             ('shoot_jump', megaman_shoot_jump, m_run_speed),
                                                             ('damage', megaman_damage, m_idle_speed),
                                                             ('concretized', megaman_concretized, m_idle_speed)
                                                             ])

      effects = Sprite('effects', x, y, width, height, [('spark_effect', [universal_var.misc_images['spark']], 1)])

      #--collision boxes
      megaman_hit_box = Collision_box(universal_var.hitbox, x, y, 55, 59, (240, 240, 0), x_offset=17)
      megaman_feet = Collision_box(universal_var.feet, x, y, 41, 3, (240, 21, 0), x_offset=26, y_offset=61)
      megaman_head = Collision_box(universal_var.head, x, y, 43, 2, (200, 21, 0), x_offset=24, y_offset=-3)
      
      super().__init__(ID, x, y, [megaman_sprite, effects], [megaman_hit_box, megaman_feet, megaman_head], is_active, width, height,
                       display_layer, gravity, direction, max_x_vel, health_points)

      if controls == None:
         self.controls = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_p, pygame.K_w]
      else:
         self.controls = controls #--right, up, left, down, action, jump--

      self.get_keys = True
      self.keys_pressed = pygame.key.get_pressed()
      self.jump_speed = 10
      self.acc_speed = 3
      self.decc_speed = 0
      self.can_jump = False
      self.lives = 2
      self.health_points_copy = self.health_points
      self.health_bar = Energy_bar('megaman_health', x=30, y=20, points=self.health_points, colour1=(255, 223, 131), colour2=(255, 255, 211))

      respawn_sprite = Sprite(universal_var.main_sprite, 0, 0, self.width, self.height, [('drop_down', [universal_var.misc_images['spawn_1']], 15),
                              ('spawn', [universal_var.misc_images['spawn_2'], universal_var.misc_images['spawn_3'], universal_var.misc_images['spawn_1']], 15)])
      self.respawn_obj = megaman_object.Megaman_object('respawn', 0, 0, [respawn_sprite], None, is_active=False, display_layer=3)
      self.all_timers.add_ID('respawn_animation', 15)

      self.all_timers.add_ID('rise_flag', 4)
      self.all_timers.add_ID('shooting_flag', 0)
      self.all_timers.add_ID('can_shoot', 1)
      self.all_timers.add_ID('startup_flag', 0)
      self.all_timers.add_ID('startup_animation', 0)
      self.all_timers.add_ID('death_sound', 1)
      self.all_timers.add_ID('death', 30)
      self.all_timers.add_ID('freeze', 0)

      self.stun_time = 50
      self.concrete_stun = False
      self.all_timers.add_ID('stun', self.stun_time)
      Death_orb.init(12) #These orbs are shot out when megaman dies
      for i in range(0, 3): #--making p_shooter bullets
         P_shooter('p_shooter', 0, 0)

      Megaman.add_to_class_lst(self, Megaman.all_sprite_surfaces, ID)


   def disable_keys(self):
      self.get_keys = False

   def enable_keys(self):
      self.get_keys = True

   def is_pressing(self, n):
      #'n' refers to index in self.controls
      if self.stun is True or self.keys_pressed == None:
         return False
      else:
         return self.keys_pressed[self.controls[n]]

   def is_stunned(self):
      return self.all_timers.is_finished('stun') != True

   def is_standstill(self):
      return (not(self.is_pressing(0) or self.is_pressing(2)) or 
            (self.is_pressing(0) and self.is_pressing(2)))

   def is_shooting(self):
      return self.all_timers.is_finished('shooting_flag') == False
   
   def check_stun(self):
      if universal_var.game_pause != True:
         self.all_timers.countdown('stun') #Knock back until timer is finished

      if self.all_timers.is_finished('stun'):
         self.stun = False
         self.all_timers.get_ID('stun')['origin'] = self.stun_time
         self.concrete_stun = False

      elif self.all_timers.is_finished('freeze') and self.concrete_stun != True:
         self.knock_back(1)
      else:
         self.all_timers.countdown('freeze')
   
   def freeze(self, amount):
      self.stun = True
      self.all_timers.replenish_timer('stun', amount)
      self.all_timers.replenish_timer('freeze', amount)

   def set_direction(self):
      #--note that direction == False means direction == Left, whereas True == Right

      if self.is_standstill():
         self.direction = self.direction

      elif self.is_pressing(0):
         #--right
         if self.is_grounded != True:
            self.direction = True
         else:
            if self.x_vel == 0:
               self.direction = True

      elif self.is_pressing(2):
         #--left
         if self.is_grounded != True:
            self.direction = False
         else:
            if self.x_vel == 0:
               self.direction = False

   def stop(self):
      #brings player to a halt
      if self.is_grounded == True:
         self.deccelerate(self.decc_speed)
      else:
         self.x_vel = 0

      if self.direction == True:
         self.x += self.x_vel
      else:
         self.x -= self.x_vel

   def move_L(self):
      if self.is_grounded == True:
         if self.direction == False:
            self.accelerate(self.acc_speed, self.max_x_vel)
            self.x -= self.x_vel
         else:
            self.deccelerate(self.decc_speed)
            self.x += self.x_vel

      else:
         self.x_vel = self.max_x_vel
         self.x -= self.x_vel


   def move_r(self):
      if self.is_grounded == True:
         if self.direction == True:
            self.accelerate(self.acc_speed, self.max_x_vel)
            self.x += self.x_vel
         else:
            self.deccelerate(self.decc_speed)
            self.x -= self.x_vel

      else:
         self.x_vel = self.max_x_vel
         self.x += self.x_vel


   def check_hazard_collision(self):
      collision = self.check_collision_lst(Megaman_object.hazards, universal_var.hitbox, universal_var.hitbox, quota=1)
      if collision.is_empty() != True:
         hazard = collision.pop()
         self.damage_megaman(hazard)

   def damage_megaman(self, hazard):
      if hazard.is_alive() and hazard.is_active and self.invincibility == False:
         self.reduce_hp(hazard.damage_points)
         if self.is_alive() == False:
            pass
         else:
            self.y_vel = 0
            self.invincibility = True
            self.stun = True
            play_sound('megaman_damage', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume + 0.1)
            self.all_timers.replenish_timer('spark_effect')
            self.all_timers.replenish_timer('stun')

      if isinstance(hazard, Concrete_shot) and hazard.is_active:
         hazard.is_active = False
         self.concrete_stun = True
         self.freeze(130)


   def check_all_collisions(self):
      #This will check all the sprite surfaces and there relation with self and act accordingly
      if camera.camera_transitioning() != True:
         self.check_ground_collision(universal_var.feet)
         self.check_ceiling_collision(universal_var.head)
         self.check_wall_collision(universal_var.hitbox)
         self.check_hazard_collision()


   def shoot(self):

      #--if you shoot
      if self.all_timers.is_finished('can_shoot') == False and P_shooter.all_p_stack.is_empty() != True:
         self.all_timers.countdown('can_shoot')
         self.all_timers.replenish_timer('shooting_flag') #the display function will countdown this timer
         play_sound('p_shooter', universal_var.megaman_sounds, volume=universal_var.sfx_volume)

         #--right
         if self.direction == True:
            P_shooter.set(self.x + self.width - 15, self.y + self.height//4, vel=70, angle=0)

         #--left
         else:
            P_shooter.set(self.x + 4, self.y + self.height//4, vel=70, angle=180)


   def check_key_pressed(self):
      if self.is_standstill() == True:
         if self.stun != True:
            self.stop()

         #--if pressing right
      elif self.is_pressing(0) and self.colliding_hori != True and camera.camera_transitioning() != True:
         self.move_r()

      #--if pressing left
      elif self.is_pressing(2) and self.colliding_hori != True and camera.camera_transitioning() != True:
         self.move_L()

      #--if you shoot
      if self.is_pressing(4) and camera.camera_transitioning() != True:
         self.shoot()
      else:
         self.all_timers.replenish_timer('can_shoot') #the player can shoot after he lets go of the shoot button

      if camera.camera_transitioning() != True:
         self.jump()



   def jump(self):
      if self.is_grounded is True and self.can_jump is True:
         self.all_timers.replenish_timer('rise_flag')
         self.y_vel = 10
         if self.is_pressing(5) and camera.camera_transitioning() != True:
            self.y_vel = self.jump_speed

      if self.gravity is False and self.is_pressing(5):
         self.rise()
      else:
         if self.y_vel > 0:
            self.y_vel = 0
         self.gravity = True

      if self.is_pressing(5) != True and self.is_grounded is True:
         self.can_jump = True
      else:
         self.can_jump = False


   def rise(self):
      if self.y_vel <= 0:
         self.gravity = True
      else:
         self.all_timers.countdown('rise_flag', 5, loop=True)
         if self.all_timers.is_finished('rise_flag') != True:
            self.y -= self.y_vel
         else:
            self.y_vel -= 2


   def startup_check(self):
      #will return true if startup animation is valid
      if universal_var.game_pause == False:
         self.all_timers.countdown('startup_animation')

      if self.is_standstill() and self.all_timers.is_finished('startup_flag') == False:
         if universal_var.game_pause == False:
            self.all_timers.countdown('startup_flag')
         return True

      elif self.is_standstill() != True and self.all_timers.is_finished('startup_flag'):
         self.all_timers.replenish_timer('startup_flag', 1)
         return True
      else:
         return False


   def startup_animation(self, surf):
      if self.direction == True:
         self.display_animation(universal_var.main_sprite, surf, 'step')

      else:
         self.display_animation(universal_var.main_sprite, surf, 'step', flip=True)



   def idle_animation(self, surf, s=''):
      if self.direction == True:
         self.display_animation(universal_var.main_sprite, surf, '{}idle'.format(s))
      else:
         self.display_animation(universal_var.main_sprite, surf, '{}idle'.format(s), flip=True)



   def walk_animation(self, surf, s=''):
      if self.direction == True:
         self.display_animation(universal_var.main_sprite, surf, '{}walk'.format(s), resume=True)

      else:
         self.display_animation(universal_var.main_sprite, surf, '{}walk'.format(s), flip=True, resume=True)



   def ground_animation(self, surf, s=''):
      #--displaying any ground animations

      if self.all_timers.is_finished('startup_animation') is not True and s == '':
         self.startup_animation(surf)

      else:
         if self.is_standstill() == True:
            self.idle_animation(surf, s)
         else:
            self.walk_animation(surf, s)



   def jump_animation(self, surf, s=''):
      if self.direction == True:
         self.display_animation(universal_var.main_sprite, surf, '{}jump'.format(s))
      else:
         self.display_animation(universal_var.main_sprite, surf, '{}jump'.format(s), flip=True)

   def diplay_effects(self, surf):
      if self.all_timers.is_finished('spark_effect') is False:
         self.display_animation('effects', surf, 'spark_effect')
         if universal_var.game_pause == False:
            self.all_timers.countdown('spark_effect')

   def stun_animation(self, surf):
      if self.concrete_stun != True:
         if self.direction == True:
            self.display_animation(universal_var.main_sprite, surf, 'damage')
         else:
            self.display_animation(universal_var.main_sprite, surf, 'damage', flip=True)

      else:
         if self.direction == True:
            self.display_animation(universal_var.main_sprite, surf, 'concretized')
         else:
            self.display_animation(universal_var.main_sprite, surf, 'concretized', flip=True)


   def display_megaman(self, surf, s=''):
      if self.startup_check() is True:
         self.all_timers.replenish_timer('startup_animation', 8)

      if self.no_display is False or camera.camera_transitioning() is True:
         if self.stun is True:
            self.stun_animation(surf)

         elif self.is_grounded is True:
            self.ground_animation(surf, s)
         else: 
            self.jump_animation(surf, s)

   def display(self, surf):
      #--displays self's sprites depending on the circumstances i.e if he's on the ground, if he shoots etc.
      if self.is_shooting():
         s = 'shoot_'
      else:
         s = ''

      if self.is_alive() and universal_var.game_pause != True:
         self.update_sprite(universal_var.main_sprite)

      if self.invincibility is True:
         self.diplay_effects(surf)

      self.display_megaman(surf, s)


   def invincibility_frames(self):
      if self.all_timers.is_finished('invincibility_frame'):
         if self.no_display is True:
            self.no_display = False
         else:
            self.no_display = True
         self.all_timers.replenish_timer('invincibility_frame')

      else:
         if universal_var.game_pause != True:
            self.all_timers.countdown('invincibility_frame')


   def check_invincibility(self):
      if self.all_timers.is_finished('invincibility'):
         self.invincibility = False
         self.no_display = False
         self.all_timers.replenish_timer('invincibility')

      else:
         if universal_var.game_pause != True:
            self.all_timers.countdown('invincibility')
         self.invincibility_frames()


   def update(self):
      if self.is_alive() and self.is_active:
         if camera.camera_transitioning() != True and universal_var.game_pause != True and self.get_keys:
            self.keys_pressed = pygame.key.get_pressed() #if the camera is not transitioning the I can catch input
         elif self.get_keys == False:
            self.keys_pressed = None

         self.set_direction()
         if universal_var.game_pause == False:
            self.all_timers.countdown('shooting_flag', 20)
         self.check_all_collisions()
         self.health_bar.points = self.health_points

         if self.stun is True:
            self.check_stun()

         if self.invincibility is True:
            self.check_invincibility()

         if universal_var.game_pause != True:
            self.check_key_pressed()
         
         if self.gravity is True and camera.camera_transitioning() != True:
            self.apply_gravity()

         Sprite_surface.update(self)
         self.colliding_hori = False
         self.colliding_vert = False

         if self.y > universal_var.screen_height + 550 and universal_var.debug != True:
            self.health_points -= self.health_points #death
            self.health_bar.points -= self.health_bar.points

      elif self.is_alive() != True:
         self.keys_pressed = None
         if self.all_timers.is_finished('death'):
            universal_var.game_pause = False
            self.is_active = False
            if self.all_timers.is_finished('death_sound') is not True:
               start_times = [0, 15, 35]
               angles = [0, 90, 180, 270, 45, 135, 225, 315, 0, 90, 180, 270]
               i = 0
               for time in start_times:
                  Death_orb.set_orb_active(self.x + 20, self.y + 20, time, angles[i], 15)
                  Death_orb.set_orb_active(self.x + 20, self.y + 20, time, angles[i+1], 15)
                  Death_orb.set_orb_active(self.x + 20, self.y + 20, time, angles[i+2], 15)
                  Death_orb.set_orb_active(self.x + 20, self.y + 20, time, angles[i+3], 15)
                  i += 4
               play_sound('death', universal_var.megaman_sounds, channel=5, volume=universal_var.sfx_volume + 0.1)
               self.all_timers.countdown('death_sound')

         else:
            self.all_timers.countdown('death')
            universal_var.game_pause = True

         if universal_var.game_reset:
            Death_orb.reset()

   def respawn(self):
      if self.respawn_obj.is_active == False:
         self.respawn_obj.y = self.spawn_point[1] - universal_var.screen_height  # set sprite_surf's falling spawn animation above screen
      if self.respawn_obj.y < self.spawn_point[1] - 15:
         self.respawn_obj.row = 0
         self.respawn_obj.x = self.spawn_point[0]
         self.respawn_obj.is_active = True
         self.respawn_obj.move(0, 18)
      else:
         if self.all_timers.is_finished('respawn_animation') != True:
            self.respawn_obj.row = 1
            self.respawn_obj.x, self.respawn_obj.y = self.spawn_point[0], self.spawn_point[1] - 15
            self.all_timers.countdown('respawn_animation')
         else:
            play_sound('megaman_spawn', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume + 0.1)
            self.respawn_obj.is_active = False
            self.health_points = self.health_points_copy
            self.health_bar.points = self.health_points_copy
            self.health_bar.is_active = True
            self.is_active = True
            self.stun = False
            self.concrete_stun = False
            self.no_display = False
            self.invincibility = False
            self.x, self.y = self.spawn_point[0], self.spawn_point[1]
            self.x_vel = 0
            self.y_vel = 0
            Sprite_surface.update(self)
            Death_orb.reset()
            self.all_timers.replenish_timer('startup_flag', 0)
            self.all_timers.replenish_timer('shooting_flag', 0)
            self.all_timers.replenish_timer('grounded_sound', 0)
            self.all_timers.replenish_timer('startup_animation', 0)
            for timer in self.all_timers:
               if timer not in ['shooting_flag', 'startup_animation', 'startup_flag', 'grounded_sound', 'freeze']:
                  self.all_timers.replenish_timer(timer)
