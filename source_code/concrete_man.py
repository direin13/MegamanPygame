from megaman_object import Megaman_object
from megaman import Megaman
from sprite import Sprite_surface, Sprite, Collision_box
from timer import Timer
from misc_function import load_images, play_sound
import universal_var
from bar import Energy_bar
from megaman_death_orb import Death_orb
from p_shooter import P_shooter
from concrete_shot import Concrete_shot
from random import randint
import projectile
from camera import World_camera
from boss_room import Boss_room

class Concrete_man(Megaman_object):
   sprite_imgs = load_images('resources/enemies/concrete_man')

   def __init__(self, x, y, trigger_coll_box, spawn=False):
      width, height = 130, 105

      idle_imgs = [Concrete_man.sprite_imgs['idle']]
      intro_imgs = [Concrete_man.sprite_imgs['intro_1'], Concrete_man.sprite_imgs['intro_2'], Concrete_man.sprite_imgs['intro_3']]
      falling_imgs = [Concrete_man.sprite_imgs['falling']]
      charge_imgs = [Concrete_man.sprite_imgs['charge_1'], Concrete_man.sprite_imgs['charge_2']]
      shoot_imgs = [Concrete_man.sprite_imgs['shoot']]
      jump_imgs = [Concrete_man.sprite_imgs['jump']]
      prepare_jump_imgs = [Concrete_man.sprite_imgs['prepare_jump']]
      landing_imgs = [Concrete_man.sprite_imgs['landing_1'], Concrete_man.sprite_imgs['landing_2'], Concrete_man.sprite_imgs['landing_3']]

      sprite = Sprite(universal_var.main_sprite, x, y, width, height, active_frames=[
                                                                          ('idle', idle_imgs, 1),
                                                                          ('introduction', intro_imgs, 33),
                                                                          ('falling', falling_imgs, 100),
                                                                          ('charge', charge_imgs, 10),
                                                                          ('shoot', shoot_imgs, 1),
                                                                          ('prepare_jump', prepare_jump_imgs, 1),
                                                                          ('jump', jump_imgs, 1),
                                                                          ('landing', landing_imgs, 25)
                                                                       ])

      effects = Sprite('effects', x, y, 100, 90, active_frames=[
                                                                        ('spark_effect', [universal_var.misc_images['spark']], 1)
                                                                     ])

      main_collbox = Collision_box(universal_var.hitbox, x, y, width-40, height-30, (40, 80, 100), x_offset=20, y_offset=15)
      ground_collbox = Collision_box("ground_collbox", x, y, width-80, 15, (150, 180, 100), x_offset=40, y_offset=height-15)

      super().__init__('concrete_man', x, y, [sprite, effects], [main_collbox, ground_collbox], 
                       width=width, height=height, is_active=False, direction=False, display_layer=3)

      Death_orb.init(16)
      projectile.Projectile.init_projectile_properties(self)
      for i in range(3):
         Concrete_shot()

      self.trigger_coll_box = Boss_room(self, trigger_coll_box.x, trigger_coll_box.y, trigger_coll_box.width, trigger_coll_box.height)
      self.health_points = 440 #440
      self.original_health_points = self.health_points
      self.damage_points = 15
      self.original_damage_points = self.damage_points
      self.battle_has_init = False
      self.grounded = False
      self.health_bar = Energy_bar('health_bar', x=70, y=20, points=self.health_points, colour1=(242, 138, 0), colour2=(255, 255, 255))
      self.health_bar.points = 0
      self.current_action = 'introduction'
      self.action_list = ['idle', 'charge', 'introduction', 'shoot', 'stomp']
      self.all_timers = Timer()
      self.all_timers.add_ID('idle_time', 25)
      self.all_timers.add_ID('damage_taken', 0)
      self.all_timers.add_ID('shake_camera', 20)

      #--timers and variables for action methods--

      #charge action
      self.all_timers.add_ID('time_till_charge', 15)
      self.all_timers.add_ID('time_till_wall_detect', 2)
      self.collided_with_wall = False

      #shoot action
      self.all_timers.add_ID('shoot_time', 20)

      #stomp action
      self.all_timers.add_ID('time_till_jump', 10)
      self.all_timers.add_ID('time_till_fall', 15)
      self.all_timers.add_ID('landing_time', 30)
      self.falling = False
      self.jump_destination = [0, 190]

      Concrete_man.add_to_class_lst(self, Megaman_object.hazards, self.ID)
      if spawn:
         self.spawn()

