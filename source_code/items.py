import pygame
import random
import universal_var
from sprite import *
from megaman_object import Megaman_object
from misc_function import load_images, play_sound
from megaman import Megaman
from camera import camera_transitioning

class Item(Megaman_object):
   drop_list = []
   item_images = load_images('resources/misc')
   randint_offset = 0

   @staticmethod
   def drop_list_init():
      for i in range(80):
         Item.drop_list.append(None)

      for i in range(2):
         s = Extra_life(0, 0, is_drop=True)
         Item.randint_offset += 1

      for i in range(5):
         s = Health_capsule(0, 0, True, is_drop=True)
         Item.randint_offset += 1

      for i in range(9):
         s = Health_capsule(0, 0, False, is_drop=True)
         Item.randint_offset += 1


   def __init__(self, ID, x, y, width, height, sprites=None, coll_boxes=None, is_drop=False, display_layer=2):

      if is_drop == False:
         is_active = True
      else:
         is_active = False
         index = random.randint(0, Item.randint_offset)
         Item.drop_list.insert(index, self)

      super().__init__(ID, x, y, sprites, coll_boxes, width=width, height=height, is_active=is_active, gravity=True, display_layer=display_layer)
      self.all_timers.add_ID('time_till_vanish', 700)
      self.is_drop = is_drop


   @staticmethod
   def drop_item(x, y, randint_offset=0):
      randint_offset += Item.randint_offset
      
      if randint_offset > len(Item.drop_list) - 1:
         randint_offset = len(Item.drop_list) - 1

      index = random.randint(0, randint_offset)
      item = Item.drop_list.pop(index)

      if item == None:
         Item.drop_list.append(item)
      else:
         item.is_active = True
         item.x, item.y = x, y
         item.y_vel = 1
         Sprite_surface.update(item)
      return item

   def update(self):
      if universal_var.game_reset != True:

         if self.is_active:
            ground_collsions = self.check_collision_lst(Megaman_object.platforms, universal_var.hitbox, universal_var.hitbox, quota=1)
            if ground_collsions.is_empty() == False:
               g = ground_collsions.pop()
               self.push_vert(g, universal_var.hitbox, universal_var.hitbox)
            else:
               self.apply_gravity()

         if self.is_drop:
            if (self.is_active and (self.is_on_screen() and 
               self.all_timers.is_finished('time_till_vanish') == False)):

               if universal_var.game_pause == False:
                  self.all_timers.countdown('time_till_vanish')
            else:
               self.is_active = False
               self.all_timers.replenish_timer('time_till_vanish')
               if self not in Item.drop_list:
                  index = random.randint(0, Item.randint_offset)
                  Item.drop_list.insert(index, self)
      Sprite_surface.update(self)


#--------------------------------------------------------------------------------------------------------------------------


class Extra_life(Item):
   def __init__(self, x, y, is_drop=False):
      width, height = 40, 40
      sprite = Sprite(universal_var.main_sprite, x, y, width, height, [
                                                            ('extra_life_img', [Item.item_images['extra_life']], 1)
                                                         ])
      coll_box = Collision_box(universal_var.hitbox, x, y, width-20, height, (255, 255, 255), x_offset=10)
      super().__init__('extra_life', x, y, width, height, [sprite], [coll_box], is_drop)

   def display(self, surf):
      if self.is_active and universal_var.game_reset == False and camera_transitioning() == False:
         self.display_animation(universal_var.main_sprite, surf, 'extra_life_img')

   def update(self):
      if self.is_active:
         megaman_collision = self.check_collision_lst(Megaman.all_sprite_surfaces, universal_var.hitbox, universal_var.hitbox)
         if megaman_collision.is_empty() != True:
            m = megaman_collision.pop()
            m.lives += 1
            self.is_active = False
            play_sound('extra_life', universal_var.megaman_sounds, channel=4, volume=universal_var.sfx_volume - 0.2)
      Item.update(self)


#---------------------------------------------------------------------------------------------------------------------


class Health_capsule(Item):
   def __init__(self, x, y, large=False, is_drop=False):
      if large == False:
         width = 18
         height = 18
         sprite_imgs = [Item.item_images['small_health_cap_1'], Item.item_images['small_health_cap_2']]
         health_points = 10
      else:
         width = 40
         height = 40
         sprite_imgs = [Item.item_images['big_health_cap_1'], Item.item_images['big_health_cap_2']]
         health_points = 25

      sprite = Sprite(universal_var.main_sprite, x, y, width, height, [
                                                                        ('health_capsule', sprite_imgs, 11)
                                                                      ])
      coll_box = Collision_box(universal_var.hitbox, x, y, width-10, height, (255,255,255), x_offset=5)
      super().__init__('health_capsule', x, y, width, height, [sprite], [coll_box], is_drop)
      self.threshold = health_points
      self.current_added_points = 0
      self.all_timers.add_ID('increment', 2)

   def display(self, surf):
      if universal_var.game_pause != True:
            self.update_sprite(universal_var.main_sprite)

      if self.is_active and universal_var.game_reset == False and camera_transitioning() == False and self.current_added_points == 0:
         self.display_animation(universal_var.main_sprite, surf, 'health_capsule')

   def update(self):
      if self.is_active:
         megaman_collision = self.check_collision_lst(Megaman.all_sprite_surfaces, universal_var.hitbox, universal_var.hitbox)
         if megaman_collision.is_empty() != True and camera_transitioning() != True:
            m = megaman_collision.pop()

            if self.current_added_points != self.threshold and m.health_bar.refill(1):
               self.current_added_points += 1
               m.health_points += 1
               universal_var.game_pause = True

            elif self.current_added_points == self.threshold or m.health_bar.is_full():
               self.is_active = False
               self.current_added_points = 0
               universal_var.game_pause = False

            if self.all_timers.is_finished('increment'):
               self.all_timers.replenish_timer('increment')
            else:
               self.all_timers.countdown('increment')

      Item.update(self)