import mega_stack
import sprite
import universal_var
from projectile import Projectile
from megaman_object import Megaman_object
from timer import Timer
from misc_function import play_sound
from p_shooter import P_shooter


class Concrete_shot(Projectile):
   all_p_stack = mega_stack.Stack()
   all_p_lst = []

   def __init__(self):
      width = 60
      height = 50
      x, y = 0, 0
      concrete_shot_liquid = [universal_var.projectiles['concrete_shot_1'], universal_var.projectiles['concrete_shot_2']]
      concrete_shot_solid = [universal_var.projectiles['concrete_block_1'], universal_var.projectiles['concrete_block_2']]
      concrete_shatter = [universal_var.projectiles['concrete_block_3'], universal_var.projectiles['concrete_block_4']]
      bullet_sprite = sprite.Sprite(universal_var.main_sprite, x, y, width, height, [
                                                                                       ('concrete_shot_liquid', concrete_shot_liquid, 6),
                                                                                       ('concrete_shot_solid', concrete_shot_solid, 6),
                                                                                       ('concrete_block_shatter', concrete_shatter, 14)
                                                                                    ])

      main_coll_box = sprite.Collision_box(universal_var.hitbox, 0, 0, width-20, height-17, (240, 240, 0), x_offset=10)
      ground_collbox = sprite.Collision_box('ground_collbox', x, y, width-30, 15, (150, 180, 100), x_offset=15, y_offset=height-17)

      super().__init__('Enemy_projectile_1', x, y, [bullet_sprite], [main_coll_box, ground_collbox], width=width, height=height, display_layer=4)
      self.damage_points = 13
      self.grounded = False
      self.solidified = False
      self.is_shattered = False
      self.all_timers = Timer()
      self.all_timers.add_ID('shatter', 28)
      Concrete_shot.all_p_stack.push(self)
      Concrete_shot.add_to_class_lst(self, Concrete_shot.all_p_lst, self.ID)


   @classmethod
   def set(cls, x, y, vel=0, angle=0, gravity=0):
      if cls.all_p_stack.is_empty() != True:
         p = cls.all_p_stack.pop()
         Concrete_shot.add_to_class_lst(p, Megaman_object.hazards, p.ID)
         p.grounded = False
         p.is_shattered = False
         Projectile.set(p, x, y, vel, angle=angle, gravity=gravity)


   def display(self, surf):
      if self.is_active:
         if self.grounded != True:
            if universal_var.game_pause != True:
               self.update_sprite(universal_var.main_sprite)
            self.display_animation(universal_var.main_sprite, surf, 'concrete_shot_liquid')

         else:
            if self.is_shattered != True:
               self.display_animation(universal_var.main_sprite, surf, 'concrete_shot_solid')
            else:
               self.display_animation(universal_var.main_sprite, surf, 'concrete_block_shatter')

            if universal_var.game_pause != True:
                  self.update_sprite(universal_var.main_sprite, auto_reset=False, loop_amount=1)


   def ground_collision(self):
      #touched ground
      if self.grounded == False:
         ground_collision = self.check_collision_lst(Megaman_object.platforms, 'ground_collbox', universal_var.hitbox, quota=1)
         if ground_collision.is_empty() != True:
            platform = ground_collision.pop()
            if not(isinstance(platform, Concrete_shot)):
               Megaman_object.push_vert(self, platform, 'ground_collbox', universal_var.hitbox)
               #play_sound('big_stomper_landing', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.1)
               return True
      return False

   def wall_collision(self):
      #touch wall
      wall_collision = self.check_collision_lst(Megaman_object.platforms, universal_var.hitbox, universal_var.hitbox, quota=1)
      if wall_collision.is_empty() != True:
         wall = wall_collision.pop()
         if not(isinstance(wall, Concrete_shot)) and self.is_shattered != True:
            self.shatter()
            self.launched = False
            return True
      return False


   def check_pshooter_contact(self):
      collision = False
      pshooter_collisions = self.check_collision_lst(P_shooter.all_p_lst, universal_var.hitbox, universal_var.hitbox, quota=1)

      if pshooter_collisions.is_empty() != True and self.is_alive():
         collision = True
         p = pshooter_collisions.pop()
         if p.reflected == False:
            if p.x < self.x:
               Projectile.set(p, p.x, p.y, vel=90, angle=130)
            else:
               Projectile.set(p, p.x, p.y, vel=90, angle=70)
            p.reflected = True
            play_sound('p_reflected', universal_var.megaman_sounds, channel=1, volume=universal_var.sfx_volume + 0.1)


   def shatter(self):
      self.all_timers.replenish_timer('shatter', 10)
      self.is_shattered = True
      if self in Megaman_object.platforms:
         Megaman_object.platforms.remove(self)



   def update(self):
      #print(self.is_active, self.x, self.y)
      if self.is_active:
         self.wall_collision()

         if self.ground_collision() and self.solidified != True:
            play_sound('concrete_shot_solidify', universal_var.megaman_sounds, channel=2, volume=universal_var.sfx_volume - 0.3)
            self.grounded = True
            self.launched = False
            self.solidified = True
            Concrete_shot.add_to_class_lst(self, Megaman_object.platforms, self.ID)
            Megaman_object.hazards.remove(self)

         if self.solidified:
            self.check_pshooter_contact()

         if self.all_timers.is_finished('shatter') and self.is_shattered:
            self.is_active = False
         elif universal_var.game_pause != True:
            self.all_timers.countdown('shatter')


      elif self not in Concrete_shot.all_p_stack.lst: #reset properties
         self.is_shatter = False
         self.solidified = False
         Concrete_shot.all_p_stack.push(self)
         if self in Megaman_object.platforms:
            Megaman_object.platforms.remove(self)
         if self in Megaman_object.hazards:
                  Megaman_object.hazards.remove(self)

      if universal_var.game_pause != True:
         Projectile.update(self)


#----------------------------------------------------------------------