#--main methods--

   def is_alive(self):
      return self.health_points > 0


   def spawn(self):
      self.x, self.y = self.spawn_point[0], self.spawn_point[1]
      self.is_active = True
      self.direction = False
      self.reset_atrributes()
      Sprite_surface.update(self)
      for ID in self.all_timers:
         if ID != 'damage_taken':
            self.all_timers.replenish_timer(ID)

   def display(self, surf):
      if self.all_timers.is_finished('damage_taken', include_loop=True) != True:
         self.display_animation('effects', surf, 'spark_effect', x_offset=16, y_offset=20)
         self.update_sprite('effects')
         if universal_var.game_pause != True:
            self.all_timers.countdown('damage_taken', loop=True, loop_amount=7)

      if self.direction == True:
         flip = True
      else:
         flip = False

      no_sprite_flicker = self.all_timers.is_almost_finished('damage_taken', self.all_timers.get_ID('damage_taken')['origin']//2)

      if no_sprite_flicker:
         if self.current_action == 'introduction':
            self.display_intro_animation(surf, flip)

         elif self.current_action == 'idle':
            self.display_idle_animation(surf, flip)

         elif self.current_action == 'charge':
            self.display_charge_animation(surf, flip)

         elif self.current_action == 'shoot':
            self.display_shoot_animation(surf, flip)

         elif self.current_action == 'stomp':
            self.display_stomp_animation(surf, flip)


   def carry_out_action(self):
      if self.current_action == 'introduction':
         self.introduction_action()

      elif self.is_alive() and universal_var.game_pause != True:
         if self.current_action == 'idle':
            self.idle_action()

         elif self.current_action == 'charge':
            self.charge_action()

         elif self.current_action == 'shoot':
            self.shoot_action()

         elif self.current_action == 'stomp':
            self.stomp_action()


   def update(self):
      self.carry_out_action()
         
      self.check_collisions()

      if self.grounded == False and self.is_active and self.launched != True:
         self.apply_gravity()

      if universal_var.game_reset:
         self.is_active = False
         self.reset_atrributes()

      if self.trigger_coll_box.battle_has_init:
         self.health_bar.points = self.health_points
         if self.is_alive() != True and self.is_active:
            self.explode()

      Sprite_surface.update(self)


#--collision detection functions--
   def check_collisions(self):
      if self.is_active:
         #touched ground
         if self.grounded == False:
            ground_collision = self.check_collision_lst(Megaman_object.platforms, 'ground_collbox', universal_var.hitbox, quota=1)
            if ground_collision.is_empty() != True:
               platform = ground_collision.pop()
               if isinstance(platform, Concrete_shot) and self.current_action == 'stomp' and self.falling:
                  platform.shatter()
               else:
                  self.push_vert(platform, 'ground_collbox', universal_var.hitbox)
                  self.grounded = True

         #touch wall
         wall_collision = self.check_collision_lst(Megaman_object.platforms, universal_var.hitbox, universal_var.hitbox, quota=1)
         if wall_collision.is_empty() != True:
            wall = wall_collision.pop()
            if isinstance(wall, Concrete_shot) and self.current_action == 'charge':
               wall.shatter()
            else:
               self.push_hori(wall, universal_var.hitbox, universal_var.hitbox)
               if self.all_timers.is_finished('time_till_wall_detect'):
                  self.collided_with_wall = True
                  self.all_timers.replenish_timer('time_till_wall_detect')
               else:
                  self.all_timers.countdown('time_till_wall_detect')

      #player pshooter
      pshooter_collisions = self.check_collision_lst(P_shooter.all_p_lst, universal_var.hitbox, universal_var.hitbox, quota=1)
      if pshooter_collisions.is_empty() != True and self.is_alive():
         collision = True
         p = pshooter_collisions.pop()
         if p.reflected == False:
            self.health_points -= p.damage_points
            self.health_bar.points -= p.damage_points
            p.is_active = False
            p.launched = False
            play_sound('impact_p', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.1)
            if self.is_alive() and self.all_timers.is_finished('damage_taken', include_loop=True):
                  self.all_timers.replenish_timer('damage_taken', 5)
#=================================================


#--action methods--
   def introduction_action(self):
      if self.health_bar.is_full():
         self.trigger_coll_box.battle_has_init = True
         self.choose_action(['charge', 'stomp'])


   def idle_action(self):
      self.damage_points = 17
      if self.all_timers.is_finished('idle_time') != True:
         self.all_timers.countdown('idle_time')
      else:
         m = Megaman.all_sprite_surfaces[0]
         if m.x + m.width//2 > self.x + self.width//2:
            self.direction = True
         else:
            self.direction = False
         self.choose_action(self.action_list)
         self.all_timers.replenish_timer('time_till_wall_detect')


   def charge_action(self):
      self.damage_points = 19
      if self.direction == True:
         vel = 8
         angle = 96
      else:
         angle = 84
         vel = -8

      if self.all_timers.is_finished('time_till_charge') != True: #wait for a bit before charging forward
         self.all_timers.countdown('time_till_charge')
         self.all_timers.replenish_timer('time_till_wall_detect')
      else:
         if self.collided_with_wall != True:
            if universal_var.game_pause != True:
               self.x += vel

         elif self.launched != True and self.collided_with_wall: #hit the wall
            play_sound('concrete_man_impact', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.1)
            self.grounded = False
            self.y -= 1
            self.all_timers.replenish_timer('shake_camera', 10)
            projectile.Projectile.set(self, self.x, self.y, 80, angle, 23)

         else:
            if self.grounded != True:
               if universal_var.game_pause != True:
                  projectile.Projectile.move(self)
                  self.shake_camera()

            else: #landed and reset
               self.launched = False
               self.collided_with_wall = False
               self.all_timers.replenish_timer('time_till_charge', 10)

               self.action_list = ['shoot', 'shoot', 'stomp', 'stomp', 'charge']
               self.all_timers.replenish_timer('idle_time')
               self.current_action = 'idle'


   def shoot_action(self):
      if Concrete_shot.all_p_stack.is_empty() and self.all_timers.is_full('shoot_time'):
         self.all_timers.replenish_timer('shoot_time')
         self.collided_with_wall = False

         self.action_list = ['charge', 'stomp']
         self.all_timers.replenish_timer('idle_time', 35)
         self.current_action = 'idle'

      else:
         self.damage_points = 16
         if self.all_timers.is_full('shoot_time'):
            play_sound('concrete_man_shoot', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.1)
            megaman = Megaman.all_sprite_surfaces[0]
            x_dist = abs(self.x + self.width//2 - megaman.x + megaman.width//2)
            vel = 0
            angle = 0

            if x_dist <= 40: #when player is very close shoot 1 bullet
               vel, angle = 45, 77
               if self.direction == True:
                  Concrete_shot.set(self.x + self.width - 40, self.y + 20, vel, angle, 22)
               else:
                  angle = 180 - angle
                  Concrete_shot.set(self.x - 20, self.y + 20, vel, angle, 22)

            else:
               if x_dist <= 150:    #choose from 3 distances
                  vel, angle = 35, 70

               elif x_dist <= 350:
                  vel, angle = 38, 65

               elif x_dist <= 600:
                  vel, angle = 55, 65

               if self.direction == True:
                  Concrete_shot.set(self.x + self.width - 40, self.y + 20, vel, angle, 24)
                  Concrete_shot.set(self.x + self.width - 40, self.y + 20, vel+32, angle+5, 24)
                  Concrete_shot.set(self.x + self.width - 40, self.y + 20, vel+30, angle-10, 24)
               else:
                  angle = 180 - angle
                  Concrete_shot.set(self.x - 20, self.y + 20, vel, angle, 24)
                  Concrete_shot.set(self.x - 20, self.y + 20, vel+32, angle-5, 24)
                  Concrete_shot.set(self.x - 20, self.y + 20, vel+27, angle+10, 24)


         if self.all_timers.is_finished('shoot_time') != True:
            self.all_timers.countdown('shoot_time')
         else:
            self.all_timers.replenish_timer('shoot_time')
            self.collided_with_wall = False

            self.action_list = ['charge', 'stomp']
            self.all_timers.replenish_timer('idle_time', 35)
            self.current_action = 'idle'


   def stomp_action(self):

      self.damage_points = 18
      megaman = Megaman.all_sprite_surfaces[0]
      if self.all_timers.is_finished('time_till_jump') != True:
         self.all_timers.countdown('time_till_jump')
         self.jump_destination[0] = megaman.x

      else:
         x_dest, y_dest = self.jump_destination[0], self.jump_destination[1]
         if self.falling != True:
            if self.all_timers.is_finished('time_till_jump') and universal_var.game_pause != True:
               self.hone_in(x_dest, y_dest, 10, min_x_vel=3, min_y_vel=4, max_x_vel=10, max_y_vel=10)

            if self.y == y_dest:
               self.all_timers.countdown('time_till_fall')
               if self.all_timers.is_finished('time_till_fall'):
                  self.falling = True
                  projectile.Projectile.set(self, self.x, self.y, 20, 270, 23)
                  self.grounded = False

         else:
            if self.grounded != True:
               self.all_timers.replenish_timer('shake_camera', 20)
               if universal_var.game_pause != True:
                  projectile.Projectile.move(self)
            else:
               if self.all_timers.is_full('landing_time'):
                  play_sound('concrete_man_impact', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.1)
                  for p in Concrete_shot.all_p_lst:
                     p.shatter()
                  if megaman.is_grounded:
                     megaman.freeze(60)

               self.all_timers.countdown('landing_time')
               self.launched = False
               self.shake_camera()

               if self.all_timers.is_finished('landing_time'):
                  self.all_timers.replenish_timer('time_till_jump')
                  self.all_timers.replenish_timer('time_till_fall')
                  self.all_timers.replenish_timer('landing_time')
                  self.falling = False
                  self.collided_with_wall = False

                  self.action_list = ['shoot', 'shoot', 'stomp', 'charge']
                  self.all_timers.replenish_timer('idle_time')
                  self.current_action = 'idle'
                  
#========================================


#--display action methods--
   def display_idle_animation(self, surf, flip=False):
      if self.grounded != True:
         self.display_animation(universal_var.main_sprite, surf, 'falling', flip=flip)
      else:
         self.display_animation(universal_var.main_sprite, surf, 'idle', flip=flip)


   def display_intro_animation(self, surf, flip=False):
      if self.grounded != True:
         self.display_animation(universal_var.main_sprite, surf, 'falling', flip=flip)
         self.update_sprite(universal_var.main_sprite)
      else:
         self.display_animation(universal_var.main_sprite, surf, 'introduction', flip=flip)
         if universal_var.game_pause != True:
            self.update_sprite(universal_var.main_sprite, auto_reset=False, loop_amount=2)


   def display_charge_animation(self, surf, flip=False):
      if self.grounded != True:
         self.display_animation(universal_var.main_sprite, surf, 'falling', flip=flip)
      else:
         self.display_animation(universal_var.main_sprite, surf, 'charge', flip=flip)

      if universal_var.game_pause != True:
         self.update_sprite(universal_var.main_sprite)

   def display_shoot_animation(self, surf, flip=False):
      self.display_animation(universal_var.main_sprite, surf, 'shoot', flip=flip)


   def display_stomp_animation(self, surf, flip=False):
      if self.all_timers.is_finished('time_till_jump') != True:
         self.display_animation(universal_var.main_sprite, surf, 'prepare_jump', flip=flip)
      else:

         if self.falling != True:
            self.display_animation(universal_var.main_sprite, surf, 'jump', flip=flip)
         else:

            if self.grounded != True:
               self.display_animation(universal_var.main_sprite, surf, 'falling', flip=flip)

            else:
               if universal_var.game_pause != True:
                  self.update_sprite(universal_var.main_sprite, auto_reset=False, loop_amount=1)
               self.display_animation(universal_var.main_sprite, surf, 'landing', flip=flip)

#=====================================================


   #--misc methods--
   def choose_action(self, lst):
      index = randint(0, len(lst)-1)
      self.current_action = lst[index]

   def explode(self):
      start_times = [0, 15]
      speeds = [15, 10]
      angles = [0, 45, 90, 135, 180, 225, 270, 315]
      i = 0
      for j in range(2):
         Death_orb.set_orb_active(self.x + 20, self.y + 20, start_times[j], angles[i], speeds[j])
         Death_orb.set_orb_active(self.x + 20, self.y + 20, start_times[j], angles[i+1], speeds[j])
         Death_orb.set_orb_active(self.x + 20, self.y + 20, start_times[j], angles[i+2], speeds[j])
         Death_orb.set_orb_active(self.x + 20, self.y + 20, start_times[j], angles[i+3], speeds[j])
         Death_orb.set_orb_active(self.x + 20, self.y + 20, start_times[j], angles[i+4], speeds[j])
         Death_orb.set_orb_active(self.x + 20, self.y + 20, start_times[j], angles[i+5], speeds[j])
         Death_orb.set_orb_active(self.x + 20, self.y + 20, start_times[j], angles[i+6], speeds[j])
         Death_orb.set_orb_active(self.x + 20, self.y + 20, start_times[j], angles[i+7], speeds[j])

      play_sound('death', universal_var.megaman_sounds, channel=5, volume=universal_var.sfx_volume + 0.1)
      self.is_active = False


   def reset_atrributes(self):
      self.trigger_coll_box.battle_has_init = False
      self.grounded = False
      self.health_points = self.original_health_points
      self.damage_points = self.original_damage_points
      self.current_action = 'introduction'
      self.collided_with_wall = False
      self.launched = False
      self.falling = False


   def shake_camera(self):
      if self.all_timers.is_finished('shake_camera') != True:
         World_camera.shake(6, 0, 5)
         self.all_timers.countdown('shake_camera')

#=============================================================



#----------------------------------------------------------------------------STAGE PROPS----------------------------------------------------------------------------------
props = [
              ['bg', (0,0), (2400, 600), (['map_1'], 30), 1, (0,0,0,0)], ['bg', (2399,0), (1800, 600), (['map_2'], 30), 1, (0,0,0,0)], 
              ['bg', (3600,600), (600, 600), (['map_3'], 30), 1, (0,0,0,0)], ['bg', (2400,1200), (1800, 600), (['map_4'], 30), 1, (0,0,0,0)], 
              ['bg', (2400,1800), (600, 1800), (['map_5'], 30), 1, (0,0,0,0)], ['bg', (2400,3600), (3000, 600), (['map_6'], 30), 1, (0,0,0,0)],

              ['bg', (169,557), (45, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (0,0,0,0)], ['bg', (214,557), (45, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (0,0,0,0)],
              ['bg', (256,557), (45, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (0,0,0,0)], ['bg', (298,557), (45, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (0,0,0,0)],
              ['bg', (169,530), (45, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)], ['bg', (214,530), (45, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)],
              ['bg', (256,530), (45, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)], ['bg', (298,530), (45, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)],

              ['bg', (517,557), (43, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (0,0,0,0)], ['bg', (517+43,557), (44, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (0,0,0,0)],
              ['bg', (517+43*2,557), (43, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (0,0,0,0)], ['bg', (517+43*3,557), (44, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (0,0,0,0)],
              ['bg', (517,530), (43, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)], ['bg', (517+43,530), (45, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)],
              ['bg', (517+43*2,530), (43, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)], ['bg', (517+43*3,530), (45, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)],

              ['bg', (1250,557), (43, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (0,0,0,0)], ['bg', (1250+43,557), (44, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (0,0,0,0)],
              ['bg', (1250+43*2,557), (43, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (0,0,0,0)], ['bg', (1250+43*3,557), (44, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (0,0,0,0)],
              ['bg', (1250,530), (43, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)], ['bg', (1250+43,530), (45, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)],
              ['bg', (1250+43*2,530), (43, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)], ['bg', (1250+43*3,530), (45, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)],
              ['bg', (1250+43*4,557), (43, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (0,0,0,0)], ['bg', (1250+43*5,557), (44, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (0,0,0,0)],
              ['bg', (1250+43*4,530), (43, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)], ['bg', (1250+43*5,530), (45, 27), (['waterdrop_1', 'waterdrop_2', 'waterdrop_3'], 17), 0, (0,0,0,0)],

              ['bg', (3387,3569), (45, 250), (['waterfall_1', 'waterfall_2'], 10), 4, (0,0,0,0)], ['bg', (3387,3569+250), (45, 250), (['waterfall_1', 'waterfall_2'], 10), 4, (0,0,0,0)],
              ['bg', (3387,3569+250*2), (45, 250), (['waterfall_1', 'waterfall_2'], 10), 4, (0,0,0,0)],

              ['bg', (3487,3569), (45, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (170,170,170,0)], 
              ['bg', (3487,3569+250), (45, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (170,170,170,0)],
              ['bg', (3487,3569+250*2), (45, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (170,170,170,0)],

              ['bg', (3887,3569), (45, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (170,170,170,0)], 
              ['bg', (3887,3569+250), (45, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (170,170,170,0)],
              ['bg', (3887,3569+250*2), (45, 250), (['waterfall_2', 'waterfall_1'], 10), 0, (170,170,170,0)],
              ['bg', (3887+45,3569), (45, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (170,170,170,0)], 
              ['bg', (3887+45,3569+250), (45, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (170,170,170,0)],
              ['bg', (3887+45,3569+250*2), (45, 250), (['waterfall_1', 'waterfall_2'], 10), 0, (170,170,170,0)],

              ['bg', (3447,4044), (43, 27), (['waterdrop_2', 'waterdrop_1', 'waterdrop_3'], 17), 0, (170,170,170,0)], 
              ['bg', (3532,4044), (43, 27), (['waterdrop_2', 'waterdrop_1', 'waterdrop_3'], 17), 0, (170,170,170,0)],

              ['bg', (3847,4001), (43, 27), (['waterdrop_2', 'waterdrop_1', 'waterdrop_3'], 17), 0, (170,170,170,0)],
              ['bg', (3977,4001), (43, 27), (['waterdrop_2', 'waterdrop_1', 'waterdrop_3'], 17), 0, (170,170,170,0)],
              ['gate', (4157,3846)], ['gate', (4757,3846)]
        ]

all_items = [
             ['e_life', 3556, 3730], ['l_hcap', 2484, 3079], ['s_hcap', 2748, 3738], ['s_hcap', 3659, 1077]
            ]

coll_boxes = [
              [(-20,0), (20,600), 'platform'], [(0,472), (1806,40), 'platform'], [(690,429), (345, 40), 'platform'], [(1208,429), (345, 40), 'platform'], 
              [(1728,385), (345, 40), 'platform'], [(2074,342), (342,642), 'platform'], [(2419,472), (254,206), 'platform'], [(2764,472), (257,317), 'platform'],
              [(3110,429), (170,402), 'platform'], [(3414,472), (559,173), 'platform'], [(3719,387), (230,103), 'platform'], [(3803,302), (167,203), 'platform'],
              [(3759,129), (213,171), 'platform'], [(3455,249), (173,46), 'platform'], [(3455,0), (85,249), 'platform'], [(4112,-182), (87,2000), 'platform'],
              [(3769,867), (351,127), 'platform'], [(3630,1117), (257,125), 'platform'], [(2907,1628), (2067,1876), 'platform'], [(3565,642), (59,771), 'platform'],
              [(3590,1300), (15,771), 'platform'], [(2986,1300), (15,771), 'platform'], [(2403,1200), (82,3198), 'platform'], [(2568,1997), (258,44), 'platform'],
              [(2818,2231), (85,41), 'platform'], [(2492,2231), (85,41), 'platform'], [(2656,2043), (42,1743), 'platform'], [(2698,2584), (129,41), 'platform'],
              [(2775,2704), (129,41), 'platform'], [(2700,2827), (129,41), 'platform'], [(2682,2400), (254,6), 'platform'], [(2483,3095), (47,41), 'platform'],
              [(2659,3776), (427,43), 'platform'], [(2827,4066), (1422,144), 'platform'], [(2483,4025), (348,172), 'platform'],
              [(3790,4022), (1058,178), 'platform'], [(4030,3515), (815,330), 'platform'], [(2994,3515), (10,1000), 'platform'],
              [(4848,4157), (550,500), 'platform'], [(4224,3842), (16,213), 'platform'], [(4821,3847), (24,193), 'platform'], [(5359,3760), (500,435), 'platform'],
              [(3269,3776), (79,43), 'platform'], [(3556,3776), (38,43), 'platform'],

              [(0,-300), (267,1500), 'c_box'], [(3918,-178), (283,1278), 'c_box'], [(3600, 600), (600, 1200), 'c_box'], 
              [(3000, 1200), (600, 600), 'c_box'], [(2400,1200), (600, 3000), 'c_box'],
              [(3000,3527), (265,1278), 'c_box'], [(3923,3527), (1500,1278), 'c_box'],

              [(3853, 578), 400, 't_box', 'down',], [(3600, 1184), 800, 't_box', 'down'], 
              [(3607, 1423), 446, 't_box', 'left'], [(3000, 1423), 546, 't_box', 'left'],
              [(2410, 1765), 581, 't_box', 'down'], [(2410, 2391), 581, 't_box', 'down'], 
              [(2407, 2978), 605, 't_box', 'down'], [(2407, 3558), 605, 't_box', 'down'],
              [(2990, 3623), 546, 't_box', 'right']
             ]

enemies = [
           [(3735,370), 'met', False, 130, 50], [(4196,823), 'lasor', 45, -6], [(3592-1400,1072), 'lasor', 148, 6], 
           [(2392-1400,1950), 'lasor', 73, 6], [(3074,2187), 'lasor', 53, -6], [(2393-1400,2539), 'lasor', 3, 6], 
           [(3074,2661), 'lasor', 50, -6], [(2393-1400,2783), 'lasor', 78, 6], [(2717,620), 'det', 90, 57, 140, 600], 
           [(3059,620), 'det', 80, 70, 150, 600], [(3347,620), 'det', 80, 77, 170, 600],
           [(3289,3755), 'met', False, 160, 50], [220, 'hoohoo', 70, (603,198), (750,279)],
           [230, 'hoohoo', 40, (1360,128), (1245,479)], [90, 'hoohoo', 100, (1360,128), (1045,479)], [80, 'hoohoo', 70, (2626,171), (567,479)], 
           [280, 'hoohoo', 60, (2484,3679), (500,600)], [90, 'hoohoo', 70, (3190,3582), (576,479)],
           [(3130,1549), 'paozo', True], [(3681, 4064), 'big_stomper', 22], [(3321, 4064), 'big_stomper', 22],
           [(5224, 3200), 'concrete_man', (4845,3762), (600,600), False]
          ]